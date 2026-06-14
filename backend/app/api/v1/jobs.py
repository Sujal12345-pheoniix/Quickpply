from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from app.dependencies import get_current_user, get_db
from app.schemas import DiscoverJobsResponse, ImportJobRequest, JobListResponse, JobSummary
from app.models import Job, JobSource, Profile, ProfileSkill

router = APIRouter()


async def seed_jobs_if_empty(db: AsyncSession):
    stmt = select(Job)
    result = await db.execute(stmt)
    existing_jobs = result.scalars().all()
    
    if not existing_jobs:
        jobs_to_seed = [
            Job(
                title="Senior AI Engineer",
                company_name="ArcLabs",
                location="Remote",
                source=JobSource.linkedin,
                source_url="https://linkedin.com/jobs/view/arclabs-ai-eng",
                description="Lead developer for ArcLabs automated agent pipelines. Work with LLMs, prompt engineering, and custom vector search engines.",
                is_active=True,
                salary_min=180000,
                salary_max=220000,
                salary_currency="USD",
                required_skills=["Python", "LLMs", "AI", "Vector Database", "LangChain", "FastAPI"],
                role_competitiveness=40,
                estimated_applicants=25,
            ),
            Job(
                title="Founding Software Engineer, Agentic SaaS",
                company_name="TalentOS",
                location="San Francisco, CA",
                source=JobSource.wellfound,
                source_url="https://wellfound.com/jobs/talentos-saas-eng",
                description="Build and scale our workforce automation SaaS products. Integrate workflows, secure Clerk authentication, and Neon DB pools.",
                is_active=True,
                salary_min=150000,
                salary_max=190000,
                salary_currency="USD",
                required_skills=["React", "Next.js", "TypeScript", "PostgreSQL", "Node.js", "Tailwind"],
                role_competitiveness=55,
                estimated_applicants=15,
            ),
            Job(
                title="LLMOps and Infrastructure Architect",
                company_name="Northstar",
                location="Remote",
                source=JobSource.remoteok,
                source_url="https://remoteok.com/jobs/northstar-llm-ops",
                description="Manage large scale LLM fine-tuning pipelines, monitor prompt usage costs, deploy Docker images, and maintain Redis message streams.",
                is_active=True,
                salary_min=140000,
                salary_max=170000,
                salary_currency="USD",
                required_skills=["Docker", "Kubernetes", "Python", "Redis", "Cloud", "Sentry"],
                role_competitiveness=30,
                estimated_applicants=12,
            ),
            Job(
                title="Fullstack Developer (Next.js & Python)",
                company_name="ApplyPilot",
                location="Remote",
                source=JobSource.career_page,
                source_url="https://applypilot.ai/careers/fullstack-dev",
                description="Design and implement interactive dashboards using Tailwind, Clerk authentication, and FastAPI SQLAlchemy async backend pools.",
                is_active=True,
                salary_min=120000,
                salary_max=160000,
                salary_currency="USD",
                required_skills=["Python", "FastAPI", "Next.js", "React", "Clerk", "PostgreSQL"],
                role_competitiveness=65,
                estimated_applicants=38,
            )
        ]
        
        for job in jobs_to_seed:
            db.add(job)
        await db.commit()
        
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
    
    # Fetch user profile and skills for dynamic matching
    profile_stmt = select(Profile).where(Profile.user_id == user.id)
    profile_result = await db.execute(profile_stmt)
    profile = profile_result.scalars().first()
    
    user_skills = set()
    user_location = "remote"
    if profile:
        skills_stmt = select(ProfileSkill).where(ProfileSkill.profile_id == profile.id)
        skills_res = await db.execute(skills_stmt)
        user_skills = {s.skill_name.lower() for s in skills_res.scalars().all()}
        user_location = (profile.remote_preference or "remote").lower()

    data = []
    for j in jobs:
        # 1. Match score calculation based on skills overlap
        job_skills = [s.lower() for s in j.required_skills]
        matched_skills = [s for s in job_skills if s in user_skills]
        
        if job_skills:
            skill_overlap_ratio = len(matched_skills) / len(job_skills)
            base_score = int(skill_overlap_ratio * 100)
        else:
            base_score = 75 # Default score if no skills requirements specified
            
        # Add some variation based on title and experience
        if profile and profile.headline:
            headline_words = set(profile.headline.lower().split())
            title_words = set(j.title.lower().split())
            if headline_words.intersection(title_words):
                base_score += 10
                
        # Normalize score bounds
        score = min(max(base_score, 45), 98)
        
        # 2. Location filter compatibility check
        # If user has remote preference, give bonus to remote jobs, or check location
        if user_location == "remote" and j.location.lower() == "remote":
            score = min(score + 5, 98)
            
        if min_score and score < min_score:
            continue
            
        # Interview Probability matches score
        interview_prob = int(score * 0.85)
        
        data.append(
            JobSummary(
                id=str(j.id),
                title=j.title,
                company=j.company_name,
                location=j.location,
                source=j.source.value,
                match_score=score,
                interview_probability=interview_prob,
                salary_range=f"${j.salary_min // 1000}k-${j.salary_max // 1000}k" if j.salary_min else "Competitive",
                posted_at="2026-06-12",
            )
        )
        
    # Sort by highest match score
    data.sort(key=lambda x: x.match_score, reverse=True)
        
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
