import enum
from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    Date,
    Text,
    Integer,
    Numeric,
    ForeignKey,
    Enum as SQLEnum,
    UniqueConstraint,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY, INET
from sqlalchemy.orm import relationship as sa_relationship, declarative_base

Base = declarative_base()

# ─── ENUMS ───────────────────────────────────────────────────────────

class SubscriptionTier(str, enum.Enum):
    free = "free"
    pro = "pro"
    teams = "teams"
    enterprise = "enterprise"


class SubscriptionStatus(str, enum.Enum):
    active = "active"
    past_due = "past_due"
    canceled = "canceled"
    trialing = "trialing"


class JobSource(str, enum.Enum):
    linkedin = "linkedin"
    wellfound = "wellfound"
    naukri = "naukri"
    instahyre = "instahyre"
    career_page = "career_page"
    ycombinator = "ycombinator"
    remoteok = "remoteok"
    indeed = "indeed"
    manual = "manual"


class ApplicationStatus(str, enum.Enum):
    draft = "draft"
    pending_review = "pending_review"
    approved = "approved"
    submitted = "submitted"
    oa = "oa"
    interview = "interview"
    rejected = "rejected"
    offer = "offer"
    withdrawn = "withdrawn"


class ApprovalAction(str, enum.Enum):
    approve = "approve"
    reject = "reject"
    edit = "edit"
    request_regeneration = "request_regeneration"


class AgentType(str, enum.Enum):
    job_finder = "job_finder"
    resume_optimizer = "resume_optimizer"
    cover_letter = "cover_letter"
    recruiter_outreach = "recruiter_outreach"
    application_tracker = "application_tracker"
    interview_coach = "interview_coach"
    market_intelligence = "market_intelligence"


class OutreachChannel(str, enum.Enum):
    linkedin_dm = "linkedin_dm"
    email = "email"
    follow_up = "follow_up"
    referral_request = "referral_request"


class CompanyFundingStage(str, enum.Enum):
    pre_seed = "pre_seed"
    seed = "seed"
    series_a = "series_a"
    series_b = "series_b"
    series_c = "series_c"
    growth = "growth"
    public = "public"
    bootstrapped = "bootstrapped"
    unknown = "unknown"


