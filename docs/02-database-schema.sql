-- ApplyPilot AI — PostgreSQL Schema
-- Version: 1.0 | PostgreSQL 16+
-- Run: psql -U applypilot -d applypilot -f 02-database-schema.sql

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";      -- Fuzzy text search
CREATE EXTENSION IF NOT EXISTS "vector";       -- pgvector fallback

-- ─── ENUMS ───────────────────────────────────────────────────────────

CREATE TYPE subscription_tier AS ENUM ('free', 'pro', 'teams', 'enterprise');
CREATE TYPE subscription_status AS ENUM ('active', 'past_due', 'canceled', 'trialing');
CREATE TYPE job_source AS ENUM (
    'linkedin', 'wellfound', 'naukri', 'instahyre',
    'career_page', 'ycombinator', 'remoteok', 'indeed', 'manual'
);
CREATE TYPE application_status AS ENUM (
    'draft', 'pending_review', 'approved', 'submitted',
    'oa', 'interview', 'rejected', 'offer', 'withdrawn'
);
CREATE TYPE approval_action AS ENUM ('approve', 'reject', 'edit', 'request_regeneration');
CREATE TYPE agent_type AS ENUM (
    'job_finder', 'resume_optimizer', 'cover_letter',
    'recruiter_outreach', 'application_tracker',
    'interview_coach', 'market_intelligence'
);
CREATE TYPE outreach_channel AS ENUM ('linkedin_dm', 'email', 'follow_up', 'referral_request');
CREATE TYPE company_funding_stage AS ENUM (
    'pre_seed', 'seed', 'series_a', 'series_b', 'series_c',
    'growth', 'public', 'bootstrapped', 'unknown'
);

-- ─── USERS & AUTH ────────────────────────────────────────────────────

