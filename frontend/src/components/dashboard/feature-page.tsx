import type { LucideIcon } from "lucide-react";

type Metric = {
  label: string;
  value: string;
  detail: string;
};

type Insight = {
  title: string;
  description: string;
};

type FeaturePageProps = {
  eyebrow: string;
  title: string;
  description: string;
  icon: LucideIcon;
  metrics: Metric[];
  insights: Insight[];
  primaryAction: string;
  secondaryAction: string;
};

export function FeaturePage({
  eyebrow,
  title,
  description,
  icon: Icon,
  metrics,
  insights,
  primaryAction,
  secondaryAction,
}: FeaturePageProps) {
  return (
    <div className="space-y-8">
      <section className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div className="max-w-2xl">
            <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
              <Icon className="h-4 w-4 text-slate-900" />
              {eyebrow}
            </div>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight text-slate-950">{title}</h1>
            <p className="mt-4 text-slate-600">{description}</p>
          </div>
          <div className="flex gap-3">
            <button className="rounded-full bg-slate-950 px-5 py-3 text-sm font-medium text-white transition hover:bg-slate-800">
              {primaryAction}
            </button>
            <button className="rounded-full border border-slate-300 bg-white px-5 py-3 text-sm font-medium text-slate-700 transition hover:border-slate-400 hover:text-slate-950">
              {secondaryAction}
            </button>
          </div>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        {metrics.map((metric) => (
          <div key={metric.label} className="rounded-[1.5rem] border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-xs uppercase tracking-[0.24em] text-slate-500">{metric.label}</p>
            <p className="mt-3 text-3xl font-semibold text-slate-950">{metric.value}</p>
            <p className="mt-2 text-sm leading-6 text-slate-600">{metric.detail}</p>
          </div>
        ))}
      </section>

      <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-500">What this page does</p>
          <div className="mt-6 space-y-4 text-sm leading-6 text-slate-600">
            {insights.map((insight) => (
              <div key={insight.title} className="rounded-2xl bg-slate-50 p-4">
                <h3 className="font-semibold text-slate-950">{insight.title}</h3>
                <p className="mt-1">{insight.description}</p>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-[2rem] border border-slate-200 bg-slate-950 p-8 text-white shadow-[0_24px_80px_rgba(15,23,42,0.28)]">
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-400">Approval model</p>
          <h2 className="mt-3 text-2xl font-semibold">Every generated asset is reviewable before it ever leaves the platform.</h2>
          <p className="mt-4 text-sm leading-6 text-slate-300">
            This is intentionally not a spam machine. The goal is higher-quality applications, stronger recruiter signals, and tighter candidate control.
          </p>
          <div className="mt-8 rounded-3xl border border-white/10 bg-white/5 p-5 text-sm text-slate-200">
            {primaryAction} · {secondaryAction}
          </div>
        </div>
      </section>
    </div>
  );
}