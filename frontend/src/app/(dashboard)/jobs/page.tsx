import { BriefcaseBusiness } from "lucide-react";

import { FeaturePage } from "@/components/dashboard/feature-page";

export default function JobsPage() {
  return (
    <FeaturePage
      eyebrow="Job Intelligence Engine"
      title="Discover and rank jobs worth applying to"
      description="Normalize roles from multiple sources, score fit, and surface the ones that deserve human attention."
      icon={BriefcaseBusiness}
      metrics={[
        { label: "Sources connected", value: "8", detail: "Job boards and company career pages can feed the same pipeline." },
        { label: "Match threshold", value: "70+", detail: "Only roles above the target score reach the application queue." },
        { label: "Detected signals", value: "19", detail: "Skills, hidden requirements, hiring velocity, and salary clues." },
      ]}
      insights={[
        { title: "Multi-source ingestion", description: "LinkedIn, Wellfound, Naukri, Instahyre, YC Jobs, RemoteOK, Indeed, and company sites normalize into one schema." },
        { title: "Decision support", description: "Every job is enriched with company health, competitiveness, and interview probability before it ever reaches the user." },
      ]}
      primaryAction="Discover jobs"
      secondaryAction="Import from URL"
    />
  );
}