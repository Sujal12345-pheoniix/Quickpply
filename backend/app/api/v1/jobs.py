from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.dependencies import get_current_user, get_db
from app.schemas import DiscoverJobsResponse, ImportJobRequest, JobListResponse, JobSummary
from app.models import Job, JobSource

router = APIRouter()


async def seed_jobs_if_empty(db: AsyncSession):
    # Check if we have any jobs in the DB
    stmt = select(Job)
    result = await db.execute(stmt)
    existing_jobs = result.scalars().all()
    
    if not existing_jobs:
        # Seed realistic jobs
        jobs_to_seed = [
            Job(
                title="Senior Product Manager, AI Hiring",
                company_name="ArcLabs",
                location="Remote, US",
                source=JobSource.linkedin,
                source_url="https://linkedin.com/jobs/view/arclabs-ai-pm",
                description="Lead product management for ArcLabs automated hiring assistant. Work with LLMs and agents to streamline workflows.",
                is_active=True,
                salary_min=180000,
                salary_max=220000,
                salary_currency="USD",
                required_skills=["Product Management", "AI", "LLMs", "Agile"],
                role_competitiveness=40,
                estimated_applicants=25,
            ),
            Job(
                title="Founding PM, Workforce Automation",
                company_name="TalentOS",
                location="San Francisco, CA",
                source=JobSource.wellfound,
                source_url="https://wellfound.com/jobs/talentos-founding-pm",
                description="Define the roadmap for our next-gen enterprise workforce orchestration platform. First product hire role.",
                is_active=True,
                salary_min=150000,
                salary_max=190000,
                salary_currency="USD",
                required_skills=["Product Management", "Workforce Automation", "SaaS"],
                role_competitiveness=55,
                estimated_applicants=15,
            ),
            Job(
                title="AI Operations Lead",
                company_name="Northstar",
                location="Remote",
                source=JobSource.remoteok,
                source_url="https://remoteok.com/jobs/northstar-ai-ops",
                description="Manage LLM pipeline deployments, monitor costs, and coordinate evaluation workflows for our customer service agent.",
                is_active=True,
                salary_min=140000,
                salary_max=170000,
                salary_currency="USD",
                required_skills=["Operations", "LLMOps", "Python", "Docker"],
                role_competitiveness=30,
                estimated_applicants=12,
            ),
            Job(
                title="Staff Software Engineer, LLM Integrations",
                company_name="ApplyPilot",
                location="Hybrid - New York, NY",
                source=JobSource.career_page,
                source_url="https://applypilot.ai/careers/staff-llm-eng",
                description="Design and build highly reliable multi-agent systems and vector indexing architectures for ApplyPilot's resume engines.",
                is_active=True,
                salary_min=200000,
                salary_max=250000,
                salary_currency="USD",
                required_skills=["Python", "LangGraph", "PostgreSQL", "Pinecone"],
                role_competitiveness=65,
                estimated_applicants=38,
            )
        ]
        
        for job in jobs_to_seed:
            db.add(job)
        await db.commit()
        
        # Query again
        result = await db.execute(select(Job))
        existing_jobs = result.scalars().all()
        
    return existing_jobs


@router.get("")
async def list_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    min_score: int | None = None,
    db: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
) -> JobListResponse:
    jobs = await seed_jobs_if_empty(db)
    
    # Map to schemas
    data = []
    for j in jobs:
        # Generate a mock match score based on title and user skills (or use fallback)
        score = 92 if "Product" in j.title else (84 if "Ops" in j.title else 88)
        if min_score and score < min_score:
            continue
            
        data.append(
            JobSummary(
                id=str(j.id),
                title=j.title,
                company=j.company_name,
                location=j.location,
                source=j.source.value,
                match_score=score,
                interview_probability=65 if score > 90 else 45,
                salary_range=f"${j.salary_min // 1000}k-${j.salary_max // 1000}k" if j.salary_min else "Competitive",
                posted_at="2026-06-12",
            )
        )
        
    return JobListResponse(
        data=data,
        meta={"page": page, "page_size": page_size, "total": len(data), "has_next": False},
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
