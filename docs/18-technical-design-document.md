# ApplyPilot AI — Technical Design Document (TDD)

**Version:** 1.0 | **Status:** Implementation Ready

---

## 1. System Context

ApplyPilot AI is a full-stack SaaS platform comprising:
- **Frontend:** Next.js 15 (App Router) deployed on Vercel
- **Backend:** FastAPI deployed on Railway with Celery workers
- **Data:** PostgreSQL + Redis + Pinecone + Cloudflare R2
- **AI:** Multi-provider LLM routing (OpenAI, Anthropic, Google)
- **Auth:** Clerk (JWT verification on backend)
- **Payments:** Stripe (subscriptions + webhooks)

Refer to [System Architecture](01-system-architecture.md) for diagrams.

---

## 2. Backend Architecture

### 2.1 FastAPI Application Structure

```python
# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.audit import AuditMiddleware
from app.config import settings

app = FastAPI(
    title="ApplyPilot AI API",
    version="1.0.0",
    docs_url="/docs" if settings.APP_ENV != "production" else None,
)

app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, ...)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuditMiddleware)

app.include_router(api_router, prefix="/v1")

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
```

### 2.2 Dependency Injection

```python
# backend/app/dependencies.py

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    return await auth_middleware.verify_and_load_user(request, db)

async def require_quota(
    action: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    await quota_service.check_and_increment(user.id, action, db)
```

### 2.3 Service Layer Pattern

```python
# backend/app/services/application_service.py

class ApplicationService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def generate_pack(
        self, user_id: UUID, job_id: UUID, include_outreach: bool = True
    ) -> Application:
        # 1. Validate quota
        await quota_service.check(user_id, "applications_generated")
        
        # 2. Verify match exists and meets threshold
        match = await match_repo.get(user_id, job_id)
        if not match or match.match_score < preferences.min_match_score:
            raise BadRequestError("Job does not meet match threshold")
        
        # 3. Create application in DRAFT state
        application = await app_repo.create(user_id, job_id, status="draft")
        
        # 4. Queue parallel Celery tasks
        task_group = group(
            generate_resume.s(str(application.id)),
            generate_cover_letter.s(str(application.id)),
            generate_outreach.s(str(application.id)) if include_outreach else noop.s(),
        )
        result = task_group.apply_async()
        
        # 5. Update status to pending_review when all complete (callback)
        application.task_id = result.id
        await app_repo.update(application)
        
        return application
```

---

## 3. Celery Task Design

### 3.1 Queue Configuration

```python
# backend/app/workers/celery_app.py

celery_app = Celery("applypilot")
celery_app.config_from_object({
    "broker_url": settings.REDIS_URL,
    "result_backend": settings.REDIS_URL,
    "task_routes": {
        "app.workers.generation.*": {"queue": "ai_generation"},
        "app.workers.job_ingestion.*": {"queue": "job_ingestion"},
        "app.workers.scheduled.*": {"queue": "critical"},
    },
    "task_acks_late": True,
    "worker_prefetch_multiplier": 1,  # Prevent worker hogging
    "task_time_limit": 300,           # 5 min hard limit
    "task_soft_time_limit": 240,
})
```

### 3.2 Generation Task with Chord

```python
@celery_app.task(bind=True, max_retries=3)
def generate_resume(self, application_id: str):
    app = asyncio.run(application_service.get(application_id))
    profile = asyncio.run(profile_service.get(app.user_id))
    job = asyncio.run(job_service.get(app.job_id))
    
    # RAG retrieval
    chunks = asyncio.run(retriever.retrieve_for_resume_tailoring(
        user_id=app.user_id, job=job, top_k=8
    ))
    
    # LLM generation
    result = asyncio.run(resume_agent.run(
        profile=profile, job=job, relevant_chunks=chunks
    ))
    
    # Validation
    validation = asyncio.run(hallucination_validator.validate(profile, result.text))
    if not validation.passed:
        raise self.retry(countdown=2 ** self.request.retries)
    
    asyncio.run(app_repo.update_resume(application_id, result))
    return {"application_id": application_id, "status": "resume_done"}

@celery_app.task
def finalize_application(results, application_id: str):
    """Chord callback — all generation tasks complete."""
    asyncio.run(app_repo.update_status(application_id, "pending_review"))
    asyncio.run(notification_service.notify_materials_ready(application_id))
```

---

## 4. LLM Router

