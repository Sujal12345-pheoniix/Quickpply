export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <section className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl">
            <p className="text-sm font-semibold uppercase tracking-[0.28em] text-slate-500">Workspace</p>
            <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-950">Your application command center</h1>
            <p className="mt-4 text-slate-600">
              Review matched jobs, prepare tailored materials, and keep every submission inside a human approval loop.
            </p>
          </div>
          <div className="grid gap-3 sm:grid-cols-3 lg:min-w-[28rem]">
            {[
              { label: "Match quality", value: "89%" },
              { label: "Packs ready", value: "12" },
              { label: "Pending review", value: "4" },
            ].map((item) => (
              <div key={item.label} className="rounded-2xl bg-slate-50 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-slate-500">{item.label}</p>
                <p className="mt-2 text-2xl font-semibold text-slate-950">{item.value}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Priority jobs</p>
              <h2 className="mt-2 text-xl font-semibold text-slate-950">Jobs worth investing in</h2>
            </div>
            <span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">3 high-fit roles</span>
          </div>
          <div className="mt-6 space-y-4">
            {[
              { title: "Senior Product Manager, AI Hiring", company: "ArcLabs", score: "92%", detail: "Strong product + AI overlap, low competition" },
              { title: "Founding PM, Workforce Automation", company: "TalentOS", score: "88%", detail: "Great narrative fit, needs sharper domain proof" },
              { title: "AI Operations Lead", company: "Northstar", score: "84%", detail: "Excellent operational match, higher seniority gap" },
            ].map((job) => (
              <article key={job.title} className="rounded-2xl border border-slate-200 p-5 transition hover:border-slate-300 hover:bg-slate-50/80">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="font-semibold text-slate-950">{job.title}</h3>
                    <p className="mt-1 text-sm text-slate-500">{job.company}</p>
                  </div>
                  <span className="rounded-full bg-slate-950 px-3 py-1 text-xs font-semibold text-white">{job.score}</span>
                </div>
                <p className="mt-4 text-sm leading-6 text-slate-600">{job.detail}</p>
              </article>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <section className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Pipeline</p>
            <div className="mt-5 space-y-4">
              {[
                ["Applied", 12],
                ["OA", 4],
                ["Interview", 3],
                ["Offer", 1],
              ].map(([label, value]) => (
                <div key={label as string}>
                  <div className="mb-2 flex items-center justify-between text-sm">
                    <span className="font-medium text-slate-700">{label as string}</span>
                    <span className="text-slate-500">{value as number}</span>
                  </div>
                  <div className="h-2 rounded-full bg-slate-100">
                    <div className="h-2 rounded-full bg-slate-950" style={{ width: `${Math.max(12, (value as number) * 12)}%` }} />
                  </div>
                </div>
              ))}
            </div>
          </section>

          <section className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">Today</p>
            <div className="mt-5 space-y-4 text-sm text-slate-600">
              <div className="rounded-2xl bg-slate-50 p-4">Tailor resume for ArcLabs and review keyword deltas.</div>
              <div className="rounded-2xl bg-slate-50 p-4">Approve recruiter DM for TalentOS and queue the follow-up.</div>
              <div className="rounded-2xl bg-slate-50 p-4">Check company health for Northstar before drafting outreach.</div>
            </div>
          </section>
        </div>
      </section>
    </div>
  );
}
