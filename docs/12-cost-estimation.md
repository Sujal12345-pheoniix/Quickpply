# ApplyPilot AI — Cost Estimation

**Baseline:** 100,000 MAU | **Paid conversion:** 8% | **Avg revenue:** $29/mo

---

## 1. Revenue Model (at 100K MAU)

| Tier | Price | Users | MRR |
|------|-------|-------|-----|
| Free | $0 | 92,000 (92%) | $0 |
| Pro | $29/mo | 7,200 (7.2%) | $208,800 |
| Teams | $79/mo/seat | 800 seats (0.8%) | $63,200 |
| **Total** | | **100,000** | **$272,000/mo** |

**ARR:** $3.26M | **Gross margin target:** 65%+

---

## 2. Infrastructure Costs (100K MAU)

| Service | Unit Cost | Volume | Monthly |
|---------|-----------|--------|---------|
| **Railway (API + Workers)** | | | |
| FastAPI (4 instances) | $50/instance | 4 | $200 |
| Celery workers (8 instances) | $50/instance | 8 | $400 |
| Celery Beat | $20 | 1 | $20 |
| **Database** | | | |
| PostgreSQL (Railway Pro) | $100 | 1 primary | $100 |
| Read replica | $100 | 1 | $100 |
| PgBouncer | $20 | 1 | $20 |
| **Redis** | | | |
| Redis cluster | $50 | 2 nodes | $100 |
| **Vercel** | | | |
| Pro plan + bandwidth | $20 + overage | 1 | $150 |
| **Pinecone** | | | |
| Serverless → Pod-based | $0.10/1M queries | 5M queries | $500 |
| Storage (2.5M vectors) | $0.025/GB | 50GB | $50 |
| **Cloudflare R2** | | | |
| Storage (resumes, PDFs) | $0.015/GB | 500GB | $8 |
| Egress | $0 | Free | $0 |
| **Monitoring** | | | |
| Sentry (Team) | $80 | 1 | $80 |
| PostHog (Scale) | $450 | 1 | $450 |
| **Email (Resend)** | $0.001/email | 500K emails | $500 |
| **Domain + DNS** | | | $50 |
| **Subtotal Infra** | | | **$2,728/mo** |

---

## 3. LLM Costs (100K MAU)

### 3.1 Usage Assumptions

| Action | Per User/Month | Active Users | Total/Month |
|--------|---------------|--------------|-------------|
| Job parsing (ingestion) | 200 jobs × 2K tokens | 100K (shared) | 40M tokens |
| Match scoring | 50 × 3K tokens | 30K active | 4.5B tokens |
| Resume tailoring | 8 × 8K tokens | 8K paid | 512M tokens |
| Cover letter | 8 × 4K tokens | 8K paid | 256M tokens |
| Outreach | 8 × 2K tokens | 8K paid | 128M tokens |
| Interview prep | 2 × 6K tokens | 3K | 36M tokens |
| ATS scoring | 8 × 1K tokens | 8K paid | 64M tokens |
| Embeddings | 10 × 1K tokens | 30K active | 300M tokens |

### 3.2 Cost by Model

| Model | Token Volume | Rate | Cost |
|-------|-------------|------|------|
| gpt-4o-mini (input) | 3B tokens | $0.15/1M | $450 |
| gpt-4o-mini (output) | 500M tokens | $0.60/1M | $300 |
| claude-3-5-sonnet (input) | 800M tokens | $3.00/1M | $2,400 |
| claude-3-5-sonnet (output) | 200M tokens | $15.00/1M | $3,000 |
| text-embedding-3-small | 300M tokens | $0.02/1M | $6 |
| **Subtotal LLM** | | | **$6,156/mo** |

### 3.3 Optimization Impact (at scale)

| Optimization | Savings | Adjusted Cost |
|-------------|---------|---------------|
| Response caching (30% hit) | -$1,847 | $4,309 |
| Fine-tuned resume model | -$1,500 | $2,809 |
| Batch API (ingestion) | -$200 | $2,609 |
| **Optimized LLM** | | **~$2,600/mo** |