```python
# backend/app/ai/llm_router.py

class LLMRouter:
    PROVIDERS = {
        "openai": AsyncOpenAI(api_key=settings.OPENAI_API_KEY),
        "anthropic": AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY),
        "google": genai.Client(api_key=settings.GOOGLE_AI_API_KEY),
    }
    
    MODEL_MAP = {
        "gpt-4o-mini": ("openai", "gpt-4o-mini"),
        "gpt-4o": ("openai", "gpt-4o"),
        "claude-3-5-sonnet": ("anthropic", "claude-3-5-sonnet-20241022"),
        "gemini-1.5-pro": ("google", "gemini-1.5-pro"),
    }
    
    async def complete(
        self,
        model: str,
        messages: list[dict],
        response_format: dict | None = None,
        temperature: float = 0.3,
    ) -> LLMResponse:
        provider_name, model_id = self.MODEL_MAP[model]
        
        for attempt in range(3):
            try:
                return await self._call(provider_name, model_id, messages, ...)
            except (RateLimitError, ServiceUnavailableError) as e:
                fallback = FALLBACK_CHAIN.get(model)
                if fallback and attempt < 2:
                    model = fallback
                    continue
                raise
        
    async def _call(self, provider, model, messages, ...) -> LLMResponse:
        start = time.monotonic()
        response = await self.PROVIDERS[provider].messages.create(...)
        
        await agent_run_repo.log(
            model=model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            latency_ms=int((time.monotonic() - start) * 1000),
        )
        return response
```

---

## 5. Frontend Architecture

### 5.1 App Router Structure

```
src/app/
├── (marketing)/          # Public pages (landing, pricing)
├── (auth)/               # Clerk sign-in/up
└── (dashboard)/          # Protected app shell
    ├── layout.tsx        # Sidebar + auth guard
    └── [feature]/page.tsx
```

### 5.2 API Client

```typescript
// frontend/src/lib/api-client.ts

class ApiClient {
  private baseUrl = process.env.NEXT_PUBLIC_API_URL!;
  
  async fetch<T>(path: string, options: RequestInit = {}): Promise<T> {
    const token = await getClerkToken();
    
    const response = await fetch(`${this.baseUrl}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...options.headers,
      },
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new ApiError(response.status, error.message);
    }
    
    return response.json();
  }
  
  // Typed methods
  jobs = {
    list: (params: JobListParams) => this.fetch<PaginatedResponse<Job>>(`/jobs?${qs(params)}`),
    get: (id: string) => this.fetch<JobDetail>(`/jobs/${id}`),
    import: (url: string) => this.fetch<Job>("/jobs/import", { method: "POST", body: JSON.stringify({ url }) }),
  };
  
  applications = {
    generate: (jobId: string) => this.fetch<ApplicationGenerateResponse>("/applications/generate", {
      method: "POST",
      body: JSON.stringify({ job_id: jobId }),
    }),
    approve: (id: string) => this.fetch(`/applications/${id}/approve`, { method: "POST" }),
  };
}

export const api = new ApiClient();
```

### 5.3 Key Component: Approval Panel

```typescript
// frontend/src/components/applications/approval-panel.tsx

