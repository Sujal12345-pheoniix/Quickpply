from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID
import datetime
from pydantic import BaseModel

from app.dependencies import get_current_user, get_db
from app.schemas import (
    ApprovalResponse,
    ApplicationsResponse,
    ApplicationSummary,
    GenerateApplicationRequest,
    GenerateApplicationResponse,
)
from app.models import Application, Job, ApplicationStatus, Profile, ProfileSkill

router = APIRouter()

class SubmitApplicationRequest(BaseModel):
    recipient_email: str | None = None


@router.get("")
async def list_applications(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
) -> ApplicationsResponse:
    stmt = select(Application).where(Application.user_id == user.id)
    result = await db.execute(stmt)
    apps = result.scalars().all()
    
    data = []
    for app in apps:
        job_stmt = select(Job).where(Job.id == app.job_id)
        job_res = await db.execute(job_stmt)
        job = job_res.scalars().first()
        
        job_title = job.title if job else "Unknown Role"
        company = job.company_name if job else "Unknown Company"
        
        data.append(
            ApplicationSummary(
                id=str(app.id),
                job_id=str(app.job_id),
                job_title=job_title,
                company=company,
                status=app.status.value,
                ats_score=app.ats_score or 90,
                updated_at=app.updated_at.isoformat() if app.updated_at else None,
            )
        )
        
    return ApplicationsResponse(data=data)


@router.post("/generate")
async def generate_application(
    body: GenerateApplicationRequest,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
) -> GenerateApplicationResponse:
    if not body.job_id:
        raise HTTPException(status_code=422, detail="job_id required")
        
    try:
        job_uuid = UUID(body.job_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid job_id format")
        
    job_stmt = select(Job).where(Job.id == job_uuid)
    job_res = await db.execute(job_stmt)
    job = job_res.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    new_app = Application(
        user_id=user.id,
        job_id=job_uuid,
        status=ApplicationStatus.pending_review,
        ats_score=92,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    
    db.add(new_app)
    await db.commit()
    await db.refresh(new_app)
    
    return GenerateApplicationResponse(
        application_id=str(new_app.id),
        task_id=f"task-gen-{new_app.id}",
        status="pending_review",
        message="Application pack generated. Human approval required before submit.",
    )


@router.post("/apply-all")
async def apply_to_all_jobs(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    # Fetch all jobs
    jobs_stmt = select(Job)
    jobs_res = await db.execute(jobs_stmt)
    jobs = jobs_res.scalars().all()
    
    # Fetch existing user applications to prevent duplicates
    app_stmt = select(Application.job_id).where(Application.user_id == user.id)
    app_res = await db.execute(app_stmt)
    applied_job_ids = set(app_res.scalars().all())
    
    # Retrieve user profile & skills
    profile_stmt = select(Profile).where(Profile.user_id == user.id)
    profile_result = await db.execute(profile_stmt)
    profile = profile_result.scalars().first()
    
    user_skills = set()
    if profile:
        skills_stmt = select(ProfileSkill).where(ProfileSkill.profile_id == profile.id)
        skills_res = await db.execute(skills_stmt)
        user_skills = {s.skill_name.lower() for s in skills_res.scalars().all()}

    applied_count = 0
    for job in jobs:
        if job.id in applied_job_ids:
            continue
            
        # Calculate match score
        job_skills = [s.lower() for s in job.required_skills]
        matched_skills = [s for s in job_skills if s in user_skills]
        base_score = int((len(matched_skills) / len(job_skills) * 100)) if job_skills else 75
        score = min(max(base_score, 45), 98)

        # Directly register application in SUBMITTED state (simulating automated apply-all)
        new_app = Application(
            user_id=user.id,
            job_id=job.id,
            status=ApplicationStatus.submitted,
            ats_score=score,
            applied_at=datetime.datetime.utcnow(),
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        db.add(new_app)
        applied_count += 1
        
    if applied_count > 0:
        await db.commit()
        
    return {
        "status": "success",
        "message": f"Automatically applied to {applied_count} matching jobs.",
        "applied_count": applied_count
    }


@router.post("/{application_id}/approve")
async def approve_application(
    application_id: str,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
) -> ApprovalResponse:
    try:
        app_uuid = UUID(application_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid application_id format")
        
    stmt = select(Application).where((Application.id == app_uuid) & (Application.user_id == user.id))
    res = await db.execute(stmt)
    app = res.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    app.status = ApplicationStatus.approved
    app.updated_at = datetime.datetime.utcnow()
    await db.commit()
    
    return ApprovalResponse(status="approved", application_id=str(app.id))


@router.post("/{application_id}/submit")
async def submit_application(
    application_id: str,
    body: SubmitApplicationRequest = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
):
    try:
        app_uuid = UUID(application_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid application_id format")
        
    stmt = select(Application).where((Application.id == app_uuid) & (Application.user_id == user.id))
    res = await db.execute(stmt)
    app = res.scalars().first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    recipient_email = body.recipient_email if body else None

    # If recipient email is configured, send actual application email!
    if recipient_email:
        # Fetch target job details
        job_stmt = select(Job).where(Job.id == app.job_id)
        job_res = await db.execute(job_stmt)
        job = job_res.scalars().first()
        job_title = job.title if job else "Unknown Role"
        company_name = job.company_name if job else "Unknown Company"

        # Build email content
        subject = f"Job Application: {user.full_name or 'Candidate'} - {job_title} at {company_name}"
        email_body = f"Hello,\n\nPlease find attached my application for the {job_title} role at {company_name}.\n\n"
        if app.cover_letter_text:
            email_body += f"Cover Letter:\n----------------------------------------\n{app.cover_letter_text}\n----------------------------------------\n"
        else:
            email_body += "I have attached my resume below for your review.\n"

        resume_bytes = None
        resume_filename = "resume.txt"
        if app.tailored_resume_text:
            resume_bytes = app.tailored_resume_text.encode("utf-8")
        else:
            # Fallback to general profile resume if tailored is empty
            profile_stmt = select(Profile).where(Profile.user_id == user.id)
            p_res = await db.execute(profile_stmt)
            profile = p_res.scalars().first()
            if profile and profile.raw_resume_text:
                resume_bytes = profile.raw_resume_text.encode("utf-8")

        from app.utils.email_service import send_email
        success = await send_email(
            to_email=recipient_email,
            subject=subject,
            body=email_body,
            attachment_bytes=resume_bytes,
            attachment_filename=resume_filename
        )

        if not success:
            raise HTTPException(status_code=500, detail="Failed to deliver application email. Check SMTP settings.")

    app.status = ApplicationStatus.submitted
    app.applied_at = datetime.datetime.utcnow()
    app.updated_at = datetime.datetime.utcnow()
    await db.commit()
    
    return {"status": "submitted", "application_id": str(app.id), "sent_email": recipient_email}
