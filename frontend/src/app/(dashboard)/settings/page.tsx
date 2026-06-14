import { ShieldCheck } from "lucide-react";

import { FeaturePage } from "@/components/dashboard/feature-page";

export default function SettingsPage() {
  return (
    <FeaturePage
      eyebrow="Platform Settings"
      title="Control billing, notifications, integrations, and safety rails"
      description="Keep the app aligned with user consent, quota management, and the operational guardrails needed for production use."
      icon={ShieldCheck}
      metrics={[
        { label: "Integrations", value: "6", detail: "Clerk, Stripe, Sentry, PostHog, Pinecone, and email integrations." },
        { label: "Safety checks", value: "Always on", detail: "Human approval, audit trails, and quota controls remain active." },
        { label: "Plan status", value: "Pro", detail: "Billing and usage are visible in one place." },
      ]}
      insights={[
        { title: "Production readiness", description: "Settings is where admin-grade control lives: auth, billing, notifications, and observability." },
        { title: "Trust boundary", description: "Users can see exactly what the platform is allowed to do and what remains manual." },
      ]}
      primaryAction="Open billing"
      secondaryAction="Update preferences"
    />
  );
}