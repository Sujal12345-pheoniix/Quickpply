# ApplyPilot AI — Folder Structure

```
applypilot/
│
├── README.md
├── docker-compose.yml
├── .env.example
├── .github/
│   └── workflows/
│       ├── ci-backend.yml          # pytest, ruff, mypy
│       ├── ci-frontend.yml         # lint, typecheck, build
│       └── deploy.yml              # Railway + Vercel deploy
│
├── docs/                           # Product & engineering deliverables (01-20)
│
├── prompts/                        # Version-controlled prompt templates
│   ├── registry.yaml               # Active prompt versions per agent
│   ├── job_finder/
│   │   ├── v1.0.0/extract_skills.jinja2
│   │   └── v1.0.0/parse_jd.jinja2
│   ├── resume_optimizer/
│   │   ├── v1.0.0/tailor_resume.jinja2
│   │   └── v1.0.0/ats_score.jinja2
│   ├── cover_letter/
│   │   └── v1.0.0/generate.jinja2
│   ├── outreach/
│   │   ├── v1.0.0/linkedin_dm.jinja2
│   │   ├── v1.0.0/email.jinja2
│   │   └── v1.0.0/referral_request.jinja2
│   ├── matching/
│   │   ├── v1.0.0/score_match.jinja2
│   │   └── v1.0.0/gap_analysis.jinja2
│   └── interview_coach/
│       └── v1.0.0/mock_interview.jinja2
│
├── frontend/                       # Next.js 15 App Router
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.ts
│   ├── components.json             # ShadCN config
│   ├── public/
│   │   └── assets/
│   └── src/
│       ├── app/
│       │   ├── layout.tsx
│       │   ├── page.tsx                    # Landing page
│       │   ├── (auth)/
│       │   │   ├── sign-in/[[...sign-in]]/page.tsx
│       │   │   └── sign-up/[[...sign-up]]/page.tsx
│       │   ├── (dashboard)/
│       │   │   ├── layout.tsx              # Sidebar + nav
│       │   │   ├── dashboard/page.tsx
│       │   │   ├── jobs/
│       │   │   │   ├── page.tsx            # Job feed + filters
│       │   │   │   └── [id]/page.tsx        # Job detail + match score
│       │   │   ├── applications/
│       │   │   │   ├── page.tsx            # Kanban tracker
│       │   │   │   └── [id]/
│       │   │   │       ├── page.tsx        # Application detail
│       │   │   │       └── review/page.tsx # Approval workflow
│       │   │   ├── profile/page.tsx
│       │   │   ├── outreach/page.tsx
│       │   │   ├── interview/page.tsx
│       │   │   ├── analytics/page.tsx
│       │   │   └── settings/
│       │   │       ├── page.tsx
│       │   │       └── billing/page.tsx
│       │   └── api/
│       │       └── webhooks/
│       │           ├── clerk/route.ts
│       │           └── stripe/route.ts
│       ├── components/
│       │   ├── ui/                         # ShadCN primitives
│       │   ├── layout/
│       │   │   ├── sidebar.tsx
│       │   │   └── header.tsx
│       │   ├── jobs/
│       │   │   ├── job-card.tsx
│       │   │   ├── match-score-badge.tsx
│       │   │   └── gap-analysis-panel.tsx
│       │   ├── applications/
│       │   │   ├── kanban-board.tsx
│       │   │   ├── approval-panel.tsx
│       │   │   └── resume-preview.tsx
│       │   └── shared/
│       │       ├── loading-skeleton.tsx
│       │       └── empty-state.tsx
│       ├── lib/
│       │   ├── api-client.ts               # Typed fetch wrapper
│       │   ├── utils.ts
│       │   └── constants.ts
│       ├── hooks/
│       │   ├── use-jobs.ts
│       │   ├── use-applications.ts
│       │   └── use-profile.ts
│       └── types/
│           ├── job.ts
│           ├── application.ts
│           └── profile.ts
│
├── backend/                        # FastAPI
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/
│   └── app/
│       ├── __init__.py
│       ├── main.py                         # FastAPI app entry
│       ├── config.py                       # Pydantic Settings
│       ├── dependencies.py                 # Auth, DB session deps
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   ├── router.py                   # Mount all v1 routes
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── auth.py
│       │       ├── profiles.py
│       │       ├── jobs.py
│       │       ├── matches.py
│       │       ├── applications.py
│       │       ├── approvals.py
│       │       ├── outreach.py
│       │       ├── interviews.py
│       │       ├── analytics.py
│       │       ├── subscriptions.py
│       │       └── webhooks.py
│       │
│       ├── models/                         # SQLAlchemy ORM
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── user.py
│       │   ├── profile.py
│       │   ├── job.py
│       │   ├── application.py
│       │   └── agent_run.py
│       │
│       ├── schemas/                        # Pydantic request/response
│       │   ├── __init__.py
│       │   ├── profile.py
│       │   ├── job.py
│       │   ├── match.py
│       │   ├── application.py
│       │   └── common.py
│       │
│       ├── services/                       # Business logic
│       │   ├── __init__.py
│       │   ├── profile_service.py
│       │   ├── job_service.py
│       │   ├── matching_service.py
│       │   ├── application_service.py
│       │   ├── approval_service.py
│       │   ├── subscription_service.py
│       │   └── quota_service.py
│       │
│       ├── agents/                         # AI Agent implementations
│       │   ├── __init__.py
│       │   ├── orchestrator.py             # LangGraph state machine
│       │   ├── base_agent.py
│       │   ├── job_finder.py
│       │   ├── resume_optimizer.py
│       │   ├── cover_letter.py
│       │   ├── recruiter_outreach.py
│       │   ├── application_tracker.py
│       │   ├── interview_coach.py
│       │   └── market_intelligence.py
│       │
│       ├── ai/                             # LLM infrastructure
│       │   ├── __init__.py
│       │   ├── llm_router.py               # Multi-provider routing
│       │   ├── prompt_manager.py           # Load & render Jinja2 prompts
│       │   ├── rag/
│       │   │   ├── __init__.py
│       │   │   ├── embeddings.py
│       │   │   ├── retriever.py
│       │   │   └── indexer.py
│       │   └── output_parser.py            # Structured JSON extraction
│       │
│       ├── integrations/                   # External APIs
│       │   ├── __init__.py
│       │   ├── job_sources/
│       │   │   ├── base.py
│       │   │   ├── linkedin.py
│       │   │   ├── wellfound.py
│       │   │   ├── remoteok.py
│       │   │   ├── indeed.py
│       │   │   ├── naukri.py
│       │   │   ├── instahyre.py
│       │   │   ├── ycombinator.py
│       │   │   └── career_page_scraper.py
│       │   ├── stripe_client.py
│       │   ├── clerk_client.py
│       │   └── pinecone_client.py
│       │
│       ├── workers/                        # Celery async tasks
│       │   ├── __init__.py
│       │   ├── celery_app.py
│       │   ├── job_ingestion.py
│       │   ├── matching.py
│       │   ├── generation.py
│       │   └── scheduled.py
│       │
│       ├── middleware/
│       │   ├── auth.py
│       │   ├── rate_limit.py
│       │   └── audit.py
│       │
│       └── utils/
│           ├── resume_parser.py            # PDF/DOCX parsing
│           ├── ats_analyzer.py
│           └── text_utils.py
│
├── infra/
│   ├── railway/
│   │   ├── railway.toml
│   │   └── Dockerfile
│   ├── vercel/
│   │   └── vercel.json
│   └── scripts/
│       ├── seed_prompts.py
│       └── migrate.sh
│
└── scripts/
    ├── dev-setup.sh
    └── generate-openapi.sh
```

## Naming Conventions

| Layer | Convention | Example |
|-------|------------|---------|
| API routes | kebab-case plural | `/api/v1/job-preferences` |
| Python modules | snake_case | `matching_service.py` |
| React components | PascalCase | `MatchScoreBadge.tsx` |
| DB tables | snake_case plural | `match_results` |
| Celery tasks | snake_case verb | `generate_application_pack` |
| Prompt files | snake_case.jinja2 | `tailor_resume.jinja2` |
| Env vars | SCREAMING_SNAKE | `PINECONE_API_KEY` |

## Module Dependency Rules

```
api/ → services/ → agents/ → ai/
                 → models/
                 → integrations/

agents/ MUST NOT import from api/
services/ MUST NOT import from agents/ directly (use Celery tasks)
frontend/ communicates ONLY via REST API (no direct DB access)
```
