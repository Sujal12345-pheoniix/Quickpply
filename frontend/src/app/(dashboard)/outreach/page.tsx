import { MessageSquareText } from "lucide-react";

import { FeaturePage } from "@/components/dashboard/feature-page";

export default function OutreachPage() {
  return (
    <FeaturePage
      eyebrow="Networking Engine"
      title="Generate recruiter outreach that sounds personal and credible"
      description="Draft LinkedIn messages, email intros, referral asks, and follow-ups tailored to the role and company context."
      icon={MessageSquareText}
      metrics={[
        { label: "Templates", value: "4", detail: "DM, email, follow-up, and referral request variants." },
        { label: "Personalized fields", value: "12", detail: "Mutual context, proof points, and role-specific hooks." },
        { label: "Approval rate", value: "100%", detail: "Nothing sends without user review." },
      ]}
      insights={[
        { title: "Tone control", description: "Messages are concise, specific, and aligned to the user’s background rather than generic recruiter spam." },
        { title: "Human workflow", description: "The platform prepares the message, the user approves it, and submission remains manual." },
      ]}
      primaryAction="Draft outreach"
      secondaryAction="Preview variations"
    />
  );
}