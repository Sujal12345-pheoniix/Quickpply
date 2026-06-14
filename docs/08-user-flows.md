# ApplyPilot AI — User Flow Diagrams

---

## 1. Onboarding Flow

```mermaid
flowchart TD
    A[Land on homepage] --> B{Signed in?}
    B -->|No| C[Sign up via Clerk]
    C --> D[Welcome wizard]
    B -->|Yes| D
    
    D --> E[Step 1: Upload resume]
    E --> F[AI parses resume]
    F --> G[Step 2: Review extracted profile]
    G --> H{Accurate?}
    H -->|No| I[Edit profile manually]
    I --> G
    H -->|Yes| J[Step 3: Set job preferences]
    J --> K[Target titles, locations, salary, sources]
    K --> L[Step 4: Set match threshold]
    L --> M[Dashboard — job discovery starts]
    
    M --> N[Background: Job Finder Agent runs]
    N --> O[Jobs appear in feed with match scores]
```

**Time to value:** < 5 minutes from signup to first matched jobs

---

## 2. Core Application Flow

```mermaid
flowchart TD
    A[Job Feed] --> B[Filter by match score ≥ threshold]
    B --> C[Click job card]
    C --> D[Job Detail Page]
    
    D --> E[View: Match score, gap analysis, interview probability]
    D --> F[View: Company intel, salary estimate]
    
    E --> G{Worth applying?}
    G -->|No| H[Dismiss or Bookmark]
    G -->|Yes| I[Click 'Prepare Application']
    
    I --> J{Quota available?}
    J -->|No| K[Upgrade prompt]
    J -->|Yes| L[AI generates application pack]
    
    L --> M[Parallel: Resume + Cover Letter + Outreach]
    M --> N[ATS score computed]
    N --> O[Review Page — PENDING_REVIEW]
    
    O --> P[User reviews all materials]
    P --> Q{Approve?}
    Q -->|Edit| R[Inline editor — save changes]
    R --> P
    Q -->|Reject| S[Request regeneration with feedback]
    S --> L
    Q -->|Approve| T[Status → APPROVED]
    
    T --> U[User copies materials]
    U --> V[User manually applies on job board]
    V --> W[Returns to ApplyPilot]
    W --> X[Marks as 'Submitted']
    X --> Y[Application Tracker — Applied column]
```

---

## 3. Human Approval Gate (Critical Path)

```mermaid
sequenceDiagram
    participant AI as AI Agents
    participant DB as Database
    participant FE as Review UI
    participant User
    participant Audit as Audit Log

    AI->>DB: Save drafts (status: pending_review)
    AI->>FE: Notify materials ready
    
    User->>FE: Open review page
    FE->>DB: Fetch application pack
    
    Note over FE: Side-by-side view:<br/>Original resume | Tailored resume<br/>Cover letter | Outreach messages<br/>ATS score breakdown
    
    alt User approves
        User->>FE: Click Approve
        FE->>DB: status → approved
        DB->>Audit: Log approval action
        FE->>User: Show copy buttons + apply link
    else User edits
        User->>FE: Edit resume/cover letter
        FE->>DB: Save edits + re-run ATS score
        User->>FE: Click Approve
    else User rejects
        User->>FE: Reject with reason
        FE->>DB: status → draft
        DB->>Audit: Log rejection + reason
        FE->>AI: Queue regeneration with feedback
    end
    
    Note over User: User NEVER auto-submitted.<br/>Manual action required on job board.
    
    User->>FE: Confirm manual submission
    FE->>DB: status → submitted
    DB->>Audit: Log submission confirmation
```

---

## 4. Application Tracker Flow

```mermaid
stateDiagram-v2
    [*] --> Applied: User marks submitted
    Applied --> OA: Recruiter sends assessment
    Applied --> Interview: Direct interview invite
    Applied --> Rejected: No response / rejection
    OA --> Interview: Pass assessment
    OA --> Rejected: Fail assessment
    Interview --> Interview: Multiple rounds
    Interview --> Offer: Offer received
    Interview --> Rejected: Not selected
    Offer --> [*]: Accepted/Declined
    Rejected --> [*]
    
    Applied --> Withdrawn: User withdraws
```

**AI-assisted transitions:**
- 7 days in Applied → AI suggests follow-up outreach
- Moved to OA → AI generates prep checklist
- Moved to Interview → AI triggers Interview Coach

---

## 5. Outreach Flow

```mermaid
flowchart LR
    A[Approved Application] --> B[Networking Engine finds contacts]
    B --> C[Recruiter at company]
    B --> D[Hiring manager]
    B --> E[Team member]
    
    C --> F[LinkedIn DM draft]
    D --> G[Email draft]
    E --> H[Referral request draft]
    
    F --> I[User reviews in Outreach tab]
    G --> I
    H --> I
    
    I --> J[User copies & sends manually]
    J --> K[Mark as sent in ApplyPilot]
    K --> L[7-day follow-up reminder]
```

---

## 6. Interview Prep Flow

```mermaid
flowchart TD
    A[Application status → Interview] --> B[Notification: Interview prep available]
    B --> C[Select session type]
    C --> D[Behavioral / Technical / System Design]
    
    D --> E[AI generates role-specific questions]
    E --> F[Question 1 presented]
    F --> G[User writes answer]
    G --> H[AI feedback: STAR score, specificity, improvements]
    H --> I{More questions?}
    I -->|Yes| F
    I -->|No| J[Session summary + overall score]
    J --> K[Improvement areas + suggested study]
```

---

## 7. Subscription & Quota Flow

```mermaid
flowchart TD
    A[User action requiring quota] --> B{Check tier + usage}
    B -->|Within quota| C[Proceed]
    B -->|Exceeded| D[Soft block modal]
    
    D --> E{Tier?}
    E -->|Free| F[Show upgrade to Pro — $29/mo]
    E -->|Pro| G[Show upgrade to Teams or wait for reset]
    
    F --> H[Stripe Checkout]
    H --> I[Webhook: subscription activated]
    I --> J[Quota reset + tier upgraded]
    J --> C
```

---

## 8. Job Discovery Flow (Background)

```mermaid
flowchart TD
    A[Celery Beat: every 6 hours] --> B[For each active user]
    B --> C[Job Finder Agent]
    C --> D[Poll enabled sources]
    D --> E[Normalize + deduplicate]
    E --> F[LLM: Parse JD]
    F --> G[Index to Pinecone]
    G --> H[Matching Engine]
    H --> I[Score vs user profile]
    I --> J{Score ≥ threshold?}
    J -->|Yes| K[Add to user's job feed]
    J -->|No| L[Store but don't notify]
    K --> M[Email digest: top 5 new matches]
```

---

## 9. Information Architecture (Navigation)

```
Dashboard
├── Overview (stats, recent activity, top matches)
├── Jobs
│   ├── Feed (matched jobs)
│   ├── Saved
│   └── Import URL
├── Applications
│   ├── Kanban Board
│   └── [Application Detail]
│       ├── Materials
│       ├── Review & Approve
│       └── Outreach
├── Profile
│   ├── Resume & Experience
│   ├── Skills
│   └── Preferences
├── Interview Prep
├── Analytics
│   ├── Application stats
│   └── Market reports
└── Settings
    ├── Account
    ├── Notifications
    └── Billing
```

---

## 10. Mobile-Responsive Priorities

| Screen | Mobile Priority | Desktop Enhancement |
|--------|----------------|---------------------|
| Job feed | Card stack, swipe dismiss | Table + filters |
| Review page | Tabbed materials | Side-by-side diff |
| Tracker | Vertical pipeline | Kanban board |
| Profile | Step wizard | Full form |
