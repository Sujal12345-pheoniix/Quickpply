"use client";

import { useEffect, useState } from "react";
import { UserRound, Upload, Loader2, CheckCircle, Brain, MapPin, Briefcase } from "lucide-react";

type Profile = {
  full_name: string;
  headline: string;
  summary: string;
  years_experience: number;
  current_title: string;
  current_company: string;
  location: string;
  willing_to_relocate: boolean;
  remote_preference: string;
  skills: string[];
};

export default function ProfilePage() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [remotePref, setRemotePref] = useState("remote");
  const [locationPref, setLocationPref] = useState("");
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/v1";

  async function loadProfile() {
    try {
      const token = await (window as any).Clerk?.session?.getToken();
      const res = await fetch(`${API_URL}/profiles`, {
        headers: {
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
      });
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
        setRemotePref(data.remote_preference || "remote");
        setLocationPref(data.location || "");
      }
    } catch (e) {
      console.error("Failed to load profile:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProfile();
  }, []);

  async function handleUpload(e: React.FormEvent) {
    e.preventDefault();
    if (!file) {
      alert("Please select a PDF resume to upload.");
      return;
    }

    setUploading(true);
    setStatusMessage("Extracting text and parsing resume with Gemini AI...");
    
    const formData = new FormData();
    formData.append("file", file);
    formData.append("remote_preference", remotePref);
    formData.append("location_preference", locationPref);

    try {
      const token = await (window as any).Clerk?.session?.getToken();
      const res = await fetch(`${API_URL}/profiles/resume`, {
        method: "POST",
        headers: {
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: formData,
      });

      if (res.ok) {
        setStatusMessage("Resume parsed successfully!");
        await loadProfile();
      } else {
        const err = await res.json();
        alert(err.detail || "Failed to parse resume.");
      }
    } catch (e) {
      console.error("Upload error:", e);
      alert("An error occurred during upload.");
    } finally {
      setUploading(false);
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
              <UserRound className="h-4 w-4 text-slate-900" />
              Candidate Profile
            </div>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight text-slate-950">Ground the AI in Real Evidence</h1>
            <p className="mt-2 text-slate-600">Upload your PDF resume to let Gemini extract your skills and calculate shortlisted chances.</p>
          </div>
        </div>
      </header>

      <div className="grid gap-8 lg:grid-cols-[1fr_1.3fr]">
        {/* Upload Form */}
        <section className="rounded-[2.5rem] border border-slate-200 bg-white p-8 shadow-sm h-fit space-y-6">
          <h2 className="text-xl font-bold text-slate-950">Upload Resume & Preferences</h2>
          
          <form onSubmit={handleUpload} className="space-y-5">
            <div>
              <label className="block text-sm font-semibold text-slate-700">Remote Preference</label>
              <select
                value={remotePref}
                onChange={(e) => setRemotePref(e.target.value)}
                className="mt-2 block w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 text-sm focus:border-slate-400 focus:outline-none"
              >
                <option value="remote">Remote Only</option>
                <option value="hybrid">Hybrid</option>
                <option value="onsite">Onsite</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700">Target Location</label>
              <input
                type="text"
                value={locationPref}
                onChange={(e) => setLocationPref(e.target.value)}
                placeholder="e.g. San Francisco, CA or Remote"
                className="mt-2 block w-full rounded-2xl border border-slate-200 bg-slate-50 p-3 text-sm focus:border-slate-400 focus:outline-none"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-slate-700">PDF Resume</label>
              <div className="mt-2 flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-200 bg-slate-50/50 p-6 text-center hover:bg-slate-50">
                <Upload className="h-8 w-8 text-slate-400" />
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="mt-4 block w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-xs file:font-semibold file:bg-slate-950 file:text-white file:hover:bg-slate-800 cursor-pointer"
                />
                {file && <p className="mt-3 text-xs font-semibold text-slate-900">Selected: {file.name}</p>}
              </div>
            </div>

            <button
              type="submit"
              disabled={uploading}
              className="w-full inline-flex items-center justify-center gap-2 rounded-full bg-slate-950 px-6 py-3.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:opacity-50"
            >
              {uploading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  Parsing Resume...
                </>
              ) : (
                "Upload and Sync"
              )}
            </button>
          </form>

          {statusMessage && (
            <div className="rounded-2xl bg-slate-50 p-4 text-xs font-medium text-slate-600 border border-slate-100">
              {statusMessage}
            </div>
          )}
        </section>

        {/* Profile Details */}
        <section className="rounded-[2.5rem] border border-slate-200 bg-white p-8 shadow-sm space-y-6">
          <h2 className="text-xl font-bold text-slate-950">Active Core Profile</h2>

          {profile && profile.skills.length > 0 ? (
            <div className="space-y-6">
              <div>
                <h3 className="text-2xl font-bold text-slate-950">{profile.full_name}</h3>
                <p className="mt-1 text-sm font-semibold text-slate-500">{profile.headline}</p>
                <div className="mt-3 flex flex-wrap gap-4 text-xs text-slate-500">
                  <span className="flex items-center gap-1">
                    <MapPin className="h-3.5 w-3.5" />
                    {profile.location} ({profile.remote_preference})
                  </span>
                  <span className="flex items-center gap-1">
                    <Briefcase className="h-3.5 w-3.5" />
                    {profile.years_experience} Years Experience
                  </span>
                </div>
              </div>

              {profile.current_company && (
                <div className="rounded-2xl border border-slate-100 bg-slate-50 p-4 text-sm">
                  <span className="font-semibold text-slate-500">Current Role:</span>{" "}
                  <span className="font-bold text-slate-900">
                    {profile.current_title} at {profile.current_company}
                  </span>
                </div>
              )}

              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Professional Summary</h4>
                <p className="mt-2 text-sm leading-6 text-slate-600">{profile.summary}</p>
              </div>

              <div>
                <h4 className="text-xs font-semibold uppercase tracking-wider text-slate-400">Skills Index ({profile.skills.length})</h4>
                <div className="mt-3 flex flex-wrap gap-2">
                  {profile.skills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white shadow-sm border border-slate-800"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <Brain className="h-12 w-12 text-slate-300" />
              <p className="mt-4 text-slate-600 font-medium">Your profile is currently empty.</p>
              <p className="mt-1 text-sm text-slate-400 max-w-sm">
                Upload your resume on the left to let Gemini parse it and start matching against active job listings.
              </p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}