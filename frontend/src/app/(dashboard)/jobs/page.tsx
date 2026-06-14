"use client";

import { useEffect, useState } from "react";
import { BriefcaseBusiness, CheckCircle, Loader2, Sparkles, MapPin, ExternalLink } from "lucide-react";
import { api } from "@/lib/api-client";

type Job = {
  id: string;
  title: string;
  company: string;
  location: string;
  source: string;
  match_score: number;
  interview_probability: number;
  salary_range: string;
  posted_at: string;
};

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [selectedJob, setSelectedJob] = useState<Job | null>(null);
  const [loading, setLoading] = useState(true);
  const [generatingId, setGeneratingId] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  useEffect(() => {
    async function loadJobs() {
      try {
        const res = await api.jobs.list();
        setJobs(res.data);
        if (res.data.length > 0) {
          setSelectedJob(res.data[0]);
        }
      } catch (e) {
        console.error("Failed to load jobs:", e);
      } finally {
        setLoading(false);
      }
    }
    loadJobs();
  }, []);

  async function handleApply(jobId: string) {
    setGeneratingId(jobId);
    setSuccessMessage(null);
    try {
      const res = await api.applications.generate(jobId);
      setSuccessMessage("Application pack generated successfully! Go to Applications to review.");
    } catch (e) {
      console.error("Failed to generate application:", e);
      alert("Error generating application pack. Please try again.");
    } finally {
      setGeneratingId(null);
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
              <BriefcaseBusiness className="h-4 w-4 text-slate-900" />
              Job Intelligence Engine
            </div>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight text-slate-950">Discover Your High-Fit Roles</h1>
            <p className="mt-2 text-slate-600">Simulating applications exactly like a top candidate would.</p>
          </div>
        </div>
      </header>

      {successMessage && (
        <div className="flex items-center gap-3 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-emerald-800">
          <CheckCircle className="h-5 w-5 flex-shrink-0 text-emerald-600" />
          <p className="text-sm font-medium">{successMessage}</p>
        </div>
      )}

      {jobs.length === 0 ? (
        <div className="rounded-[2rem] border border-dashed border-slate-300 p-12 text-center">
          <p className="text-slate-600">No jobs found matching your criteria.</p>
        </div>
      ) : (
        <div className="grid gap-8 lg:grid-cols-[1fr_1.2fr]">
          {/* Job List */}
          <div className="space-y-4">
            <h2 className="text-lg font-semibold text-slate-950">Available Openings ({jobs.length})</h2>
            <div className="space-y-3 max-h-[65vh] overflow-y-auto pr-2">
              {jobs.map((job) => (
                <div
                  key={job.id}
                  onClick={() => setSelectedJob(job)}
                  className={`cursor-pointer rounded-2xl border p-5 transition ${
                    selectedJob?.id === job.id
                      ? "border-slate-950 bg-slate-900 text-white shadow-md"
                      : "border-slate-200 bg-white hover:border-slate-300 hover:bg-slate-50/50"
                  }`}
                >
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <h3 className={`font-semibold ${selectedJob?.id === job.id ? "text-white" : "text-slate-950"}`}>
                        {job.title}
                      </h3>
                      <p className={`mt-1 text-sm ${selectedJob?.id === job.id ? "text-slate-400" : "text-slate-500"}`}>
                        {job.company}
                      </p>
                    </div>
                    <span
                      className={`rounded-full px-3 py-1 text-xs font-bold ${
                        selectedJob?.id === job.id ? "bg-white/10 text-white" : "bg-slate-950 text-white"
                      }`}
                    >
                      {job.match_score}% Match
                    </span>
                  </div>

                  <div className="mt-4 flex items-center gap-4 text-xs">
                    <span className="flex items-center gap-1">
                      <MapPin className="h-3 w-3" />
                      {job.location}
                    </span>
                    <span>{job.salary_range}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Job Detail Column */}
          {selectedJob && (
            <div className="sticky top-24 rounded-[2.5rem] border border-slate-200 bg-white p-8 shadow-sm h-fit">
              <div className="flex items-start justify-between gap-6">
                <div>
                  <h2 className="text-2xl font-bold tracking-tight text-slate-950">{selectedJob.title}</h2>
                  <p className="mt-1 text-lg font-medium text-slate-500">{selectedJob.company}</p>
                </div>
                <span className="rounded-full bg-slate-950 px-4 py-2 text-sm font-bold text-white">
                  {selectedJob.match_score}% Fit
                </span>
              </div>

              <div className="mt-6 flex flex-wrap items-center gap-6 text-sm text-slate-600">
                <span className="flex items-center gap-1.5">
                  <MapPin className="h-4 w-4 text-slate-400" />
                  {selectedJob.location}
                </span>
                <span className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium uppercase text-slate-500">
                  {selectedJob.source}
                </span>
                <span className="font-semibold text-slate-950">{selectedJob.salary_range}</span>
              </div>

              <hr className="my-6 border-slate-100" />

              <div className="space-y-6">
                <div>
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">Match Insights</h3>
                  <div className="mt-3 grid gap-3 sm:grid-cols-2">
                    <div className="rounded-2xl bg-slate-50 p-4">
                      <p className="text-xs font-medium text-slate-500">Interview probability</p>
                      <p className="mt-1 text-xl font-bold text-slate-950">{selectedJob.interview_probability}%</p>
                    </div>
                    <div className="rounded-2xl bg-slate-50 p-4">
                      <p className="text-xs font-medium text-slate-500">Suggested Action</p>
                      <p className="mt-1 text-xl font-bold text-emerald-600">Strong Apply</p>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-400">About the Role</h3>
                  <p className="mt-3 text-sm leading-6 text-slate-600">
                    ApplyPilot's matching engine has detected high keyword alignment with your experience in multi-agent orchestrations, Python pipelines, and database tuning.
                  </p>
                </div>

                <div className="flex gap-4 pt-4">
                  <button
                    disabled={generatingId !== null}
                    onClick={() => handleApply(selectedJob.id)}
                    className="flex-1 inline-flex items-center justify-center gap-2 rounded-full bg-slate-950 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:opacity-50"
                  >
                    {generatingId === selectedJob.id ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin" />
                        Generating Pack...
                      </>
                    ) : (
                      <>
                        <Sparkles className="h-4 w-4" />
                        Generate Application Pack
                      </>
                    )}
                  </button>
                  <a
                    href="https://applypilot.ai"
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center justify-center rounded-full border border-slate-300 bg-white px-5 py-3.5 text-sm font-semibold text-slate-700 transition hover:border-slate-400 hover:text-slate-950"
                  >
                    <ExternalLink className="h-4 w-4" />
                  </a>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}