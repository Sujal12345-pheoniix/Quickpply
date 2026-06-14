from fastapi import APIRouter, Depends, Query

from app.dependencies import get_current_user
from app.schemas import DiscoverJobsResponse, ImportJobRequest, JobListResponse, JobSummary

router = APIRouter()


@router.get("")
async def list_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    min_score: int | None = None,
    user=Depends(get_current_user),
) -> JobListResponse:
    return JobListResponse(
        data=[
            JobSummary(
                id="job_01",
                title="Senior Product Manager, AI Hiring",
                company="ArcLabs",
                location="Remote",
                source="LinkedIn",
                match_score=min_score or 89,
                interview_probability=71,
                salary_range="$180k-$220k",
                posted_at="2026-06-12",
            )
        ],
        meta={"page": page, "page_size": page_size, "total": 1, "has_next": False},
    )


@router.post("/discover")
async def discover_jobs(user=Depends(get_current_user)) -> DiscoverJobsResponse:
    return DiscoverJobsResponse(
        task_id="job-discovery-dev-001",
        message="Job discovery queued across configured sources",
    )


@router.post("/import")
async def import_job(payload: ImportJobRequest, user=Depends(get_current_user)):
    return {"message": "Job import queued", "url": str(payload.url)}
