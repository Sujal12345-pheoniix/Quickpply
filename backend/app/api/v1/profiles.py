from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID

from app.dependencies import get_current_user, get_db
from app.schemas import ProfileResponse, ResumeUploadResponse
from app.models import Profile, ProfileSkill, User
from app.utils.resume_parser import extract_text_from_pdf, parse_resume_with_gemini

router = APIRouter()


@router.get("")
async def get_profile(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    # Query profile from database
    stmt = select(Profile).where(Profile.user_id == user.id)
    result = await db.execute(stmt)
    profile = result.scalars().first()

    if not profile:
        return {
            "id": str(user.id),
            "full_name": user.full_name or "New Candidate",
            "headline": "No resume uploaded yet",
            "summary": "",
            "years_experience": 0,
            "current_title": "",
            "current_company": "",
            "location": "",
            "willing_to_relocate": False,
            "remote_preference": "remote",
            "skills": []
        }

    # Fetch skills
    skills_stmt = select(ProfileSkill).where(ProfileSkill.profile_id == profile.id)
    skills_result = await db.execute(skills_stmt)
    skills = [s.skill_name for s in skills_result.scalars().all()]

    return {
        "id": str(profile.id),
        "full_name": user.full_name or "Candidate",
        "headline": profile.headline,
        "summary": profile.summary,
        "years_experience": float(profile.years_experience or 0),
        "current_title": profile.current_title,
        "current_company": profile.current_company,
        "location": profile.location,
        "willing_to_relocate": profile.willing_to_relocate,
        "remote_preference": profile.remote_preference,
        "skills": skills
    }


@router.post("/resume")
async def upload_resume(
    file: UploadFile = File(...),
    remote_preference: str = Form("remote"),
    location_preference: str = Form(""),
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF resumes are supported currently.")

    # Read bytes
    pdf_bytes = await file.read()
    
    # Extract text
    resume_text = extract_text_from_pdf(pdf_bytes)
    if not resume_text:
        raise HTTPException(status_code=400, detail="Unable to extract text from the PDF file.")

    # Parse with Gemini
    parsed_data = await parse_resume_with_gemini(resume_text)
    if not parsed_data:
        raise HTTPException(status_code=500, detail="Failed to parse resume text using Gemini AI.")

    # 1. Update User full name if available
    user_name = parsed_data.get("full_name")
    if user_name:
        user_stmt = select(User).where(User.id == user.id)
        u_res = await db.execute(user_stmt)
        db_user = u_res.scalars().first()
        if db_user:
            db_user.full_name = user_name

    # 2. Check/Upsert Profile
    profile_stmt = select(Profile).where(Profile.user_id == user.id)
    p_res = await db.execute(profile_stmt)
    profile = p_res.scalars().first()

    if not profile:
        profile = Profile(
            user_id=user.id,
            headline=parsed_data.get("headline", "AI Developer"),
            summary=parsed_data.get("summary", ""),
            years_experience=parsed_data.get("years_experience", 0.0),
            current_title=parsed_data.get("current_title", ""),
            current_company=parsed_data.get("current_company", ""),
            location=location_preference or parsed_data.get("location", "Remote"),
            remote_preference=remote_preference,
            raw_resume_text=resume_text,
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    else:
        profile.headline = parsed_data.get("headline", profile.headline)
        profile.summary = parsed_data.get("summary", profile.summary)
        profile.years_experience = parsed_data.get("years_experience", profile.years_experience)
        profile.current_title = parsed_data.get("current_title", profile.current_title)
        profile.current_company = parsed_data.get("current_company", profile.current_company)
        profile.location = location_preference or parsed_data.get("location", profile.location)
        profile.remote_preference = remote_preference
        profile.raw_resume_text = resume_text
        await db.commit()

    # 3. Re-populate skills
    # Clear old skills
    await db.execute(delete(ProfileSkill).where(ProfileSkill.profile_id == profile.id))
    
    skills = parsed_data.get("skills", [])
    for skill_name in skills:
        p_skill = ProfileSkill(
            profile_id=profile.id,
            skill_name=skill_name,
            proficiency="advanced"
        )
        db.add(p_skill)
        
    await db.commit()

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "parsed_status": "completed",
        "message": "Resume successfully parsed and profile updated.",
        "parsed_data": parsed_data
    }