# ─── USERS & AUTH ────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    clerk_id = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    avatar_url = Column(Text, nullable=True)
    timezone = Column(String(50), default="UTC")
    onboarding_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subscription = sa_relationship("Subscription", back_populates="user", uselist=False, cascade="all, delete-orphan")
    usage_quotas = sa_relationship("UsageQuota", back_populates="user", cascade="all, delete-orphan")
    profile = sa_relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    job_preference = sa_relationship("JobPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    match_results = sa_relationship("MatchResult", back_populates="user", cascade="all, delete-orphan")
    applications = sa_relationship("Application", back_populates="user", cascade="all, delete-orphan")
    approval_requests = sa_relationship("ApprovalRequest", back_populates="user", cascade="all, delete-orphan")
    approval_audit_logs = sa_relationship("ApprovalAuditLog", back_populates="user", cascade="all, delete-orphan")
    outreach_messages = sa_relationship("OutreachMessage", back_populates="user", cascade="all, delete-orphan")
    network_contacts = sa_relationship("NetworkContact", back_populates="user", cascade="all, delete-orphan")
    interview_sessions = sa_relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")
    agent_runs = sa_relationship("AgentRun", back_populates="user", cascade="all, delete-orphan")
    market_reports = sa_relationship("MarketReport", back_populates="user", cascade="all, delete-orphan")
    audit_events = sa_relationship("AuditEvent", back_populates="user", cascade="all, delete-orphan")


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    stripe_customer_id = Column(String(255), unique=True, nullable=True)
    stripe_subscription_id = Column(String(255), unique=True, nullable=True)
    tier = Column(SQLEnum(SubscriptionTier), default=SubscriptionTier.free)
    status = Column(SQLEnum(SubscriptionStatus), default=SubscriptionStatus.active)
    current_period_start = Column(DateTime(timezone=True), nullable=True)
    current_period_end = Column(DateTime(timezone=True), nullable=True)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = sa_relationship("User", back_populates="subscription")


class UsageQuota(Base):
    __tablename__ = "usage_quotas"
    __table_args__ = (UniqueConstraint("user_id", "period_start", name="uq_user_period"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    jobs_analyzed = Column(Integer, default=0)
    applications_generated = Column(Integer, default=0)
    llm_tokens_used = Column(Integer, default=0)

    # Relationships
    user = sa_relationship("User", back_populates="usage_quotas")


# ─── USER PROFILES ───────────────────────────────────────────────────

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    headline = Column(String(500), nullable=True)
    summary = Column(Text, nullable=True)
    years_experience = Column(Numeric(4, 1), nullable=True)
    current_title = Column(String(255), nullable=True)
    current_company = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    willing_to_relocate = Column(Boolean, default=False)
    remote_preference = Column(String(50), default="hybrid")  # remote, hybrid, onsite, any
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(3), default="USD")
    linkedin_url = Column(Text, nullable=True)
    portfolio_url = Column(Text, nullable=True)
    github_url = Column(Text, nullable=True)
    raw_resume_text = Column(Text, nullable=True)
    resume_s3_key = Column(Text, nullable=True)
    embedding_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = sa_relationship("User", back_populates="profile")
    skills = sa_relationship("ProfileSkill", back_populates="profile", cascade="all, delete-orphan")
    experiences = sa_relationship("ProfileExperience", back_populates="profile", cascade="all, delete-orphan")
    education = sa_relationship("ProfileEducation", back_populates="profile", cascade="all, delete-orphan")
    projects = sa_relationship("ProfileProject", back_populates="profile", cascade="all, delete-orphan")


class ProfileSkill(Base):
    __tablename__ = "profile_skills"
    __table_args__ = (UniqueConstraint("profile_id", "skill_name", name="uq_profile_skill"),)

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    proficiency = Column(String(20), default="intermediate")  # beginner, intermediate, advanced, expert
    years_used = Column(Numeric(3, 1), nullable=True)
    is_primary = Column(Boolean, default=False)

    # Relationships
    profile = sa_relationship("Profile", back_populates="skills")


class ProfileExperience(Base):
    __tablename__ = "profile_experiences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    company = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    location = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)  # Null indicates present
    is_current = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    achievements = Column(JSONB, default=list)  # JSONB array of strings
    technologies = Column(ARRAY(String), default=list)
    display_order = Column(Integer, default=0)

    # Relationships
    profile = sa_relationship("Profile", back_populates="experiences")


class ProfileEducation(Base):
    __tablename__ = "profile_education"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=True)
    field_of_study = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    gpa = Column(Numeric(3, 2), nullable=True)
    display_order = Column(Integer, default=0)

    # Relationships
    profile = sa_relationship("Profile", back_populates="education")


class ProfileProject(Base):
    __tablename__ = "profile_projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(Text, nullable=True)
    technologies = Column(ARRAY(String), default=list)
    highlights = Column(JSONB, default=list)
    display_order = Column(Integer, default=0)

    # Relationships
    profile = sa_relationship("Profile", back_populates="projects")


# ─── JOB PREFERENCES ─────────────────────────────────────────────────

class JobPreference(Base):
    __tablename__ = "job_preferences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    target_titles = Column(ARRAY(String), default=list)
    target_companies = Column(ARRAY(String), default=list)
    excluded_companies = Column(ARRAY(String), default=list)
    locations = Column(ARRAY(String), default=list)
    remote_only = Column(Boolean, default=False)
    min_salary = Column(Integer, nullable=True)
    max_salary = Column(Integer, nullable=True)
    experience_levels = Column(ARRAY(String), default=list)
    company_stages = Column(ARRAY(String), default=list)
    enabled_sources = Column(ARRAY(String), default=lambda: ["linkedin", "wellfound", "remoteok"])
    min_match_score = Column(Integer, default=70)
    max_applications_per_week = Column(Integer, default=10)
    keywords_include = Column(ARRAY(String), default=list)
    keywords_exclude = Column(ARRAY(String), default=list)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = sa_relationship("User", back_populates="job_preference")


# ─── COMPANIES ───────────────────────────────────────────────────────

class Company(Base):
    __tablename__ = "companies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=True)
    domain = Column(String(255), nullable=True)
    logo_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    industry = Column(String(100), nullable=True)
    employee_count = Column(Integer, nullable=True)
    employee_range = Column(String(50), nullable=True)
    funding_stage = Column(SQLEnum(CompanyFundingStage), default=CompanyFundingStage.unknown)
    total_funding = Column(Integer, nullable=True)
    founded_year = Column(Integer, nullable=True)
    headquarters = Column(String(255), nullable=True)
    linkedin_url = Column(Text, nullable=True)
    careers_page_url = Column(Text, nullable=True)
    health_score = Column(Integer, nullable=True)
    hiring_velocity = Column(Integer, nullable=True)
    glassdoor_rating = Column(Numeric(2, 1), nullable=True)
    company_metadata = Column("metadata", JSONB, default=dict)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    jobs = sa_relationship("Job", back_populates="company")
    network_contacts = sa_relationship("NetworkContact", back_populates="company")


# ─── JOBS ────────────────────────────────────────────────────────────

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    external_id = Column(String(255), nullable=True)
    source = Column(SQLEnum(JobSource), nullable=False)
    source_url = Column(Text, nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    company_name = Column(String(255), nullable=False)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    description_html = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    is_remote = Column(Boolean, default=False)
    employment_type = Column(String(50), nullable=True)
    experience_level = Column(String(50), nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    salary_currency = Column(String(3), default="USD")
    posted_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)
    required_skills = Column(ARRAY(String), default=list)
    preferred_skills = Column(ARRAY(String), default=list)
    responsibilities = Column(JSONB, default=list)
    hidden_requirements = Column(JSONB, default=list)
    keywords = Column(ARRAY(String), default=list)
    parsed_metadata = Column(JSONB, default=dict)
    embedding_id = Column(String(255), nullable=True)
    role_competitiveness = Column(Integer, nullable=True)
    estimated_applicants = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraints / Args
    __table_args__ = (UniqueConstraint("source", "external_id", name="uq_job_source_external"),)

    # Relationships
    company = sa_relationship("Company", back_populates="jobs")
    analyses = sa_relationship("JobAnalysis", back_populates="job", cascade="all, delete-orphan")
    match_results = sa_relationship("MatchResult", back_populates="job", cascade="all, delete-orphan")
    applications = sa_relationship("Application", back_populates="job")


class JobAnalysis(Base):
    __tablename__ = "job_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    model_used = Column(String(100), nullable=False)
    prompt_version = Column(String(20), nullable=False)
    extracted_skills = Column(JSONB, nullable=False)
    experience_requirements = Column(JSONB, nullable=False)
    responsibilities = Column(JSONB, nullable=False)
    hidden_requirements = Column(JSONB, default=list)
    company_type = Column(String(100), nullable=True)
    seniority_signals = Column(JSONB, default=dict)
    red_flags = Column(JSONB, default=list)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    job = sa_relationship("Job", back_populates="analyses")


# ─── MATCH RESULTS ───────────────────────────────────────────────────

class MatchResult(Base):
    __tablename__ = "match_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    match_score = Column(Integer, nullable=False)
    skill_match = Column(JSONB, nullable=False)  # e.g., {matched: [], missing: [], transferable: []}
    gap_analysis = Column(JSONB, nullable=False)
    interview_probability = Column(JSONB, nullable=False)  # e.g., {shortlist: 0.8, oa: 0.5, interview: 0.3}
    recommendation = Column(String(50), nullable=True)  # strong_apply, apply, consider, skip
    reasoning = Column(Text, nullable=True)
    is_bookmarked = Column(Boolean, default=False)
    is_dismissed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Constraints / Args
    __table_args__ = (
        CheckConstraint("match_score >= 0 AND match_score <= 100", name="chk_match_score_range"),
        UniqueConstraint("user_id", "job_id", name="uq_user_job_match"),
    )

    # Relationships
    user = sa_relationship("User", back_populates="match_results")
    job = sa_relationship("Job", back_populates="match_results")
    applications = sa_relationship("Application", back_populates="match_result")


# ─── APPLICATIONS ────────────────────────────────────────────────────

class Application(Base):
    __tablename__ = "applications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"), nullable=False)
    match_result_id = Column(UUID(as_uuid=True), ForeignKey("match_results.id"), nullable=True)
    status = Column(SQLEnum(ApplicationStatus), default=ApplicationStatus.draft)
    tailored_resume_s3_key = Column(Text, nullable=True)
    tailored_resume_text = Column(Text, nullable=True)
    cover_letter_text = Column(Text, nullable=True)
    ats_score = Column(Integer, nullable=True)
    keyword_coverage = Column(JSONB, nullable=True)
    applied_at = Column(DateTime(timezone=True), nullable=True)
    submitted_url = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = sa_relationship("User", back_populates="applications")
    job = sa_relationship("Job", back_populates="applications")
    match_result = sa_relationship("MatchResult", back_populates="applications")
    approval_requests = sa_relationship("ApprovalRequest", back_populates="application", cascade="all, delete-orphan")
    approval_audit_logs = sa_relationship("ApprovalAuditLog", back_populates="application", cascade="all, delete-orphan")
    outreach_messages = sa_relationship("OutreachMessage", back_populates="application", cascade="all, delete-orphan")
    interview_sessions = sa_relationship("InterviewSession", back_populates="application")


