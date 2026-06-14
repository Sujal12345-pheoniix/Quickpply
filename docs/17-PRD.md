# ApplyPilot AI — Product Requirements Document (PRD)

**Version:** 1.0 | **Author:** Product Team | **Status:** Approved for MVP  
**Last Updated:** June 2026

---

## 1. Problem Statement

Job seekers spend 5-10 hours per application tailoring resumes, writing cover letters, and researching companies — yet receive interview rates below 5%. Existing tools either automate low-quality mass applications (damaging candidate reputation) or provide fragmented point solutions (resume builders, job boards, ChatGPT prompts) without an integrated workflow.

**ApplyPilot AI solves this by acting as an AI-powered application strategist that produces human-quality materials with mandatory user approval before any submission.**

---

## 2. Goals & Success Metrics

### Business Goals
1. Achieve 500 beta users within 12 weeks of launch
2. Reach $5K MRR within 6 months
3. Maintain 15%+ interview rate for approved applications
4. Achieve NPS ≥ 40 within 3 months of launch

### User Goals
1. Reduce time per quality application from 2 hours to 15 minutes
2. Increase interview rate from ~3% to 15%+
3. Apply to fewer, better-matched roles (quality over quantity)
4. Maintain full control over what gets submitted

### Key Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| Interview Rate | Interviews / Submitted applications | ≥ 15% |
| Activation Rate | Users who see first match ≥70 within 24h | ≥ 60% |
| Generation Rate | Matches → application packs generated | ≥ 20% |
| Approval Rate | Generated → approved by user | ≥ 70% |
| Submission Rate | Approved → marked submitted | ≥ 80% |
| Free→Pro Conversion | Free users upgrading within 30 days | ≥ 8% |
| D30 Retention | Active users at day 30 | ≥ 40% |

---

## 3. User Personas

### Persona 1: Active Searcher — "Alex"
- **Role:** Senior Software Engineer, 5 YOE
- **Situation:** Laid off, actively searching, 3-month runway
- **Behavior:** Applies to 20-30 roles/month, spends 2hr per application
- **Pain:** Low response rate despite strong background; exhausted by tailoring
- **Goal:** Maximize interviews with minimum time investment
- **Tier:** Pro ($29/mo)

### Persona 2: Passive Explorer — "Priya"
- **Role:** Product Manager, 3 YOE, currently employed
- **Situation:** Open to opportunities but selective
- **Behavior:** Applies to 3-5 dream roles/month
- **Pain:** Hard to find truly matching roles among noise
- **Goal:** Only apply to roles worth the effort
- **Tier:** Free → Pro when active

### Persona 3: Career Coach — "Marcus"
- **Role:** Independent career coach, 20 clients
- **Situation:** Manually helps clients with resumes and applications
- **Behavior:** Creates materials in Google Docs, tracks in spreadsheets
- **Pain:** Can't scale beyond 20 clients
- **Goal:** AI-powered materials generation for all clients
- **Tier:** Teams ($79/seat/mo)

---

## 4. Feature Requirements

### 4.1 Profile Management [P0 — MVP]

**FR-001:** User can upload resume (PDF/DOCX) and system extracts structured profile  
**FR-002:** User can manually edit all profile fields (experience, skills, education, projects)  
**FR-003:** System indexes profile to vector store for RAG retrieval  
**FR-004:** User can set job search preferences (titles, locations, salary, sources, match threshold)

**Acceptance Criteria:**
- Resume parsing accuracy ≥ 90% for standard formats
- Profile editable within 3 clicks from dashboard
- Vector indexing completes within 5 seconds of profile save

### 4.2 Job Discovery & Intelligence [P0 — MVP]

**FR-010:** System discovers jobs from configured sources on schedule (6h interval)  
**FR-011:** System parses JDs to extract skills, requirements, hidden signals  
**FR-012:** System deduplicates jobs across sources  
**FR-013:** User can manually import job via URL  
**FR-014:** Job feed displays matched jobs sorted by match score  
**FR-015:** Job detail shows company intelligence (health score, funding, hiring velocity)

**Acceptance Criteria:**
- Jobs appear in feed within 6h of posting (for supported sources)
- JD parsing F1 ≥ 0.85 on skill extraction
- Zero duplicate jobs in user's feed

### 4.3 Matching Engine [P0 — MVP]

**FR-020:** System computes match score (0-100) for each job vs user profile  
**FR-021:** System generates gap analysis (matched skills, missing skills, transferable skills)  
**FR-022:** System estimates interview probability (shortlist, OA, interview)  
**FR-023:** System recommends action (strong_apply, apply, consider, skip)  
**FR-024:** User can bookmark or dismiss matched jobs

**Acceptance Criteria:**
- Match scores correlate with user-perceived fit (≥ 80% agreement in user testing)
- Gap analysis identifies top 3 gaps and top 3 strengths
- Jobs below user's threshold are hidden from primary feed

### 4.4 Application Generation [P0 — MVP]

**FR-030:** User can generate application pack for a matched job  
**FR-031:** System generates ATS-optimized tailored resume (grounded in profile, no fabrication)  
**FR-032:** System generates personalized cover letter (≤ 350 words)  
**FR-033:** System generates outreach messages (LinkedIn DM + email)  
**FR-034:** System computes ATS score and keyword coverage  
**FR-035:** All materials enter PENDING_REVIEW state — never auto-submitted

