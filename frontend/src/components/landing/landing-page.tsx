import Link from "next/link";
import { ArrowRight, BadgeCheck, Brain, BriefcaseBusiness, ShieldCheck, Sparkles, Target, TimerReset } from "lucide-react";

export function LandingPage() {
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-50 border-b border-slate-200/80 bg-white/70 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-slate-500">ApplyPilot AI</p>
            <p className="text-sm text-slate-500">AI that applies like a top candidate would</p>
          </div>
          <nav className="flex items-center gap-6 text-sm text-slate-600">
            <Link href="#workflow" className="transition hover:text-slate-950">
              Workflow
            </Link>
            <Link href="#agents" className="transition hover:text-slate-950">
              Agents
            </Link>
            <Link href="#pricing" className="transition hover:text-slate-950">
              Pricing
            </Link>
            <Link
              href="/dashboard"
              className="inline-flex items-center gap-2 rounded-full bg-slate-950 px-4 py-2 font-medium text-white transition hover:bg-slate-800"
            >
              Get started
              <ArrowRight className="h-4 w-4" />
            </Link>
          </nav>
        </div>
      </header>

      <main>
        <section className="mx-auto grid max-w-7xl gap-12 px-6 pb-20 pt-16 lg:grid-cols-[1.15fr_0.85fr] lg:pt-24">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm text-slate-600 shadow-sm">
              <Sparkles className="h-4 w-4 text-amber-500" />
              Human-reviewed applications, never bot spam
            </div>
            <h1 className="mt-6 text-5xl font-semibold tracking-tight text-slate-950 sm:text-6xl">
              AI that applies to jobs exactly like a top candidate would.
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600">
              Find the right roles, tailor every asset, and generate recruiter-ready outreach with mandatory approval before every submission.
            </p>
            <div className="mt-10 flex flex-wrap items-center gap-4">
              <Link
                href="/dashboard"
                className="inline-flex items-center gap-2 rounded-full bg-slate-950 px-6 py-3 text-sm font-medium text-white transition hover:bg-slate-800"
              >
                Start free
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                href="#workflow"
                className="inline-flex items-center gap-2 rounded-full border border-slate-300 bg-white px-6 py-3 text-sm font-medium text-slate-700 transition hover:border-slate-400 hover:text-slate-950"
              >
                See workflow
              </Link>
            </div>
            <div className="mt-8 flex flex-wrap gap-6 text-sm text-slate-600">
              <div className="flex items-center gap-2"><ShieldCheck className="h-4 w-4 text-emerald-600" /> Human approval gate</div>
              <div className="flex items-center gap-2"><Target className="h-4 w-4 text-blue-600" /> ATS-first ranking</div>
              <div className="flex items-center gap-2"><TimerReset className="h-4 w-4 text-amber-600" /> Faster applications, not more spam</div>
            </div>
          </div>

          <div className="rounded-[2rem] border border-slate-200 bg-white p-5 shadow-[0_30px_80px_rgba(15,23,42,0.12)]">
            <div className="rounded-[1.5rem] bg-slate-950 p-6 text-white">
              <div className="flex items-center justify-between text-sm text-slate-300">
                <span>Candidate readiness</span>
                <span>86/100</span>
              </div>
              <div className="mt-4 h-3 overflow-hidden rounded-full bg-slate-800">
                <div className="h-full w-[86%] rounded-full bg-gradient-to-r from-cyan-400 via-blue-500 to-amber-400" />
              </div>
              <div className="mt-6 grid gap-3 text-sm text-slate-200 sm:grid-cols-2">
                <div className="rounded-2xl bg-white/5 p-4">
                  <p className="text-slate-400">Match score</p>
                  <p className="mt-1 text-2xl font-semibold text-white">92%</p>
                </div>
                <div className="rounded-2xl bg-white/5 p-4">
                  <p className="text-slate-400">Interview probability</p>
                  <p className="mt-1 text-2xl font-semibold text-white">68%</p>
                </div>
                <div className="rounded-2xl bg-white/5 p-4">
                  <p className="text-slate-400">ATS coverage</p>
                  <p className="mt-1 text-2xl font-semibold text-white">94%</p>
                </div>
                <div className="rounded-2xl bg-white/5 p-4">
                  <p className="text-slate-400">Ready to send</p>
                  <p className="mt-1 text-2xl font-semibold text-white">Approval only</p>
                </div>
              </div>
            </div>
            <div className="mt-5 grid gap-3 sm:grid-cols-3">
              {[
                { label: "Jobs analyzed", value: "1,248" },
                { label: "Resumes tailored", value: "8,400" },
                { label: "Messages generated", value: "12,970" },
              ].map((item) => (
                <div key={item.label} className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <p className="text-xs uppercase tracking-[0.18em] text-slate-500">{item.label}</p>
                  <p className="mt-2 text-xl font-semibold text-slate-950">{item.value}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="workflow" className="mx-auto max-w-7xl px-6 py-20">
          <div className="max-w-2xl">
            <p className="text-sm font-semibold uppercase tracking-[0.28em] text-slate-500">Workflow</p>
            <h2 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">A hiring workflow that behaves like a strong applicant, not a bot.</h2>
          </div>
          <div className="mt-10 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
            {[
              { title: "Discover", desc: "Collect roles from job boards and company career pages.", icon: BriefcaseBusiness },
              { title: "Analyze", desc: "Extract skills, hidden requirements, and company context.", icon: Brain },
              { title: "Tailor", desc: "Generate ATS-safe resume, cover letter, and outreach.", icon: BadgeCheck },
              { title: "Approve", desc: "User reviews everything before any manual submission.", icon: ShieldCheck },
            ].map((step, index) => {
              const Icon = step.icon;
              return (
                <div key={step.title} className="rounded-[1.5rem] border border-slate-200 bg-white p-6 shadow-sm">
                  <div className="flex items-center justify-between text-sm text-slate-500">
                    <span>Step {index + 1}</span>
                    <Icon className="h-5 w-5 text-slate-900" />
                  </div>
                  <h3 className="mt-6 text-xl font-semibold text-slate-950">{step.title}</h3>
                  <p className="mt-3 text-sm leading-6 text-slate-600">{step.desc}</p>
                </div>
              );
            })}
          </div>
        </section>

        <section id="agents" className="bg-slate-950 py-20 text-white">
          <div className="mx-auto max-w-7xl px-6">
            <div className="max-w-2xl">
              <p className="text-sm font-semibold uppercase tracking-[0.28em] text-slate-400">AI Agents</p>
              <h2 className="mt-3 text-3xl font-semibold tracking-tight">Seven specialist agents, one approval gate.</h2>
            </div>
            <div className="mt-10 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {[
                ["Job Finder", "Multi-source intake and normalization."],
                ["Resume Optimizer", "ATS-safe tailoring grounded in real experience."],
                ["Cover Letter Generator", "Role-specific narrative with the right tone."],
                ["Recruiter Outreach", "LinkedIn DM, email, referral, and follow-up drafts."],
                ["Application Tracker", "Status, notes, and next steps in one place."],
                ["Market Intelligence", "Company health, compensation, and hiring signals."],
              ].map(([title, desc]) => (
                <div key={title} className="rounded-[1.25rem] border border-white/10 bg-white/5 p-5">
                  <h3 className="font-semibold text-white">{title}</h3>
                  <p className="mt-2 text-sm leading-6 text-slate-300">{desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section id="pricing" className="mx-auto max-w-7xl px-6 py-20">
          <div className="max-w-2xl">
            <p className="text-sm font-semibold uppercase tracking-[0.28em] text-slate-500">Pricing</p>
            <h2 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Simple plans that align with interview outcomes.</h2>
          </div>
          <div className="mt-10 grid gap-6 lg:grid-cols-2">
            <div className="rounded-[1.75rem] border border-slate-200 bg-white p-8 shadow-sm">
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Free</p>
              <div className="mt-4 flex items-end gap-1">
                <span className="text-5xl font-semibold text-slate-950">$0</span>
                <span className="pb-1 text-slate-500">/mo</span>
              </div>
              <ul className="mt-6 space-y-3 text-sm text-slate-600">
                <li>5 application packs per month</li>
                <li>Job matching and gap analysis</li>
                <li>ATS resume score and keyword coverage</li>
              </ul>
            </div>
            <div className="rounded-[1.75rem] border border-slate-950 bg-slate-950 p-8 text-white shadow-[0_24px_80px_rgba(15,23,42,0.3)]">
              <div className="inline-flex rounded-full bg-white/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-white/70">
                Popular
              </div>
              <div className="mt-4 flex items-end gap-1">
                <span className="text-5xl font-semibold text-white">$29</span>
                <span className="pb-1 text-slate-300">/mo</span>
              </div>
              <ul className="mt-6 space-y-3 text-sm text-slate-300">
                <li>50 application packs per month</li>
                <li>All job sources and intelligence layers</li>
                <li>Recruiter outreach and interview coaching</li>
                <li>Approval workflow and application tracker</li>
              </ul>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
