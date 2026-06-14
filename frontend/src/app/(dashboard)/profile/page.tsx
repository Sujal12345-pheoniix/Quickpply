import { UserRound } from "lucide-react";

import { FeaturePage } from "@/components/dashboard/feature-page";

export default function ProfilePage() {
  return (
    <FeaturePage
      eyebrow="Candidate Profile"
      title="Keep the system grounded in real experience"
      description="Store resume history, target roles, positioning notes, and the factual evidence the AI can safely use."
      icon={UserRound}
      metrics={[
        { label: "Profile completeness", value: "92%", detail: "Core evidence, preferences, and target roles are captured." },
        { label: "Resume versions", value: "6", detail: "Tailored outputs remain tied to the user’s base source of truth." },
        { label: "Target roles", value: "3", detail: "The platform optimizes around a focused search strategy." },
      ]}
      insights={[
        { title: "Single source of truth", description: "The profile drives matching, tailoring, and outreach. That keeps generated content consistent and defensible." },
        { title: "Positioning layer", description: "Users can tune how they want to show up without compromising truthfulness." },
      ]}
      primaryAction="Edit profile"
      secondaryAction="Upload resume"
    />
  );
}