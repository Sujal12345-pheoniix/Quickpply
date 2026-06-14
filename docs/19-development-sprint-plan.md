# ApplyPilot AI — Development Sprint Plan

**Sprint Duration:** 2 weeks | **Team:** 2 engineers + 1 designer + founder  
**Total Sprints:** 6 (12 weeks to MVP)

---

## Sprint 1: Foundation (Weeks 1-2)

**Goal:** User can sign up, upload resume, and see dashboard shell

### Backend (Engineer 1)
| Task | Points | Owner |
|------|--------|-------|
| FastAPI project setup + config | 2 | Eng 1 |
| PostgreSQL schema + Alembic migrations | 5 | Eng 1 |
| Clerk JWT verification middleware | 3 | Eng 1 |
| User sync webhook (Clerk → DB) | 3 | Eng 1 |
| Profile CRUD API | 5 | Eng 1 |
| Resume upload + PDF parsing (PyMuPDF) | 5 | Eng 1 |

### Frontend (Engineer 2)
| Task | Points | Owner |
|------|--------|-------|
| Next.js 15 project setup + Tailwind + ShadCN | 3 | Eng 2 |
| Clerk auth integration | 3 | Eng 2 |
| Dashboard layout (sidebar, header) | 5 | Eng 2 |
| Landing page (hero, features, CTA) | 5 | Eng 2 |
| Profile page (view/edit) | 5 | Eng 2 |
| Resume upload component | 3 | Eng 2 |

### Design
| Task | Points | Owner |
|------|--------|-------|
| Design system (colors, typography, components) | 5 | Design |
| Dashboard wireframes | 3 | Design |
| Landing page mockup | 3 | Design |

### DevOps
| Task | Points | Owner |
|------|--------|-------|
| Docker Compose (PG + Redis) | 2 | Eng 1 |
| GitHub Actions CI (lint, test, build) | 3 | Eng 1 |
| Railway + Vercel project setup | 2 | Eng 1 |

**Sprint 1 Total:** 55 points | **Velocity target:** 50

**Demo:** Sign up → upload resume → see parsed profile on dashboard

---

## Sprint 2: Job Intelligence (Weeks 3-4)

**Goal:** Jobs discovered, parsed, and displayed with match scores

### Backend
| Task | Points |
|------|--------|
| Pinecone setup + embedding service | 5 |
| Profile indexing pipeline | 5 |
| Job source adapter: RemoteOK | 3 |
| Job source adapter: YC Jobs | 3 |
| Job normalization + dedup | 5 |
| JD parsing prompt v1 + agent | 8 |
| Job CRUD API + listing with filters | 5 |
| Matching engine v1 (embedding + LLM) | 8 |
| Match results API | 3 |
| Celery setup + job ingestion task | 5 |
| Job preferences API | 3 |

### Frontend
| Task | Points |
|------|--------|
| Job preferences form | 5 |
| Job feed page (cards, filters, pagination) | 8 |
| Job detail page | 5 |
| Match score badge + gap analysis panel | 5 |
| Company intel card | 3 |
| Bookmark/dismiss actions | 2 |

**Sprint 2 Total:** 58 points

**Demo:** Set preferences → jobs appear with match scores → view gap analysis

---

## Sprint 3: Application Generation (Weeks 5-6)

**Goal:** End-to-end application pack generation with review

### Backend
| Task | Points |
|------|--------|
| RAG retriever for resume tailoring | 8 |
| Resume Optimizer agent + prompt | 8 |
| Anti-hallucination validator | 5 |
| ATS analyzer (keyword coverage + score) | 5 |
| Cover Letter agent + prompt | 5 |
| Outreach agent (DM + email) | 5 |
| Application generation API (Celery chord) | 8 |
| Application CRUD + materials API | 5 |
| Quota service (Redis counters) | 5 |

### Frontend
| Task | Points |
|------|--------|
| "Prepare Application" flow + loading state | 5 |
| Review page (side-by-side resume diff) | 8 |
| Cover letter editor | 3 |
| ATS score breakdown component | 5 |
| Outreach messages tab | 3 |
| Inline editing + save | 5 |
| Generation progress indicator | 3 |

**Sprint 3 Total:** 60 points