export function ApprovalPanel({ application }: { application: ApplicationPack }) {
  const [editedResume, setEditedResume] = useState(application.tailored_resume_text);
  const [editedCoverLetter, setEditedCoverLetter] = useState(application.cover_letter_text);
  
  const approveMutation = useMutation({
    mutationFn: () => api.applications.approve(application.id),
    onSuccess: () => toast.success("Application approved! Copy materials and apply on the job board."),
  });
  
  return (
    <div className="grid grid-cols-2 gap-6">
      <ResumePreview original={profile.resume} tailored={editedResume} onEdit={setEditedResume} />
      <CoverLetterEditor value={editedCoverLetter} onChange={setEditedCoverLetter} />
      <AtsScoreBreakdown score={application.ats_score} coverage={application.keyword_coverage} />
      <OutreachMessages messages={application.outreach_messages} />
      
      <div className="col-span-2 flex gap-4">
        <Button variant="destructive" onClick={() => rejectMutation.mutate()}>Reject & Regenerate</Button>
        <Button onClick={() => approveMutation.mutate()} disabled={application.status !== "pending_review"}>
          Approve Application
        </Button>
      </div>
    </div>
  );
}
```

---

## 6. Database Access Layer

```python
# backend/app/models/application.py

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False, index=True)
    job_id = Column(UUID, ForeignKey("jobs.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT)
    tailored_resume_text = Column(Text)
    cover_letter_text = Column(Text)
    ats_score = Column(Integer)
    keyword_coverage = Column(JSONB)
    
    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job")
    outreach_messages = relationship("OutreachMessage", back_populates="application")

# Repository pattern for complex queries
class ApplicationRepository:
    async def get_with_materials(self, app_id: UUID, user_id: UUID) -> Application | None:
        result = await self.db.execute(
            select(Application)
            .options(joinedload(Application.job), joinedload(Application.outreach_messages))
            .where(Application.id == app_id, Application.user_id == user_id)
        )
        return result.scalar_one_or_none()
```

---

## 7. Job Source Adapter Pattern

```python
# backend/app/integrations/job_sources/base.py

class JobSourceAdapter(ABC):
    source: JobSource
    rate_limit: RateLimit
    
    @abstractmethod
    async def fetch_jobs(self, preferences: JobPreferences) -> list[RawJob]: ...
    
    @abstractmethod
    async def normalize(self, raw: RawJob) -> NormalizedJob: ...
    
    async def fetch_with_circuit_breaker(self, preferences):
        if self.circuit_breaker.is_open(self.source):
            logger.warning(f"Circuit open for {self.source}")
            return []
        
        try:
            jobs = await self.rate_limit.acquire_and_call(self.fetch_jobs, preferences)
            self.circuit_breaker.record_success(self.source)
            return jobs
        except Exception as e:
            self.circuit_breaker.record_failure(self.source)
            raise

# Register all adapters
SOURCE_REGISTRY = {
    JobSource.REMOTEOK: RemoteOKAdapter(),
    JobSource.YCOMBINATOR: YCombinatorAdapter(),
    JobSource.WELLFOUND: WellfoundAdapter(),
    JobSource.INDEED: IndeedAdapter(),
    # ...
}
```

---

## 8. Real-Time Updates (WebSocket)

```python
# Phase 2: WebSocket for generation progress
@router.websocket("/ws/applications/{application_id}")
async def application_progress(websocket: WebSocket, application_id: str, user: User = Depends(ws_auth)):
    await websocket.accept()
    pubsub = redis.pubsub()
    await pubsub.subscribe(f"application:{application_id}")
    
    async for message in pubsub.listen():
        if message["type"] == "message":
            await websocket.send_json(json.loads(message["data"]))
            if json.loads(message["data"]).get("status") == "pending_review":
                break
```

---

## 9. Testing Strategy

```python
# backend/tests/test_application_flow.py

@pytest.mark.asyncio
async def test_generate_application_pack(client, auth_headers, matched_job, mock_llm):
    mock_llm.set_response("resume", SAMPLE_TAILORED_RESUME)
    mock_llm.set_response("cover_letter", SAMPLE_COVER_LETTER)
    
    response = await client.post(
        "/v1/applications/generate",
        json={"job_id": str(matched_job.id)},
        headers=auth_headers,
    )
    assert response.status_code == 202
    
    # Wait for Celery tasks (eager mode in tests)
    application = await get_application(response.json()["application_id"])
    assert application.status == "pending_review"
    assert application.tailored_resume_text is not None
    assert application.ats_score >= 70

@pytest.mark.asyncio
async def test_cannot_submit_without_approval(client, auth_headers, draft_application):
    response = await client.post(
        f"/v1/applications/{draft_application.id}/submit",
        headers=auth_headers,
    )
    assert response.status_code == 403
```

---

## 10. Performance Targets

| Endpoint | p50 | p95 | p99 |
|----------|-----|-----|-----|
| GET /jobs | 50ms | 200ms | 500ms |
| GET /matches | 80ms | 300ms | 600ms |
| POST /applications/generate | 202 immediate | — | — |
| Generation completion | 30s | 60s | 90s |
| GET /applications/{id} | 40ms | 150ms | 300ms |

---

## 11. Migration Plan

1. Run `02-database-schema.sql` via Alembic initial migration
2. Seed prompt templates via `scripts/seed_prompts.py`
3. Seed test data for staging environment
4. Configure Pinecone index via `scripts/setup_pinecone.py`

---

## 12. Monitoring Instrumentation

```python
# Every service method wrapped with tracing
@trace("application_service.generate_pack")
async def generate_pack(self, user_id, job_id):
    with posthog.capture("application_generation_started", {"user_id": str(user_id)}):
        ...

# Custom Sentry context
sentry_sdk.set_context("application", {
    "application_id": str(app.id),
    "job_id": str(app.job_id),
    "match_score": match.match_score,
})
```
