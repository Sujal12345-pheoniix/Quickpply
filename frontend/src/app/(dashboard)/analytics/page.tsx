import { LineChart } from "lucide-react";

import { FeaturePage } from "@/components/dashboard/feature-page";

export default function AnalyticsPage() {
  return (
    <FeaturePage
      eyebrow="Market Intelligence"
      title="See the market signals behind every role"
      description="Estimate salary, hiring velocity, competition, and company health so users spend time on the best bets."
      icon={LineChart}
      metrics={[
        { label: "Company health score", value: "82", detail: "Funding, hiring pace, and public signal analysis combined." },
        { label: "Velocity index", value: "High", detail: "Indicates how quickly a team is staffing the role." },
        { label: "Salary confidence", value: "Medium", detail: "Derived from postings, market ranges, and peer signals." },
      ]}
      insights={[
        { title: "Decision layer", description: "Useful for prioritization, not just curiosity. It helps users target the highest-return opportunities." },
        { title: "Competitive context", description: "Role competitiveness and company momentum shape whether to apply, network, or wait." },
      ]}
      primaryAction="Open report"
      secondaryAction="Compare roles"
    />
  );
}