# ─── APPROVAL WORKFLOW ───────────────────────────────────────────────

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    status = Column(String(50), default="pending")  # pending, approved, rejected
    reviewer_notes = Column(Text, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    application = sa_relationship("Application", back_populates="approval_requests")
    user = sa_relationship("User", back_populates="approval_requests")
    audit_logs = sa_relationship("ApprovalAuditLog", back_populates="approval_request")


class ApprovalAuditLog(Base):
    __tablename__ = "approval_audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    approval_request_id = Column(UUID(as_uuid=True), ForeignKey("approval_requests.id"), nullable=True)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(SQLEnum(ApprovalAction), nullable=False)
    previous_status = Column(SQLEnum(ApplicationStatus), nullable=True)
    new_status = Column(SQLEnum(ApplicationStatus), nullable=True)
    changes = Column(JSONB, nullable=True)  # Diff of fields edited
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    approval_request = sa_relationship("ApprovalRequest", back_populates="audit_logs")
    application = sa_relationship("Application", back_populates="approval_audit_logs")
    user = sa_relationship("User", back_populates="approval_audit_logs")


# ─── OUTREACH ────────────────────────────────────────────────────────

class OutreachMessage(Base):
    __tablename__ = "outreach_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    channel = Column(SQLEnum(OutreachChannel), nullable=False)
    recipient_name = Column(String(255), nullable=True)
    recipient_title = Column(String(255), nullable=True)
    recipient_linkedin = Column(Text, nullable=True)
    recipient_email = Column(Text, nullable=True)
    subject = Column(String(500), nullable=True)
    body = Column(Text, nullable=False)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    application = sa_relationship("Application", back_populates="outreach_messages")
    user = sa_relationship("User", back_populates="outreach_messages")


# ─── NETWORKING CONTACTS ─────────────────────────────────────────────

class NetworkContact(Base):
    __tablename__ = "network_contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=True)
    full_name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=True)
    linkedin_url = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    relationship = Column(String(50), nullable=True)  # recruiter, hiring_manager, employee, alumni
    connection_strength = Column(Integer, default=0)
    notes = Column(Text, nullable=True)
    last_contacted = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user = sa_relationship("User", back_populates="network_contacts")
    company = sa_relationship("Company", back_populates="network_contacts")


