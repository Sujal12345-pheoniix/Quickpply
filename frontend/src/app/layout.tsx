import type { Metadata } from "next";
import { Space_Grotesk } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";

const spaceGrotesk = Space_Grotesk({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ApplyPilot AI — Get More Interviews, Not Spam",
  description:
    "AI that applies to jobs exactly like a top candidate would. Human-approved applications with ATS-optimized resumes.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={spaceGrotesk.className}>{children}</body>
      </html>
    </ClerkProvider>
  );
}