**Acceptance Criteria:**
- Generation completes within 60 seconds (p95)
- ATS score ≥ 70 on first generation for 80% of applications
- Zero fabricated experience in validation testing (100% pass rate)
- User can edit all generated materials inline

### 4.5 Human Approval Workflow [P0 — MVP]

**FR-040:** User reviews all materials in unified review page  
**FR-041:** User can approve, reject (with feedback), or edit materials  
**FR-042:** Approved materials unlock copy-to-clipboard and external apply link  
**FR-043:** User confirms manual submission → status changes to SUBMITTED  
**FR-044:** All approval actions logged in immutable audit trail

**Acceptance Criteria:**
- Review page loads all materials in < 2 seconds
- Approve/reject actions persist immediately
- System physically cannot submit to external job boards (API enforced)
- Audit log captures action, timestamp, IP, changes

### 4.6 Application Tracker [P0 — MVP]

**FR-050:** Kanban board with stages: Applied → OA → Interview → Rejected → Offer  
**FR-051:** User can drag applications between stages or update via dropdown  
**FR-052:** System suggests follow-up after 7 days in Applied stage  
**FR-053:** Moving to Interview stage triggers interview prep availability

**Acceptance Criteria:**
- Board loads all applications in < 1 second
- Status changes persist and reflect in analytics
- Follow-up suggestion appears exactly at 7-day mark

### 4.7 Interview Coach [P1 — MVP Basic]

**FR-060:** User can start mock interview session (behavioral, technical, system design)  
**FR-061:** System generates role-specific questions based on JD  
**FR-062:** User submits answers and receives AI feedback with improvement suggestions

**Acceptance Criteria:**
- Questions relevant to specific role (validated by user rating ≥ 4/5)
- Feedback includes STAR structure analysis and specific improvements

### 4.8 Subscription & Quotas [P0 — MVP]

**FR-070:** Free tier with defined limits; Pro tier via Stripe subscription  
**FR-071:** System enforces quotas (applications/month, jobs analyzed/day)  
**FR-072:** Upgrade prompts at quota limits with Stripe checkout  
**FR-073:** Billing portal for subscription management

**Acceptance Criteria:**
- Quota enforcement is accurate (zero over-quota generation)
- Stripe checkout completes in < 3 clicks from upgrade prompt
- Subscription changes reflect within 60 seconds of webhook

---

## 5. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| API response time (p95) | < 500ms (non-AI endpoints) |
| Application generation (p95) | < 60 seconds |
| Uptime | 99.5% (MVP), 99.9% (Scale) |
| Concurrent users | 100 (MVP), 10,000 (Scale) |
| Data encryption | AES-256 at rest, TLS 1.3 in transit |
| GDPR compliance | Data export + deletion within 30 days |
| Accessibility | WCAG 2.1 AA (Phase 2) |
| Mobile | Responsive web (MVP), native app (Phase 3) |

---

## 6. Out of Scope (MVP)

- Auto-submission to any job board
- Browser extension
- Email parsing for status updates
- Voice-based interview coach
- Mobile native app
- Multi-language support
- Enterprise SSO
- API access for third parties
- Networking contact scraping from LinkedIn

---

## 7. User Stories (Priority Order)

| # | Story | Priority | Points |
|---|-------|----------|--------|
| 1 | As a user, I upload my resume and see my parsed profile | P0 | 5 |
| 2 | As a user, I set job preferences and see matched jobs | P0 | 8 |
| 3 | As a user, I see match score and gap analysis for a job | P0 | 5 |
| 4 | As a user, I generate an application pack for a high-match job | P0 | 13 |
| 5 | As a user, I review and approve materials before applying | P0 | 8 |
| 6 | As a user, I track my applications on a kanban board | P0 | 5 |
| 7 | As a user, I upgrade to Pro when I hit free limits | P0 | 5 |
| 8 | As a user, I receive outreach message drafts | P0 | 5 |
| 9 | As a user, I practice mock interviews for upcoming interviews | P1 | 8 |
| 10 | As a user, I see analytics on my application performance | P1 | 5 |

---

## 8. Dependencies & Risks

| Dependency | Risk | Mitigation |
|-----------|------|------------|
| OpenAI/Anthropic API availability | Service outage | Multi-provider fallback |
| Job source APIs | Access revoked | Multiple sources + manual import |
| Clerk auth | Service outage | Session caching, graceful degradation |
| Stripe payments | Webhook failures | Idempotent processing + reconciliation |
| Pinecone | Latency/cost at scale | pgvector fallback |

---

## 9. Launch Criteria

- [ ] All P0 features implemented and tested
- [ ] End-to-end flow validated by 10 beta testers
- [ ] Interview rate ≥ 10% in beta (target 15% at scale)
- [ ] Zero critical bugs in staging for 7 days
- [ ] Security review completed (OWASP top 10)
- [ ] Load test passed (100 concurrent users)
- [ ] Stripe payments working in production
- [ ] Legal review of ToS and Privacy Policy
- [ ] Sentry + PostHog instrumentation live
- [ ] Landing page + onboarding wizard complete

---

## 10. Appendix

### A. Glossary
- **Application Pack:** Tailored resume + cover letter + outreach messages
- **Match Score:** 0-100 fit score between user profile and job
- **ATS Score:** 0-100 resume compatibility with job's ATS keywords
- **Approval Gate:** Mandatory user review before submission

### B. Related Documents
- [System Architecture](01-system-architecture.md)
- [Technical Design Document](18-technical-design-document.md)
- [MVP Roadmap](09-mvp-roadmap.md)
