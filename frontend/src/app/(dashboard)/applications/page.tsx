"use client";

import { useEffect, useState } from "react";
import { BadgeCheck, CheckCircle2, ChevronRight, FileText, Loader2, Play, Sparkles } from "lucide-react";
import { api } from "@/lib/api-client";

type Application = {
  id: string;
  job_id: string;
  job_title: string;
  company: string;
  status: string;
  ats_score: number;
  updated_at: string | null;
};

export default function ApplicationsPage() {
  const [apps, setApps] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);
  const [actioningId, setActioningId] = useState<string | null>(null);

  async function loadApplications() {
    try {
      const res = await api.applications.list();
      setApps(res.data);
    } catch (e) {
      console.error("Failed to load applications:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadApplications();
  }, []);

  async function handleApprove(id: string) {
    setActioningId(id);
    try {
      await api.applications.approve(id);
      await loadApplications();
    } catch (e) {
      console.error("Failed to approve application:", e);
      alert("Error approving application.");
    } finally {
      setActioningId(null);
    }
  }

  async function handleSubmit(id: string) {
    setActioningId(id);
    try {
      // Direct call to submit route using fetch wrapper
      const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/v1";
      const token = await (window as any).Clerk?.session?.getToken();
      await fetch(`${API_URL}/applications/${id}/submit`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
      });
      await loadApplications();
    } catch (e) {
      console.error("Failed to submit application:", e);
      alert("Error submitting application.");
    } finally {
      setActioningId(null);
    }
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
              <BadgeCheck className="h-4 w-4 text-slate-900" />
              Human-in-the-Loop Approval Layer
            </div>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight text-slate-950">Application Queue</h1>
            <p className="mt-2 text-slate-600">Review tailored assets and approve them. AI will never auto-submit without your authorization.</p>
          </div>
        </div>
      </header>

      {apps.length === 0 ? (
        <div className="rounded-[2rem] border border-dashed border-slate-300 p-12 text-center bg-white shadow-sm">
          <p className="text-slate-600">You haven't generated any application packs yet.</p>
          <p className="mt-2 text-sm text-slate-400">Head over to the Jobs section to find a job and click "Generate Application Pack".</p>
        </div>
      ) : (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-slate-950">Active Applications ({apps.length})</h2>
          <div className="grid gap-4">
            {apps.map((app) => (
              <div
                key={app.id}
                className="flex flex-col gap-4 rounded-[2rem] border border-slate-200 bg-white p-6 shadow-sm sm:flex-row sm:items-center sm:justify-between transition hover:shadow-md"
              >
                <div className="flex items-center gap-4">
                  <div className="rounded-2xl bg-slate-50 p-3">
                    <FileText className="h-6 w-6 text-slate-600" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-slate-950">{app.job_title}</h3>
                    <p className="text-sm text-slate-500">{app.company}</p>
                    <div className="mt-2 flex items-center gap-3">
                      <span
                        className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                          app.status === "pending_review"
                            ? "bg-amber-50 text-amber-700 border border-amber-200"
                            : app.status === "approved"
                            ? "bg-blue-50 text-blue-700 border border-blue-200"
                            : "bg-emerald-50 text-emerald-700 border border-emerald-200"
                        }`}
                      >
                        {app.status.replace("_", " ")}
                      </span>
                      <span className="text-xs text-slate-400">ATS Score: {app.ats_score}%</span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 sm:self-center">
                  {app.status === "pending_review" && (
                    <button
                      disabled={actioningId !== null}
                      onClick={() => handleApprove(app.id)}
                      className="inline-flex items-center gap-2 rounded-full bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:opacity-50"
                    >
                      {actioningId === app.id ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <CheckCircle2 className="h-4 w-4" />
                      )}
                      Approve Materials
                    </button>
                  )}

                  {app.status === "approved" && (
                    <button
                      disabled={actioningId !== null}
                      onClick={() => handleSubmit(app.id)}
                      className="inline-flex items-center gap-2 rounded-full bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-emerald-500 disabled:opacity-50"
                    >
                      {actioningId === app.id ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Play className="h-4 w-4" />
                      )}
                      Mark as Submitted
                    </button>
                  )}

                  {app.status === "submitted" && (
                    <div className="flex items-center gap-2 text-sm font-semibold text-emerald-600 pr-4">
                      <CheckCircle2 className="h-5 w-5" />
                      Applied
                    </div>
                  )}

                  <ChevronRight className="h-5 w-5 text-slate-400" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}