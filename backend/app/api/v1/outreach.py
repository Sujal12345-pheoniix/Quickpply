from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from pydantic import BaseModel
import google.generativeai as genai

from app.dependencies import get_current_user, get_db
from app.models import Application, Job, Profile, ProfileSkill, OutreachMessage, OutreachChannel
from app.config import settings

router = APIRouter()


class GenerateOutreachRequest(BaseModel):
    application_id: str
    recipient_name: str
    recipient_title: str
    channel: str  # linkedin_dm, email


async def generate_recruiter_message_with_gemini(
    candidate_name: str,
    headline: str,
    summary: str,
    skills: list[str],
    job_title: str,
    company: str,
    recruiter_name: str,
    recruiter_title: str,
    channel: str
) -> str:
    if not settings.GOOGLE_AI_API_KEY:
        return "GOOGLE_AI_API_KEY not configured. Failed to generate outreach."

    genai.configure(api_key=settings.GOOGLE_AI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are an expert recruiter and career coach. Write a highly personalized, short, professional cold outreach message from a candidate to a recruiter/hiring manager.
    The message must sound natural, professional, and confident, avoiding generic corporate templates or AI jargon (like 'hope this finds you well', 'delve', 'testament').
    The candidate is attaching their resume.

    Outreach Channel: {channel} (if linkedin_dm, keep it under 300 characters. If email, make it under 150 words with a subject line at the top).

    Candidate Name: {candidate_name}
    Candidate Headline: {headline}
    Candidate Skills: {', '.join(skills)}
    Candidate Summary: {summary}

    Target Role: {job_title} at {company}
    Recipient Name: {recruiter_name}
    Recipient Title: {recruiter_title}

    Output ONLY the written message body (with subject line at the top if it's an email).
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print("Error generating outreach message:", e)
        return "Failed to generate outreach message due to AI model error."


@router.post("/generate")
async def generate_outreach(
    payload: GenerateOutreachRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        app_uuid = UUID(payload.application_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid application_id format")

    # Fetch Application
    app_stmt = select(Application).where((Application.id == app_uuid) & (Application.user_id == user.id))
    app_res = await db.execute(app_stmt)
    app = app_res.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Application record not found")

    # Fetch Job
    job_stmt = select(Job).where(Job.id == app.job_id)
    job_res = await db.execute(job_stmt)
    job = job_res.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Target job details not found")

    # Fetch User Profile & Skills
    profile_stmt = select(Profile).where(Profile.user_id == user.id)
    p_res = await db.execute(profile_stmt)
    profile = p_res.scalars().first()

    skills = []
    headline = "Professional Candidate"
    summary = ""
    if profile:
        headline = profile.headline or headline
        summary = profile.summary or summary
        skills_stmt = select(ProfileSkill).where(ProfileSkill.profile_id == profile.id)
        s_res = await db.execute(skills_stmt)
        skills = [s.skill_name for s in s_res.scalars().all()]

    # Generate outreach message body
    message_body = await generate_recruiter_message_with_gemini(
        candidate_name=user.full_name or "Candidate",
        headline=headline,
        summary=summary,
        skills=skills,
        job_title=job.title,
        company=job.company_name,
        recruiter_name=payload.recipient_name,
        recruiter_title=payload.recipient_title,
        channel=payload.channel
    )

    # Convert channel string to enum
    outreach_channel_enum = OutreachChannel.linkedin_dm if payload.channel == "linkedin_dm" else OutreachChannel.email

    # Save to database
    outreach_msg = OutreachMessage(
        application_id=app.id,
        user_id=user.id,
        channel=outreach_channel_enum,
        recipient_name=payload.recipient_name,
        recipient_title=payload.recipient_title,
        subject="Regarding Job Application" if payload.channel == "email" else None,
        body=message_body,
        is_sent=False
    )
    db.add(outreach_msg)
    await db.commit()
    await db.refresh(outreach_msg)

    return {
        "id": str(outreach_msg.id),
        "channel": payload.channel,
        "recipient_name": payload.recipient_name,
        "recipient_title": payload.recipient_title,
        "message": message_body,
        "attached_resume": "resume.pdf"
    }
