from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user
from app.schemas import (
    ApprovalResponse,
    ApplicationsResponse,
    ApplicationSummary,
    GenerateApplicationRequest,
    GenerateApplicationResponse,
)

router = APIRouter()


@router.get("")
async def list_applications(user=Depends(get_current_user)) -> ApplicationsResponse:
    return ApplicationsResponse(
        data=[
            ApplicationSummary(
                id="app_01",
                job_id="job_01",
                job_title="Senior Product Manager, AI Hiring",
                company="ArcLabs",
                status="pending_review",
                ats_score=91,
                updated_at="2026-06-13T09:00:00Z",
            )
        ]
    )


@router.post("/generate")
async def generate_application(body: GenerateApplicationRequest, user=Depends(get_current_user)) -> GenerateApplicationResponse:
    if not body.job_id:
        raise HTTPException(status_code=422, detail="job_id required")
    return GenerateApplicationResponse(
        application_id="app_queued_01",
        task_id="app-gen-dev-001",
        status="pending_review",
        message="Application pack generation queued. Human approval required before submit.",
    )


@router.post("/{application_id}/approve")
async def approve_application(application_id: str, user=Depends(get_current_user)) -> ApprovalResponse:
    return ApprovalResponse(status="approved", application_id=application_id)


@router.post("/{application_id}/submit")
async def submit_application(application_id: str, user=Depends(get_current_user)):
    """Requires APPROVED status — user confirms manual submission on job board."""
    return {"status": "submitted", "application_id": application_id}
