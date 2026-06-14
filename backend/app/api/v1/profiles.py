from fastapi import APIRouter, Depends, UploadFile, File

from app.dependencies import get_current_user
from app.schemas import ProfileResponse, ResumeUploadResponse

router = APIRouter()


@router.get("")
async def get_profile(user=Depends(get_current_user)) -> ProfileResponse:
    return ProfileResponse(
        id=str(user.id),
        full_name=user.full_name or "Dev User",
        headline="AI-powered job seeker profile",
        location="Remote",
        target_roles=["Product Manager", "Software Engineer", "AI Engineer"],
        onboarding_completed=user.onboarding_completed,
    )


@router.post("/resume")
async def upload_resume(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
) -> ResumeUploadResponse:
    return ResumeUploadResponse(
        filename=file.filename or "resume.pdf",
        content_type=file.content_type,
        message="Resume upload accepted and queued for parsing",
    )
