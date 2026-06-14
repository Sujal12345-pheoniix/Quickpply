import { MicVocal } from "lucide-react";

import { FeaturePage } from "@/components/dashboard/feature-page";

export default function InterviewPage() {
  return (
    <FeaturePage
      eyebrow="Interview Coach"
      title="Prepare for screeners, OA, and final rounds with targeted coaching"
      description="Turn job analysis into mock interview questions, structured answers, and feedback loops specific to the role."
      icon={MicVocal}
      metrics={[
        { label: "Practice rounds", value: "24", detail: "Simulated interviews tied to role level and company type." },
        { label: "Answer frameworks", value: "6", detail: "STAR, leadership stories, trade-offs, and case reasoning." },
        { label: "Feedback signals", value: "11", detail: "Clarity, specificity, confidence, and risk flags." },
      ]}
      insights={[
        { title: "Role-aware practice", description: "Questions are grounded in the actual job description, not generic interview trivia." },
        { title: "Reinforcement", description: "The coach surfaces weak spots so users can improve before the real interview begins." },
      ]}
      primaryAction="Start mock interview"
      secondaryAction="Review answers"
    />
  );
}