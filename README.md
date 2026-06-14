# ApplyPilot AI

**Tagline:** AI that applies to jobs exactly like a top candidate would.

Production-grade job application intelligence platform. Not spam. Not bots. Human-quality applications at scale—with mandatory human approval before every submission.

## Repository Structure

```
applypilot/
├── docs/                    # All product & engineering deliverables
├── frontend/                # Next.js 15 + TypeScript + Tailwind + ShadCN
├── backend/                 # FastAPI + Celery + SQLAlchemy
├── infra/                   # Docker, Railway, Vercel configs
├── prompts/                 # Versioned prompt registry
└── scripts/                 # Dev & deployment scripts
```

## Quick Start

```bash
# Infrastructure
docker compose up -d postgres redis

# Backend
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm run dev

# Workers
celery -A app.workers.celery_app worker -l info
```

## Documentation Index

| # | Deliverable | Location |
|---|-------------|----------|
| 1 | System Architecture | [docs/01-system-architecture.md](docs/01-system-architecture.md) |
| 2 | Database Schema | [docs/02-database-schema.sql](docs/02-database-schema.sql) |
| 3 | Folder Structure | [docs/03-folder-structure.md](docs/03-folder-structure.md) |
| 4 | API Design | [docs/04-api-design.yaml](docs/04-api-design.yaml) |
| 5 | AI Agent Architecture | [docs/05-ai-agent-architecture.md](docs/05-ai-agent-architecture.md) |
| 6 | Prompt Engineering | [docs/06-prompt-engineering.md](docs/06-prompt-engineering.md) |
| 7 | RAG Implementation | [docs/07-rag-implementation.md](docs/07-rag-implementation.md) |
| 8 | User Flow Diagrams | [docs/08-user-flows.md](docs/08-user-flows.md) |
| 9 | MVP Roadmap | [docs/09-mvp-roadmap.md](docs/09-mvp-roadmap.md) |
| 10 | Scale Roadmap | [docs/10-scale-roadmap.md](docs/10-scale-roadmap.md) |
| 11 | Security Design | [docs/11-security-design.md](docs/11-security-design.md) |
| 12 | Cost Estimation | [docs/12-cost-estimation.md](docs/12-cost-estimation.md) |
| 13 | Deployment Plan | [docs/13-deployment-plan.md](docs/13-deployment-plan.md) |
| 14 | Growth Strategy | [docs/14-growth-strategy.md](docs/14-growth-strategy.md) |
| 15 | Competitive Advantage | [docs/15-competitive-advantage.md](docs/15-competitive-advantage.md) |
| 16 | Monetization | [docs/16-monetization-strategy.md](docs/16-monetization-strategy.md) |
| 17 | PRD | [docs/17-PRD.md](docs/17-PRD.md) |
| 18 | Technical Design | [docs/18-technical-design-document.md](docs/18-technical-design-document.md) |
| 19 | Sprint Plan | [docs/19-development-sprint-plan.md](docs/19-development-sprint-plan.md) |
| 20 | Cursor Prompts | [docs/20-cursor-implementation-prompts.md](docs/20-cursor-implementation-prompts.md) |

## Core Principles

1. **Human-in-the-loop always** — AI prepares; user approves; system never auto-submits
2. **Quality over volume** — Match score threshold gates application generation
3. **ATS-first** — Every resume output passes internal ATS simulation before delivery
4. **Compliance by design** — Rate limits, platform ToS respect, audit trails

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 15, TypeScript, Tailwind, ShadCN, Clerk |
| Backend | FastAPI, Celery, Redis, PostgreSQL |
| AI | OpenAI GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro |
| Vector | Pinecone |
| Payments | Stripe |
| Deploy | Vercel (FE), Railway (BE) |
| Observability | Sentry, PostHog |

## License

Proprietary. All rights reserved.
