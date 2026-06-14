# ApplyPilot AI — Cursor Implementation Prompts

Copy-paste these prompts into Cursor to implement each module sequentially.

---

## Phase 0: Project Setup

### Prompt 0.1 — Initialize Monorepo
```
Create the ApplyPilot AI monorepo structure:
- backend/ with FastAPI (Python 3.12), SQLAlchemy async, Alembic, Celery
- frontend/ with Next.js 15 App Router, TypeScript, Tailwind CSS, ShadCN UI
- docker-compose.yml with PostgreSQL 16 and Redis 7
- .env.example with all required environment variables
- README.md with setup instructions

Follow the folder structure in docs/03-folder-structure.md exactly.
Use docs/02-database-schema.sql as the database source of truth.
```

### Prompt 0.2 — Backend Foundation
```
Implement the FastAPI backend foundation in backend/app/:

1. config.py - Pydantic Settings loading from env vars
2. main.py - FastAPI app with CORS, health check, router mount
3. dependencies.py - get_db (async SQLAlchemy session), get_current_user (Clerk JWT)
4. models/base.py - SQLAlchemy declarative base with UUID primary keys
5. models/user.py - User model matching docs/02-database-schema.sql
6. middleware/auth.py - Clerk JWT verification
7. api/v1/auth.py - GET /auth/me endpoint
8. api/router.py - Mount all v1 routes

Use async SQLAlchemy with asyncpg. Reference docs/18-technical-design-document.md.
```

### Prompt 0.3 — Frontend Foundation
```
Implement the Next.js frontend foundation:

1. Initialize ShadCN UI with default theme (slate/zinc, professional look)
2. app/layout.tsx - Root layout with ClerkProvider, font, metadata
3. app/page.tsx - Landing page with hero, features grid, pricing, CTA
4. app/(auth)/ - Clerk sign-in and sign-up pages
5. app/(dashboard)/layout.tsx - Protected layout with sidebar navigation
6. components/layout/sidebar.tsx - Nav links: Dashboard, Jobs, Applications, Profile, Settings
7. lib/api-client.ts - Typed fetch wrapper with Clerk token injection
8. lib/constants.ts - API URL, tier limits

Design: Clean, professional, dark sidebar. Tagline: "AI that applies to jobs exactly like a top candidate would."
Reference docs/08-user-flows.md for navigation structure.
```

---

## Phase 1: Profile & Auth

### Prompt 1.1 — Profile Backend
```
Implement profile management backend:

1. models/profile.py - Profile, ProfileSkill, ProfileExperience, ProfileEducation, ProfileProject
2. schemas/profile.py - Pydantic request/response schemas
3. services/profile_service.py - CRUD + resume parsing
4. api/v1/profiles.py - GET/PUT /profiles, POST /profiles/resume (file upload)
5. utils/resume_parser.py - PDF parsing with PyMuPDF, DOCX with python-docx

Resume upload flow: accept PDF/DOCX → parse text → LLM extract structured profile → save to DB.
Use gpt-4o-mini for extraction with structured JSON output.
Include all tables from docs/02-database-schema.sql profiles section.
```

### Prompt 1.2 — Profile Frontend
```
Implement profile management frontend:

1. app/(dashboard)/profile/page.tsx - Profile view/edit page
2. components/profile/resume-upload.tsx - Drag-and-drop upload with parsing progress
3. components/profile/experience-form.tsx - Add/edit experiences with achievements
4. components/profile/skills-editor.tsx - Tag-based skill editor with proficiency
5. components/profile/preferences-form.tsx - Job search preferences
6. hooks/use-profile.ts - React Query hooks for profile CRUD

On resume upload: show parsing spinner → display extracted data → allow edits → save.
Reference docs/08-user-flows.md onboarding flow.
```

---

## Phase 2: Job Intelligence

### Prompt 2.1 — Job Ingestion Pipeline
```
Implement job ingestion pipeline:

1. integrations/job_sources/base.py - Abstract adapter with circuit breaker + rate limiting
2. integrations/job_sources/remoteok.py - RemoteOK JSON API adapter
3. integrations/job_sources/ycombinator.py - YC Work at a Startup adapter
4. services/job_service.py - Normalize, deduplicate, store jobs
5. workers/job_ingestion.py - Celery task for scheduled + manual discovery
6. ai/rag/embeddings.py - OpenAI embedding service with Redis cache
7. ai/rag/indexer.py - Pinecone indexing for jobs

Job normalization: extract title, company, location, description, salary, source_url.
Dedup by (source, external_id) and embedding similarity > 0.92.
Reference docs/05-ai-agent-architecture.md Agent 1 and docs/07-rag-implementation.md.
```

