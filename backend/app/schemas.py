from pydantic import BaseModel, EmailStr, Field, HttpUrl


class AuthMeResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None = None
    onboarding_completed: bool = False


class ProfileResponse(BaseModel):
    id: str
    full_name: str
    headline: str | None = None
    location: str | None = None
    target_roles: list[str] = Field(default_factory=list)
    onboarding_completed: bool = False


class ResumeUploadResponse(BaseModel):
    filename: str
    content_type: str | None = None
    parsed_status: str = "queued"
    message: str


class JobSummary(BaseModel):
    id: str
    title: str
    company: str
    location: str | None = None
    source: str
    match_score: int = Field(ge=0, le=100)
    interview_probability: int = Field(ge=0, le=100)
    salary_range: str | None = None
    posted_at: str | None = None


class JobListResponse(BaseModel):
    data: list[JobSummary]
    meta: dict[str, int | bool]


class DiscoverJobsResponse(BaseModel):
    task_id: str
    status: str = "queued"
    message: str


class ImportJobRequest(BaseModel):
    url: HttpUrl


class MatchSummary(BaseModel):
    job_id: str
    job_title: str
    company: str
    match_score: int = Field(ge=0, le=100)
    interview_probability: int = Field(ge=0, le=100)
    gap_summary: list[str] = Field(default_factory=list)


class MatchListResponse(BaseModel):
    data: list[MatchSummary]
    min_score: int


class ApplicationSummary(BaseModel):
    id: str
    job_id: str
    job_title: str
    company: str
    status: str
    ats_score: int = Field(ge=0, le=100)
    updated_at: str | None = None


class ApplicationsResponse(BaseModel):
    data: list[ApplicationSummary]


class GenerateApplicationRequest(BaseModel):
    job_id: str
    include_outreach: bool = True


class GenerateApplicationResponse(BaseModel):
    application_id: str
    task_id: str
    status: str
    message: str


class ApprovalResponse(BaseModel):
    application_id: str
    status: str


# --- Auth schemas ---
class SignupRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
