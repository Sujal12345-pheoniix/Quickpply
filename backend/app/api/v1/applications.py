from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID
import datetime

from app.dependencies import get_current_user, get_db
from app.schemas import (
    ApprovalResponse,
    ApplicationsResponse,
    ApplicationSummary,
    GenerateApplicationRequest,
    GenerateApplicationResponse,
)
from app.models import Application, Job, ApplicationStatus

router = APIRouter()


@router.get("")
async def list_applications(
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user)
) -> ApplicationsResponse:
    # Query all applications for the current user
    stmt = select(Application).where(Application.user_id == user.id)
    result = await db.execute(stmt)
    apps = result.scalars().all()
    
    data = []
    for app in apps:
        # Fetch associated job details
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
        
    # Check if job exists
    job_stmt = select(Job).where(Job.id == job_uuid)
    job_res = await db.execute(job_stmt)
    job = job_res.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Create new application record in draft / pending_review status
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
        
    # Check if application exists and belongs to the user
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
        
    app.status = ApplicationStatus.submitted
    app.applied_at = datetime.datetime.utcnow()
    app.updated_at = datetime.datetime.utcnow()
    await db.commit()
    
    return {"status": "submitted", "application_id": str(app.id)}
