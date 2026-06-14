import Link from "next/link";
import {
  LayoutDashboard,
  Briefcase,
  FileText,
  User,
  Settings,
  MessageSquare,
  BarChart3,
} from "lucide-react";

const navItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/jobs", label: "Jobs", icon: Briefcase },
  { href: "/applications", label: "Applications", icon: FileText },
  { href: "/outreach", label: "Outreach", icon: MessageSquare },
  { href: "/interview", label: "Interview Prep", icon: MessageSquare },
  { href: "/analytics", label: "Analytics", icon: BarChart3 },
  { href: "/profile", label: "Profile", icon: User },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white min-h-screen p-4 flex flex-col">
      <div className="mb-8 px-2">
        <span className="text-lg font-bold">ApplyPilot AI</span>
        <p className="text-xs text-slate-400 mt-1">Interview-focused applications</p>
      </div>
      <nav className="flex-1 space-y-1">
        {navItems.map(({ href, label, icon: Icon }) => (
          <Link
            key={href}
            href={href}
            className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-300 hover:bg-slate-800 hover:text-white"
          >
            <Icon className="w-4 h-4" />
            {label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
