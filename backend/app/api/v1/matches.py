from fastapi import APIRouter, Depends, Query

from app.dependencies import get_current_user
from app.schemas import MatchListResponse, MatchSummary

router = APIRouter()


@router.get("")
async def list_matches(
    min_score: int = Query(70, ge=0, le=100),
    user=Depends(get_current_user),
) -> MatchListResponse:
    return MatchListResponse(
        data=[
            MatchSummary(
                job_id="job_01",
                job_title="Senior Product Manager, AI Hiring",
                company="ArcLabs",
                match_score=max(min_score, 89),
                interview_probability=71,
                gap_summary=["Needs deeper fintech domain context", "Leadership scope is slightly larger than current profile"],
            )
        ],
        min_score=min_score,
    )
