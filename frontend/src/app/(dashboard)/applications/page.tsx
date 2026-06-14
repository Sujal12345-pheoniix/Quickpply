import { FileText } from "lucide-react";

import { FeaturePage } from "@/components/dashboard/feature-page";

export default function ApplicationsPage() {
  return (
    <FeaturePage
      eyebrow="Application Tracker"
      title="Track every application through a human approval workflow"
      description="Generated packs stay in review until the user approves each submission and records the final status."
      icon={FileText}
      metrics={[
        { label: "Pending review", value: "4", detail: "Generated packs waiting for human approval." },
        { label: "Submitted", value: "17", detail: "Manually confirmed applications already sent." },
        { label: "Follow-ups", value: "6", detail: "Queued nudges and outreach reminders." },
      ]}
      insights={[
        { title: "State machine", description: "Applied, OA, interview, rejected, and offer are first-class states with auditability." },
        { title: "Approval gate", description: "AI drafts the pack, but the user decides what gets copied, edited, and submitted." },
      ]}
      primaryAction="Generate application"
      secondaryAction="Review queue"
    />
  );
}