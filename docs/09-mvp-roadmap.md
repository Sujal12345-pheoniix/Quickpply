# ApplyPilot AI — MVP Roadmap

**Timeline:** 12 weeks | **Team:** 2 engineers + 1 designer + founder  
**Goal:** 500 beta users, 15% interview rate, $5K MRR

---

## Phase 0: Foundation (Weeks 1-2)

### Week 1
- [ ] Monorepo setup (Next.js + FastAPI + Docker)
- [ ] PostgreSQL schema migration (Alembic)
- [ ] Clerk auth integration (FE + BE webhook sync)
- [ ] Basic dashboard shell with ShadCN
- [ ] CI/CD pipeline (GitHub Actions → Vercel + Railway)

### Week 2
- [ ] Profile CRUD API + resume upload (PDF parsing)
- [ ] Job preferences form
- [ ] Pinecone index setup + embedding service
- [ ] Profile indexing pipeline
- [ ] Sentry + PostHog instrumentation

**Exit criteria:** User can sign up, upload resume, set preferences

---

## Phase 1: Job Intelligence (Weeks 3-5)

### Week 3
- [ ] Job source adapters: RemoteOK, YC Jobs (easiest APIs)
- [ ] Job normalization + dedup pipeline
- [ ] JD parsing prompt v1.0.0 + eval suite
- [ ] Job listing API + frontend feed

### Week 4
- [ ] Matching engine v1 (embedding similarity + LLM gap analysis)
- [ ] Match score display + gap analysis UI
- [ ] Job detail page with company intel (basic)
- [ ] Bookmark/dismiss actions

### Week 5
- [ ] Add sources: Wellfound, Indeed
- [ ] Scheduled job discovery (Celery Beat, 6h interval)
- [ ] Email digest: top matches
- [ ] Manual job URL import

**Exit criteria:** Users see matched jobs with scores within 6h of signup

---

## Phase 2: Application Generation (Weeks 6-8)

### Week 6
- [ ] Resume Optimizer agent + prompt v1.0.0
- [ ] RAG retrieval for resume tailoring
- [ ] ATS analyzer (keyword coverage + score)
- [ ] Anti-hallucination validation layer

### Week 7
- [ ] Cover Letter Generator agent
- [ ] Application pack generation API (parallel Celery tasks)
- [ ] Review page UI (side-by-side resume diff)
- [ ] Inline editing + re-ATS-score

### Week 8
- [ ] Human approval workflow (approve/reject/regenerate)
- [ ] Approval audit log
- [ ] Outreach agent (LinkedIn DM + email)
- [ ] Copy-to-clipboard + manual submit confirmation

**Exit criteria:** End-to-end flow from job match → approved application pack

---

## Phase 3: Tracker + Monetization (Weeks 9-10)

### Week 9
- [ ] Application tracker (Kanban board)
- [ ] Status update API + UI
- [ ] AI-suggested follow-ups (7-day rule)
- [ ] Usage quota system (Redis counters)

### Week 10
- [ ] Stripe integration (Free + Pro tiers)
- [ ] Checkout + billing portal
- [ ] Quota enforcement middleware
- [ ] Upgrade prompts at quota limits

**Exit criteria:** Users can track applications and upgrade to Pro

---

## Phase 4: Polish + Launch (Weeks 11-12)

### Week 11
- [ ] Interview Coach agent (basic mock interview)
- [ ] Analytics dashboard (application stats)
- [ ] Landing page + SEO
- [ ] Onboarding wizard polish
- [ ] Mobile responsive pass

### Week 12
- [ ] Beta launch (500 users via waitlist)
- [ ] Load testing (100 concurrent users)
- [ ] Security audit (OWASP top 10)
- [ ] Documentation + help center
- [ ] Feedback collection loop

**Exit criteria:** Public beta live, paying customers

---

## MVP Feature Matrix

| Feature | MVP | Post-MVP |
|---------|-----|----------|
| Resume upload + parse | ✅ | |
| Job preferences | ✅ | |
| RemoteOK + YC + Wellfound + Indeed | ✅ | |
| LinkedIn + Naukri + Instahyre | | ✅ Phase 2 |
| Career page scraper | | ✅ Phase 2 |
| Match scoring | ✅ | |
| Gap analysis | ✅ | |
| Interview probability | ✅ Basic | Advanced model |
| Resume tailoring | ✅ | |
| Cover letter | ✅ | |
| Outreach messages | ✅ DM + Email | Referral requests |
| Human approval | ✅ | |
| Application tracker | ✅ | |
| Interview coach | ✅ Basic | Voice mode |
| Market intelligence | | ✅ Phase 2 |
| Networking engine | | ✅ Phase 2 |
| Browser extension | | ✅ Phase 3 |
| Teams tier | | ✅ Phase 2 |
| Email parsing | | ✅ Phase 3 |

---

## MVP Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Signup → first match | < 24 hours | PostHog funnel |
| Match → application generated | 20% | Conversion rate |
| Application → approved | 70% | Approval rate |
| Approved → submitted | 80% | Submission rate |
| Submitted → interview | 15% | User-reported + tracker |
| Free → Pro conversion | 8% | Stripe |
| NPS | ≥ 40 | In-app survey |
| Churn (monthly) | < 5% | Stripe |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| LLM quality inconsistent | Eval suite + human review loop before prompt promotion |
| Job source API changes | Adapter pattern + circuit breakers + manual import fallback |
| Low interview rates | A/B test resume formats; collect outcome data to improve matching |
| Legal (ToS violations) | No auto-submit; official APIs preferred; legal review before launch |
| High LLM costs | gpt-4o-mini for extraction; cache aggressively; quota limits |

---

## Beta Launch Strategy

1. **Waitlist:** 2,000 signups via landing page (Week 8)
2. **Invite waves:** 100/week starting Week 12
3. **Cohort:** Software engineers, 2-8 YOE, US remote
4. **Feedback:** Weekly 15-min calls with 10 power users
5. **Iterate:** 2-week sprint cycles post-launch