CREATE TABLE users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clerk_id        VARCHAR(255) UNIQUE NOT NULL,
    email           VARCHAR(255) UNIQUE NOT NULL,
    full_name       VARCHAR(255),
    avatar_url      TEXT,
    timezone        VARCHAR(50) DEFAULT 'UTC',
    onboarding_completed BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE subscriptions (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    stripe_customer_id  VARCHAR(255) UNIQUE,
    stripe_subscription_id VARCHAR(255) UNIQUE,
    tier                subscription_tier DEFAULT 'free',
    status              subscription_status DEFAULT 'active',
    current_period_start TIMESTAMPTZ,
    current_period_end   TIMESTAMPTZ,
    cancel_at_period_end BOOLEAN DEFAULT FALSE,
    created_at          TIMESTAMPTZ DEFAULT NOW(),
    updated_at          TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE usage_quotas (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    period_start    DATE NOT NULL,
    period_end      DATE NOT NULL,
    jobs_analyzed   INT DEFAULT 0,
    applications_generated INT DEFAULT 0,
    llm_tokens_used BIGINT DEFAULT 0,
    UNIQUE(user_id, period_start)
);

-- ─── USER PROFILES ───────────────────────────────────────────────────

CREATE TABLE profiles (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    headline        VARCHAR(500),
    summary         TEXT,
    years_experience NUMERIC(4,1),
    current_title   VARCHAR(255),
    current_company VARCHAR(255),
    location        VARCHAR(255),
    willing_to_relocate BOOLEAN DEFAULT FALSE,
    remote_preference VARCHAR(50) DEFAULT 'hybrid', -- remote, hybrid, onsite, any
    salary_min      INT,
    salary_max      INT,
    salary_currency VARCHAR(3) DEFAULT 'USD',
    linkedin_url    TEXT,
    portfolio_url   TEXT,
    github_url      TEXT,
    raw_resume_text TEXT,                    -- Parsed source of truth
    resume_s3_key   TEXT,                    -- Original PDF/DOCX
    embedding_id    VARCHAR(255),          -- Pinecone vector ID
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE profile_skills (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id      UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    skill_name      VARCHAR(100) NOT NULL,
    proficiency     VARCHAR(20) DEFAULT 'intermediate', -- beginner, intermediate, advanced, expert
    years_used      NUMERIC(3,1),
    is_primary      BOOLEAN DEFAULT FALSE,
    UNIQUE(profile_id, skill_name)
);

CREATE TABLE profile_experiences (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id      UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    company         VARCHAR(255) NOT NULL,
    title           VARCHAR(255) NOT NULL,
    location        VARCHAR(255),
    start_date      DATE,
    end_date        DATE,                    -- NULL = present
    is_current      BOOLEAN DEFAULT FALSE,
    description     TEXT,
    achievements    JSONB DEFAULT '[]',      -- ["Increased X by 40%", ...]
    technologies    TEXT[] DEFAULT '{}',
    display_order   INT DEFAULT 0
);

CREATE TABLE profile_education (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id      UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    institution     VARCHAR(255) NOT NULL,
    degree          VARCHAR(255),
    field_of_study  VARCHAR(255),
    start_date      DATE,
    end_date        DATE,
    gpa             NUMERIC(3,2),
    display_order   INT DEFAULT 0
);

CREATE TABLE profile_projects (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id      UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    url             TEXT,
    technologies    TEXT[] DEFAULT '{}',
    highlights      JSONB DEFAULT '[]',
    display_order   INT DEFAULT 0
);

-- ─── JOB PREFERENCES ─────────────────────────────────────────────────

CREATE TABLE job_preferences (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    target_titles   TEXT[] DEFAULT '{}',
    target_companies TEXT[] DEFAULT '{}',
    excluded_companies TEXT[] DEFAULT '{}',
    locations       TEXT[] DEFAULT '{}',
    remote_only     BOOLEAN DEFAULT FALSE,
    min_salary      INT,
    max_salary      INT,
    experience_levels TEXT[] DEFAULT '{}',     -- entry, mid, senior, staff, principal
    company_stages  TEXT[] DEFAULT '{}',
    enabled_sources job_source[] DEFAULT '{linkedin,wellfound,remoteok}',
    min_match_score INT DEFAULT 70,            -- Gate for application generation
    max_applications_per_week INT DEFAULT 10,
    keywords_include TEXT[] DEFAULT '{}',
    keywords_exclude TEXT[] DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── COMPANIES ───────────────────────────────────────────────────────

CREATE TABLE companies (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(255) NOT NULL,
    slug            VARCHAR(255) UNIQUE,
    domain          VARCHAR(255),
    logo_url        TEXT,
    description     TEXT,
    industry        VARCHAR(100),
    employee_count  INT,
    employee_range  VARCHAR(50),             -- "51-200"
    funding_stage   company_funding_stage DEFAULT 'unknown',
    total_funding   BIGINT,                  -- USD cents
    founded_year    INT,
    headquarters    VARCHAR(255),
    linkedin_url    TEXT,
    careers_page_url TEXT,
    -- Intelligence scores (0-100)
    health_score    INT,
    hiring_velocity INT,                     -- Jobs posted last 90 days trend
    glassdoor_rating NUMERIC(2,1),
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_companies_name_trgm ON companies USING gin (name gin_trgm_ops);

-- ─── JOBS ────────────────────────────────────────────────────────────

CREATE TABLE jobs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    external_id     VARCHAR(255),            -- Source-specific ID
    source          job_source NOT NULL,
    source_url      TEXT NOT NULL,
    company_id      UUID REFERENCES companies(id),
    company_name    VARCHAR(255) NOT NULL,     -- Denormalized for speed
    title           VARCHAR(500) NOT NULL,
    description     TEXT NOT NULL,
    description_html TEXT,
    location        VARCHAR(255),
    is_remote       BOOLEAN DEFAULT FALSE,
    employment_type VARCHAR(50),             -- full_time, contract, internship
    experience_level VARCHAR(50),
    salary_min      INT,
    salary_max      INT,
    salary_currency VARCHAR(3) DEFAULT 'USD',
    posted_at       TIMESTAMPTZ,
    expires_at      TIMESTAMPTZ,
    is_active       BOOLEAN DEFAULT TRUE,
    -- Parsed intelligence (LLM extracted)
    required_skills TEXT[] DEFAULT '{}',
    preferred_skills TEXT[] DEFAULT '{}',
    responsibilities JSONB DEFAULT '[]',
    hidden_requirements JSONB DEFAULT '[]',
    keywords        TEXT[] DEFAULT '{}',
    parsed_metadata JSONB DEFAULT '{}',
    embedding_id    VARCHAR(255),            -- Pinecone ID
    -- Scores
    role_competitiveness INT,                -- 0-100
    estimated_applicants INT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(source, external_id)
);

CREATE INDEX idx_jobs_active ON jobs(is_active, posted_at DESC);
CREATE INDEX idx_jobs_company ON jobs(company_id);
CREATE INDEX idx_jobs_title_trgm ON jobs USING gin (title gin_trgm_ops);
CREATE INDEX idx_jobs_skills ON jobs USING gin (required_skills);

-- ─── JOB ANALYSIS ────────────────────────────────────────────────────

CREATE TABLE job_analyses (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    job_id          UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    model_used      VARCHAR(100) NOT NULL,
    prompt_version  VARCHAR(20) NOT NULL,
    extracted_skills JSONB NOT NULL,
    experience_requirements JSONB NOT NULL,
    responsibilities JSONB NOT NULL,
    hidden_requirements JSONB DEFAULT '[]',
    company_type    VARCHAR(100),
    seniority_signals JSONB DEFAULT '{}',
    red_flags       JSONB DEFAULT '[]',
    input_tokens    INT,
    output_tokens   INT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── MATCH RESULTS ───────────────────────────────────────────────────

CREATE TABLE match_results (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id          UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    match_score     INT NOT NULL CHECK (match_score BETWEEN 0 AND 100),
    skill_match     JSONB NOT NULL,          -- {matched: [], missing: [], transferable: []}
    gap_analysis    JSONB NOT NULL,
    interview_probability JSONB NOT NULL,    -- {shortlist: 0.0-1.0, oa: 0.0-1.0, interview: 0.0-1.0}
    recommendation  VARCHAR(50),             -- strong_apply, apply, consider, skip
    reasoning       TEXT,
    is_bookmarked   BOOLEAN DEFAULT FALSE,
    is_dismissed    BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, job_id)
);

CREATE INDEX idx_match_user_score ON match_results(user_id, match_score DESC) WHERE NOT is_dismissed;

-- ─── APPLICATIONS ────────────────────────────────────────────────────

CREATE TABLE applications (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id          UUID NOT NULL REFERENCES jobs(id),
    match_result_id UUID REFERENCES match_results(id),
    status          application_status DEFAULT 'draft',
    -- Generated materials (S3 keys)
    tailored_resume_s3_key TEXT,
    tailored_resume_text TEXT,
    cover_letter_text TEXT,
    ats_score       INT,                     -- 0-100
    keyword_coverage JSONB,                  -- {matched: [], missing: []}
    -- Tracking
    applied_at      TIMESTAMPTZ,
    submitted_url   TEXT,                    -- Where user actually applied
    notes           TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_applications_user_status ON applications(user_id, status);

-- ─── APPROVAL WORKFLOW ───────────────────────────────────────────────

CREATE TABLE approval_requests (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id  UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id),
    status          VARCHAR(50) DEFAULT 'pending', -- pending, approved, rejected
    reviewer_notes  TEXT,
    expires_at      TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days'),
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    resolved_at     TIMESTAMPTZ
);

CREATE TABLE approval_audit_log (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    approval_request_id UUID REFERENCES approval_requests(id),
    application_id  UUID NOT NULL REFERENCES applications(id),
    user_id         UUID NOT NULL REFERENCES users(id),
    action          approval_action NOT NULL,
    previous_status application_status,
    new_status      application_status,
    changes         JSONB,                   -- Diff of edited fields
    ip_address      INET,
    user_agent      TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── OUTREACH ────────────────────────────────────────────────────────

CREATE TABLE outreach_messages (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id  UUID NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
    user_id         UUID NOT NULL REFERENCES users(id),
    channel         outreach_channel NOT NULL,
    recipient_name  VARCHAR(255),
    recipient_title VARCHAR(255),
    recipient_linkedin TEXT,
    recipient_email TEXT,
    subject         VARCHAR(500),            -- For email
    body            TEXT NOT NULL,
    is_sent         BOOLEAN DEFAULT FALSE,
    sent_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── NETWORKING CONTACTS ─────────────────────────────────────────────

CREATE TABLE network_contacts (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_id      UUID REFERENCES companies(id),
    full_name       VARCHAR(255) NOT NULL,
    title           VARCHAR(255),
    linkedin_url    TEXT,
    email           TEXT,
    relationship    VARCHAR(50),             -- recruiter, hiring_manager, employee, alumni
    connection_strength INT DEFAULT 0,       -- 0-100
    notes           TEXT,
    last_contacted  TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── INTERVIEW PREP ──────────────────────────────────────────────────

CREATE TABLE interview_sessions (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    application_id  UUID REFERENCES applications(id),
    session_type    VARCHAR(50),             -- behavioral, technical, system_design
    questions       JSONB NOT NULL,
    user_answers    JSONB DEFAULT '[]',
    ai_feedback     JSONB,
    score           INT,
    duration_seconds INT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ─── AI AGENT RUNS ───────────────────────────────────────────────────

CREATE TABLE agent_runs (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID REFERENCES users(id),
    agent_type      agent_type NOT NULL,
    status          VARCHAR(50) DEFAULT 'running', -- running, completed, failed
    input_payload   JSONB NOT NULL,
    output_payload  JSONB,
    model_used      VARCHAR(100),
    prompt_version  VARCHAR(20),
    input_tokens    INT DEFAULT 0,
    output_tokens   INT DEFAULT 0,
    cost_usd        NUMERIC(10,6),
    error_message   TEXT,
    started_at      TIMESTAMPTZ DEFAULT NOW(),
    completed_at    TIMESTAMPTZ,
    celery_task_id  VARCHAR(255)
);

CREATE INDEX idx_agent_runs_user ON agent_runs(user_id, started_at DESC);

-- ─── PROMPT REGISTRY ─────────────────────────────────────────────────

CREATE TABLE prompt_templates (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            VARCHAR(100) NOT NULL,
    version         VARCHAR(20) NOT NULL,
    agent_type      agent_type NOT NULL,
    template        TEXT NOT NULL,
    variables       JSONB DEFAULT '[]',        -- Expected input variables
    model_config    JSONB DEFAULT '{}',        -- temperature, max_tokens, etc.
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(name, version)
);

-- ─── MARKET INTELLIGENCE ─────────────────────────────────────────────

CREATE TABLE market_reports (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID REFERENCES users(id),
    report_type     VARCHAR(50),             -- role_market, salary, company
    target_role     VARCHAR(255),
    target_location VARCHAR(255),
    content         JSONB NOT NULL,
    generated_at    TIMESTAMPTZ DEFAULT NOW()
);

-- ─── AUDIT & COMPLIANCE ──────────────────────────────────────────────

CREATE TABLE audit_events (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID REFERENCES users(id),
    event_type      VARCHAR(100) NOT NULL,
    resource_type   VARCHAR(100),
    resource_id     UUID,
    metadata        JSONB DEFAULT '{}',
    ip_address      INET,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON audit_events(user_id, created_at DESC);

-- ─── TRIGGERS ────────────────────────────────────────────────────────

CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER profiles_updated_at BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER applications_updated_at BEFORE UPDATE ON applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ─── ROW LEVEL SECURITY (enable in production) ───────────────────────

-- ALTER TABLE applications ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY applications_user_policy ON applications
--     USING (user_id = current_setting('app.current_user_id')::uuid);