### Prompt 2.2 — JD Analysis & Matching
```
Implement JD analysis and matching engine:

1. agents/job_finder.py - JD parsing agent using prompts/job_finder/v1.0.0/parse_jd.jinja2
2. ai/prompt_manager.py - Jinja2 prompt loader from prompts/ directory
3. services/matching_service.py - Hybrid matching (embedding similarity + LLM scoring)
4. agents/matching/score_match - Use prompts/matching/v1.0.0/score_match.jinja2
5. api/v1/jobs.py - GET /jobs, GET /jobs/{id}, POST /jobs/import, POST /jobs/discover
6. api/v1/matches.py - GET /matches, POST bookmark/dismiss

Create prompt templates from docs/06-prompt-engineering.md.
Matching: Pinecone semantic search → LLM gap analysis → store in match_results table.
Return match_score, skill_match, gap_analysis, interview_probability, recommendation.
```

### Prompt 2.3 — Job Feed Frontend
```
Implement job discovery frontend:

1. app/(dashboard)/jobs/page.tsx - Job feed with filters (score, remote, source)
2. app/(dashboard)/jobs/[id]/page.tsx - Job detail with match analysis
3. components/jobs/job-card.tsx - Title, company, score badge, location, salary
4. components/jobs/match-score-badge.tsx - Color-coded score (green ≥80, yellow ≥60, red <60)
5. components/jobs/gap-analysis-panel.tsx - Matched/missing/transferable skills visualization
6. components/jobs/company-intel-card.tsx - Health score, funding, hiring velocity
7. hooks/use-jobs.ts - React Query hooks with pagination

Job detail page shows: full description, match score, gap analysis, interview probability, company intel.
"Prepare Application" button visible when match_score ≥ user threshold.
Reference docs/04-api-design.yaml for API shapes.
```

---

## Phase 3: Application Generation

### Prompt 3.1 — AI Generation Pipeline
```
Implement application generation pipeline:

1. agents/resume_optimizer.py - RAG-grounded resume tailoring
2. agents/cover_letter.py - Personalized cover letter generation
3. agents/recruiter_outreach.py - LinkedIn DM + email generation
4. ai/rag/retriever.py - Hybrid retriever for profile chunks
5. utils/ats_analyzer.py - Keyword coverage + ATS score computation
6. utils/hallucination_validator.py - Verify output against source profile
7. workers/generation.py - Celery tasks with chord pattern for parallel generation
8. services/application_service.py - Orchestrate generation, manage state machine

Create all prompt templates from docs/06-prompt-engineering.md in prompts/ directory.
State flow: draft → pending_review (NEVER auto-submit).
Anti-hallucination: verify companies, dates, skills exist in original profile.
ATS target: score ≥ 70 or retry up to 3 times.
Reference docs/05-ai-agent-architecture.md Agents 2-4.
```

### Prompt 3.2 — Application Review Frontend
```
Implement application review and approval frontend:

1. app/(dashboard)/applications/page.tsx - Kanban tracker board
2. app/(dashboard)/applications/[id]/review/page.tsx - Review & approval page
3. components/applications/approval-panel.tsx - Side-by-side review with approve/reject
4. components/applications/resume-preview.tsx - Original vs tailored diff view
5. components/applications/ats-score-breakdown.tsx - Score + keyword coverage viz
6. components/applications/kanban-board.tsx - Drag-and-drop pipeline stages
7. hooks/use-applications.ts - React Query hooks

Review page layout:
- Left: Original resume | Right: Tailored resume (editable)
- Below: Cover letter (editable)
- Tab: Outreach messages (LinkedIn DM, email)
- Bottom: ATS score breakdown
- Actions: Reject & Regenerate | Approve

CRITICAL: No "Submit" button that auto-applies. After approve: "Copy Materials" + link to job board.
Reference docs/08-user-flows.md approval gate sequence diagram.
```

---

## Phase 4: Approval & Payments

### Prompt 4.1 — Approval Workflow Backend
```
Implement approval workflow and audit system:

1. services/approval_service.py - State machine: pending_review → approved → submitted
2. api/v1/approvals.py - POST approve, reject, submit endpoints
3. middleware/audit.py - Log all approval actions to approval_audit_log
4. Enforce: submit endpoint returns 403 unless status == approved
5. Enforce: approve endpoint requires authenticated user owns application

State machine rules:
- generate → pending_review
- approve → approved (creates approval_request + audit_log entry)
- reject → draft (optionally triggers regeneration)
- submit → submitted (requires approved, user confirms manual submission)

This is a CRITICAL security requirement. Reference docs/11-security-design.md.
```

### Prompt 4.2 — Stripe Integration
```
Implement Stripe subscription system:

1. services/subscription_service.py - Create checkout, handle webhooks, manage tiers
2. services/quota_service.py - Redis-based usage tracking per tier
3. middleware/rate_limit.py - Enforce tier quotas on generation endpoints
4. api/v1/subscriptions.py - POST checkout, POST portal
5. api/v1/webhooks.py - Stripe webhook handler (checkout.session.completed, subscription.updated/deleted)
6. frontend/app/api/webhooks/stripe/route.ts - Forward to backend

Tier limits from docs/16-monetization-strategy.md:
- Free: 5 apps/mo, 20 jobs/day
- Pro ($29): 50 apps/mo, 200 jobs/day
- Teams ($79): 200 apps/seat/mo

Upgrade modal triggers when quota exceeded. Stripe checkout in 3 clicks.
```

---

## Phase 5: Interview Coach & Analytics