**Demo:** Select job → generate pack → review tailored resume + cover letter + outreach

---

## Sprint 4: Approval + Tracker (Weeks 7-8)

**Goal:** Human approval workflow and application tracking

### Backend
| Task | Points |
|------|--------|
| Approval workflow API (approve/reject/submit) | 5 |
| Approval audit log | 3 |
| Application status update API | 3 |
| Follow-up suggestion logic (7-day rule) | 3 |
| Add sources: Wellfound + Indeed | 5 |
| Scheduled job discovery (Celery Beat) | 5 |
| Email digest (top matches) | 5 |

### Frontend
| Task | Points |
|------|--------|
| Approval panel (approve/reject/edit) | 8 |
| Copy-to-clipboard + external link | 2 |
| Submit confirmation modal | 3 |
| Kanban tracker board | 8 |
| Status update dropdown | 3 |
| Application detail page | 5 |
| Follow-up suggestion card | 3 |

**Sprint 4 Total:** 48 points

**Demo:** Approve application → mark submitted → track on kanban → get follow-up suggestion

---

## Sprint 5: Monetization + Interview Coach (Weeks 9-10)

**Goal:** Stripe payments and basic interview prep

### Backend
| Task | Points |
|------|--------|
| Stripe checkout + webhook integration | 8 |
| Subscription management API | 5 |
| Quota enforcement middleware | 5 |
| Billing portal API | 3 |
| Interview Coach agent + prompt | 8 |
| Interview session API | 5 |
| Analytics dashboard API | 5 |

### Frontend
| Task | Points |
|------|--------|
| Stripe checkout integration | 5 |
| Upgrade modal at quota limits | 5 |
| Billing settings page | 5 |
| Interview prep page | 8 |
| Mock interview UI (question/answer/feedback) | 8 |
| Analytics dashboard | 5 |

**Sprint 5 Total:** 53 points

**Demo:** Hit free limit → upgrade to Pro → mock interview for upcoming interview

---

## Sprint 6: Polish + Launch (Weeks 11-12)

**Goal:** Production-ready beta launch

### All Team
| Task | Points | Owner |
|------|--------|-------|
| Onboarding wizard (4 steps) | 8 | Eng 2 + Design |
| Mobile responsive pass | 5 | Eng 2 |
| Error handling + empty states | 5 | Eng 2 |
| Sentry + PostHog full instrumentation | 5 | Eng 1 |
| Load testing (100 concurrent) | 5 | Eng 1 |
| Security review (OWASP top 10) | 5 | Eng 1 |
| Prompt eval suite | 5 | Eng 1 |
| SEO landing page optimization | 3 | Eng 2 |
| Help documentation | 3 | Founder |
| Beta launch checklist | 3 | Founder |
| Product Hunt assets | 3 | Design + Founder |

**Sprint 6 Total:** 45 points

**Demo:** Full platform launch to first 100 beta users

---

## Sprint Ceremonies

| Ceremony | When | Duration |
|----------|------|----------|
| Sprint Planning | Monday W1 | 2 hours |
| Daily Standup | Every day | 15 min |
| Sprint Review | Friday W2 | 1 hour |
| Sprint Retro | Friday W2 | 30 min |
| Backlog Refinement | Wednesday W2 | 1 hour |

---

## Definition of Done

- [ ] Code reviewed and merged to `develop`
- [ ] Unit tests written (≥ 80% coverage on services)
- [ ] API documented in OpenAPI spec
- [ ] No P0/P1 bugs
- [ ] Deployed to staging and verified
- [ ] PostHog events instrumented
- [ ] Designer sign-off on UI

---

## Risk Buffer

Each sprint includes 10% buffer for:
- LLM prompt iteration (expect 2-3 iterations per prompt)
- Job source API quirks
- Clerk/Stripe integration edge cases
- Designer feedback loops

---

## Post-MVP Sprint Preview (Sprints 7-10)

| Sprint | Focus |
|--------|-------|
| 7 | LinkedIn + Naukri sources, networking engine |
| 8 | Browser extension MVP, email parsing |
| 9 | Teams tier, market intelligence reports |
| 10 | Advanced matching model, outcome tracking ML |
