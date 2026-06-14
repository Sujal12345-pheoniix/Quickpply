"use client";

import { useEffect, useState } from "react";
import { MessageSquareText, Loader2, Copy, CheckCircle, Send, FileText } from "lucide-react";

type Application = {
  id: string;
  job_title: string;
  company: string;
  status: string;
};

export default function OutreachPage() {
  const [apps, setApps] = useState<Application[]>([]);
  const [selectedAppId, setSelectedAppId] = useState("");
  const [recipientName, setRecipientName] = useState("");
  const [recipientTitle, setRecipientTitle] = useState("");
  const [channel, setChannel] = useState("linkedin_dm");
  const [attachResume, setAttachResume] = useState(true);
  
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [generatedMsg, setGeneratedMsg] = useState("");
  const [copied, setCopied] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/v1";

  async function loadApplications() {
    try {
      const token = await (window as any).Clerk?.session?.getToken();
      const res = await fetch(`${API_URL}/applications`, {
        headers: {
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
      });
      if (res.ok) {
        const data = await res.json();
        setApps(data.data);
        if (data.data.length > 0) {
          setSelectedAppId(data.data[0].id);
        }
      }
    } catch (e) {
      console.error("Failed to load applications:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadApplications();
  }, []);

  async function handleGenerate(e: React.FormEvent) {
    e.preventDefault();
    if (!selectedAppId) {
      alert("Please select a target application/company first.");
      return;
    }
    if (!recipientName) {
      alert("Please enter the recruiter's name.");
      return;
    }

    setGenerating(true);
    setGeneratedMsg("");
    setCopied(false);

    try {
      const token = await (window as any).Clerk?.session?.getToken();
      const res = await fetch(`${API_URL}/outreach/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({
          application_id: selectedAppId,
          recipient_name: recipientName,
          recipient_title: recipientTitle,
          channel: channel,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        setGeneratedMsg(data.message);
      } else {
        const err = await res.json();
        alert(err.detail || "Failed to generate outreach message.");
      }
    } catch (e) {
      console.error("Outreach generation error:", e);
      alert("An error occurred during generation.");
    } finally {
      setGenerating(false);
    }
  }

  function handleCopy() {
    navigator.clipboard.writeText(generatedMsg);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  if (loading) {
    return (
      <div className="flex h-[60vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-slate-600" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <header className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-sm">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full bg-slate-50 border border-slate-200 px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] text-slate-500">
              <MessageSquareText className="h-4 w-4 text-slate-900" />
              Networking Engine
            </div>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight text-slate-950">Cold DM & Recruiter Outreach</h1>
            <p className="mt-2 text-slate-600">Draft personalized, high-conversion messages targeting HR personnel with your resume attached.</p>
          </div>
        </div>
      </header>

      {apps.length === 0 ? (
        <div className="rounded-[2rem] border border-dashed border-slate-300 p-12 text-center bg-white shadow-sm">
          <p className="text-slate-600">You must create at least one application pack first to target a company.</p>
          <p className="mt-2 text-sm text-slate-400">Please go to the Jobs dashboard, select a role, and click "Generate Application Pack".</p>
        </div>
      ) : (
        <div className="grid gap-8 lg:grid-cols-[1fr_1.3fr]">
          {/* Form */}
          <section className="rounded-[2.5rem] border border-slate-200 bg-white p-8 shadow-sm h-fit space-y-6">
            <h2 className="text-xl font-bold text-slate-950">Draft Cold Outreach</h2>

            <form onSubmit={handleGenerate} className="space-y-5">
              <div>
                <label className="block text-sm font-semibold text-slate-700">Target Role & Company</label>
                <select
                  value={selectedAppId}
                  onChange={(e) => setSelectedAppId(e.target.value)}
                  className="mt-2 block w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 text-sm focus:border-slate-400 focus:outline-none"
                >
                  {apps.map((app) => (
                    <option key={app.id} value={app.id}>
                      {app.job_title} at {app.company} ({app.status})
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700">Recruiter / HR Name</label>
                <input
                  type="text"
                  required
                  value={recipientName}
                  onChange={(e) => setRecipientName(e.target.value)}
                  placeholder="e.g. Sarah Jennings"
                  className="mt-2 block w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 text-sm focus:border-slate-400 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700">Recruiter Title</label>
                <input
                  type="text"
                  value={recipientTitle}
                  onChange={(e) => setRecipientTitle(e.target.value)}
                  placeholder="e.g. Technical Recruiter or Engineering Manager"
                  className="mt-2 block w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 text-sm focus:border-slate-400 focus:outline-none"
                />
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700">Channel</label>
                <select
                  value={channel}
                  onChange={(e) => setChannel(e.target.value)}
                  className="mt-2 block w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 text-sm focus:border-slate-400 focus:outline-none"
                >
                  <option value="linkedin_dm">LinkedIn DM</option>
                  <option value="email">Cold Email</option>
                </select>
              </div>

              <div className="flex items-center gap-2 py-1">
                <input
                  type="checkbox"
                  id="attach"
                  checked={attachResume}
                  onChange={(e) => setAttachResume(e.target.checked)}
                  className="rounded border-slate-300 text-slate-950 focus:ring-slate-950 h-4 w-4"
                />
                <label htmlFor="attach" className="text-sm font-medium text-slate-600 flex items-center gap-1.5 cursor-pointer">
                  <FileText className="h-4 w-4 text-slate-400" />
                  Attach Active PDF Resume
                </label>
              </div>

              <button
                type="submit"
                disabled={generating}
                className="w-full inline-flex items-center justify-center gap-2 rounded-full bg-slate-950 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:opacity-50"
              >
                {generating ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Drafting Message...
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4" />
                    Generate Message
                  </>
                )}
              </button>
            </form>
          </section>

          {/* Generated Box */}
          <section className="rounded-[2.5rem] border border-slate-200 bg-white p-8 shadow-sm space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-slate-950">Review Generated Message</h2>
              {generatedMsg && (
                <button
                  onClick={handleCopy}
                  className="inline-flex items-center gap-1.5 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold text-slate-600 hover:bg-slate-50 transition"
                >
                  {copied ? (
                    <>
                      <CheckCircle className="h-3.5 w-3.5 text-emerald-600" />
                      Copied
                    </>
                  ) : (
                    <>
                      <Copy className="h-3.5 w-3.5" />
                      Copy
                    </>
                  )}
                </button>
              )}
            </div>

            {generatedMsg ? (
              <div className="space-y-4">
                <textarea
                  readOnly
                  value={generatedMsg}
                  className="w-full h-[40vh] p-5 rounded-3xl border border-slate-200 bg-slate-50 text-sm leading-6 text-slate-700 font-mono focus:outline-none resize-none"
                />
                
                {attachResume && (
                  <div className="flex items-center gap-2.5 rounded-2xl border border-emerald-200 bg-emerald-50/50 p-4 text-sm text-emerald-800">
                    <FileText className="h-5 w-5 text-emerald-600" />
                    <span>Your active PDF resume is marked as attached to this outreach.</span>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-20 text-center text-slate-400">
                <MessageSquareText className="h-12 w-12 text-slate-300" />
                <p className="mt-4 font-medium">No message drafted yet.</p>
                <p className="mt-1 text-xs max-w-xs">
                  Fill in the recruiter details on the left and click generate to draft a custom message with your resume attached.
                </p>
              </div>
            )}
          </section>
        </div>
      )}
    </div>
  );
}