# ─── INTERVIEW PREP ──────────────────────────────────────────────────

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    application_id = Column(UUID(as_uuid=True), ForeignKey("applications.id"), nullable=True)
    session_type = Column(String(50), nullable=True)  # behavioral, technical, system_design
    questions = Column(JSONB, nullable=False)
    user_answers = Column(JSONB, default=list)
    ai_feedback = Column(JSONB, nullable=True)
    score = Column(Integer, nullable=True)
    duration_seconds = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user = sa_relationship("User", back_populates="interview_sessions")
    application = sa_relationship("Application", back_populates="interview_sessions")


# ─── AI AGENT RUNS ───────────────────────────────────────────────────

class AgentRun(Base):
    __tablename__ = "agent_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    agent_type = Column(SQLEnum(AgentType), nullable=False)
    status = Column(String(50), default="running")  # running, completed, failed
    input_payload = Column(JSONB, nullable=False)
    output_payload = Column(JSONB, nullable=True)
    model_used = Column(String(100), nullable=True)
    prompt_version = Column(String(20), nullable=True)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    cost_usd = Column(Numeric(10, 6), nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    celery_task_id = Column(String(255), nullable=True)

    # Relationships
    user = sa_relationship("User", back_populates="agent_runs")


# ─── PROMPT REGISTRY ─────────────────────────────────────────────────

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    agent_type = Column(SQLEnum(AgentType), nullable=False)
    template = Column(Text, nullable=False)
    variables = Column(JSONB, default=list)  # Expected variables
    model_config = Column(JSONB, default=dict)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Constraints / Args
    __table_args__ = (UniqueConstraint("name", "version", name="uq_prompt_name_version"),)


# ─── MARKET INTELLIGENCE ─────────────────────────────────────────────

class MarketReport(Base):
    __tablename__ = "market_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    report_type = Column(String(50), nullable=True)  # role_market, salary, company
    target_role = Column(String(255), nullable=True)
    target_location = Column(String(255), nullable=True)
    content = Column(JSONB, nullable=False)
    generated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user = sa_relationship("User", back_populates="market_reports")


# ─── AUDIT & COMPLIANCE ──────────────────────────────────────────────

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    event_type = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=True)
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    audit_metadata = Column("metadata", JSONB, default=dict)
    ip_address = Column(INET, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    user = sa_relationship("User", back_populates="audit_events")