---

## 4. People Costs (Month 24)

| Role | Count | Avg Salary | Monthly |
|------|-------|-----------|---------|
| Engineering | 12 | $150K | $150,000 |
| Product/Design | 3 | $130K | $32,500 |
| Growth/Marketing | 4 | $120K | $40,000 |
| Sales | 3 | $100K + comm | $30,000 |
| CS/Support | 3 | $60K | $15,000 |
| G&A (legal, finance) | 2 | $120K | $20,000 |
| Founders | 2 | $150K | $25,000 |
| **Subtotal People** | **29** | | **$312,500/mo** |

---

## 5. Other Operating Costs

| Category | Monthly |
|----------|---------|
| Job source APIs (RapidAPI, etc.) | $2,000 |
| Stripe fees (2.9% + $0.30) | $7,888 |
| Legal/compliance | $5,000 |
| Insurance (E&O, cyber) | $2,000 |
| Office/tools (GitHub, Figma, etc.) | $3,000 |
| Marketing/ad spend | $30,000 |
| **Subtotal Other** | **$49,888/mo** |

---

## 6. Total Cost Summary (100K MAU)

| Category | Monthly | % of Revenue |
|----------|---------|-------------|
| Infrastructure | $2,728 | 1.0% |
| LLM (optimized) | $2,600 | 1.0% |
| People | $312,500 | 114.9% |
| Other | $49,888 | 18.3% |
| **Total** | **$367,716/mo** | **135.2%** |

**Note:** At 100K MAU with 8% paid, company is investment-stage (not yet profitable on people costs). Unit economics are strong:

---

## 7. Unit Economics (Per Paying User)

| Metric | Value |
|--------|-------|
| ARPU (Pro) | $29/mo |
| LLM cost per Pro user | ~$0.33/mo |
| Infra cost per Pro user | ~$0.34/mo |
| **Gross margin per Pro user** | **$28.33 (97.7%)** |
| CAC target | < $50 |
| LTV (12-month, 5% churn) | $290 |
| **LTV:CAC ratio** | **5.8:1** |

---

## 8. Cost by Growth Stage

| Stage | MAU | Infra | LLM | People | Total/mo | MRR | Burn |
|-------|-----|-------|-----|--------|----------|-----|------|
| MVP | 500 | $200 | $150 | $25K | $30K | $1K | -$29K |
| PMF | 5K | $800 | $800 | $60K | $70K | $12K | -$58K |
| Growth | 25K | $1,500 | $3K | $150K | $170K | $58K | -$112K |
| Scale | 100K | $2,700 | $2,600 | $312K | $367K | $272K | -$95K |
| Profitable | 200K | $5K | $4K | $350K | $420K | $580K | +$160K |

**Break-even (people costs covered):** ~180K MAU at 8% paid conversion

---

## 9. LLM Cost Per Application Pack

| Component | Tokens | Model | Cost |
|-----------|--------|-------|------|
| RAG retrieval | 500 | embedding | $0.00001 |
| Resume tailoring | 8,000 | claude-3-5-sonnet | $0.08 |
| Cover letter | 4,000 | claude-3-5-sonnet | $0.04 |
| Outreach (3 messages) | 4,000 | gpt-4o-mini | $0.002 |
| ATS scoring | 2,000 | gpt-4o-mini | $0.001 |
| **Total per pack** | | | **~$0.12** |

At $29/mo Pro with 50 packs: $6 revenue vs $6 LLM cost → need caching + mini models to maintain margin.

**With optimization:** ~$0.05/pack → $2.50 LLM cost for 50 packs → **91% gross margin on LLM**

---

## 10. Funding Requirements

| Round | Amount | Runway | Milestone |
|-------|--------|--------|-----------|
| Pre-seed | $500K | 12 months | MVP + 5K users |
| Seed | $2M | 18 months | 25K users, $50K MRR |
| Series A | $8M | 24 months | 100K users, $250K MRR |

**Seed allocation:** 60% engineering, 25% growth, 15% ops/legal