### Prompt 5.1 — Interview Coach
```
Implement interview coach agent:

1. agents/interview_coach.py - Generate role-specific questions, evaluate answers
2. api/v1/interviews.py - POST /sessions, POST /sessions/{id}/answer
3. prompts/interview_coach/v1.0.0/mock_interview.jinja2
4. prompts/interview_coach/v1.0.0/feedback.jinja2
5. frontend/app/(dashboard)/interview/page.tsx - Mock interview UI

Session flow: select type (behavioral/technical/system_design) → 
5-8 questions generated from JD → user answers → AI feedback with STAR analysis → 
session summary with score.

Trigger: available when application status = interview.
Reference docs/05-ai-agent-architecture.md Agent 6.
```

### Prompt 5.2 — Analytics Dashboard
```
Implement analytics dashboard:

1. api/v1/analytics.py - GET /dashboard (stats, pipeline, weekly activity)
2. frontend/app/(dashboard)/analytics/page.tsx - Charts and metrics
3. PostHog event tracking for all key user actions
4. Sentry error tracking setup

Dashboard metrics:
- Total applications, interview rate, avg match score
- Pipeline breakdown (applied, OA, interview, offer, rejected)
- Weekly activity chart
- Top performing job sources

PostHog events: signup, resume_uploaded, job_matched, application_generated,
application_approved, application_submitted, interview_received, upgraded_to_pro.
Reference docs/01-system-architecture.md observability section.
```

---

## Phase 6: Launch Prep

### Prompt 6.1 — Onboarding Wizard
```
Implement onboarding wizard for new users:

1. frontend/components/onboarding/wizard.tsx - 4-step wizard with progress bar
2. Step 1: Upload resume (reuse resume-upload component)
3. Step 2: Review extracted profile (reuse profile components)
4. Step 3: Set job preferences (titles, locations, salary, sources)
5. Step 4: Set match threshold + tour of dashboard
6. Backend: PATCH /auth/me { onboarding_completed: true }

Trigger wizard on first login if onboarding_completed == false.
Target: < 5 minutes from signup to first matched jobs visible.
Reference docs/08-user-flows.md onboarding flow.
```

### Prompt 6.2 — Production Hardening
```
Production hardening pass:

1. Add comprehensive error handling (global exception handler, user-friendly messages)
2. Add request validation on all endpoints (Pydantic schemas)
3. Add rate limiting middleware (Redis sliding window per tier)
4. Add structured logging with PII redaction
5. Add health check endpoints (/health, /health/workers, /health/db)
6. Add database connection pooling (pool_size=20, max_overflow=10)
7. Add Celery task monitoring (flower or custom /health/workers)
8. Frontend: error boundaries, loading skeletons, empty states
9. Frontend: SEO meta tags on landing page
10. Run through docs/11-security-design.md OWASP checklist

Deploy configuration from docs/13-deployment-plan.md.
```

---

## Utility Prompts

### Prompt U.1 — Add New Job Source
```
Add a new job source adapter for {SOURCE_NAME}:

1. Create integrations/job_sources/{source}.py implementing JobSourceAdapter
2. Add to SOURCE_REGISTRY in integrations/job_sources/__init__.py
3. Add source to JobSource enum in models/job.py
4. Write tests with mocked API responses
5. Configure rate limits per docs/05-ai-agent-architecture.md source table

Follow the adapter pattern in integrations/job_sources/base.py.
Handle: fetch → normalize → dedup → store → index to Pinecone.
```

### Prompt U.2 — New Prompt Version
```
Create a new prompt version for {AGENT}/{PROMPT_NAME}:

1. Copy prompts/{agent}/v{current}/ to v{new}/
2. Modify the prompt template
3. Run eval suite: pytest tests/evals/test_{agent}.py
4. Update prompts/registry.yaml to point to new version
5. A/B test on 5% traffic before full promotion

Follow prompt engineering guidelines in docs/06-prompt-engineering.md.
Never remove anti-hallucination constraints.
```

### Prompt U.3 — Debug Agent Failure
```
Debug a failed agent run:

1. Query agent_runs table for the failed run ID
2. Check Sentry for associated error
3. Verify prompt rendered correctly (check input_payload)
4. Check LLM provider status (fallback chain triggered?)
5. Verify RAG retrieval returned relevant chunks
6. Check quota not exceeded
7. Review anti-hallucination validation failure reason

Common fixes:
- Prompt too long → truncate JD input
- Hallucination detected → tighten prompt constraints
- Rate limited → check circuit breaker status
- Timeout → increase task_time_limit or reduce input size
```

---

## Implementation Order

```
Week 1-2:  Prompts 0.1 → 0.2 → 0.3 → 1.1 → 1.2
Week 3-4:  Prompts 2.1 → 2.2 → 2.3
Week 5-6:  Prompts 3.1 → 3.2
Week 7-8:  Prompts 4.1 → 4.2
Week 9-10: Prompts 5.1 → 5.2
Week 11-12: Prompts 6.1 → 6.2
```

Each prompt is designed to be self-contained with references to the docs/ directory for detailed specifications.
