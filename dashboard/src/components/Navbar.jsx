import React from 'react';
import { Sun, Moon, ShieldCheck, Activity } from 'lucide-react';

export default function Navbar({ darkMode, setDarkMode, activePage }) {
  return (
    <header className="h-16 border-b border-[var(--border-color)] bg-[var(--bg-card)] px-6 flex items-center justify-between sticky top-0 z-50">
      <div className="flex items-center space-x-3">
        <div className="w-9 h-9 rounded-lg bg-sky-500 flex items-center justify-center text-white font-bold shadow-md">
          DC
        </div>
        <div>
          <h1 className="font-bold text-lg leading-none">DataCo Global</h1>
          <p className="text-xs text-[var(--text-muted)] font-medium mt-0.5">Supply Chain Executive Intelligence</p>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <div className="hidden md:flex items-center space-x-2 bg-emerald-500/10 text-emerald-500 px-3 py-1 rounded-full text-xs font-semibold">
          <Activity className="w-3.5 h-3.5 animate-pulse" />
          <span>System Status: Analytics Engine Active</span>
        </div>

        <button
          onClick={() => setDarkMode(!darkMode)}
          className="p-2 rounded-lg border border-[var(--border-color)] hover:bg-[var(--border-color)] transition-colors"
          title="Toggle Dark/Light Mode"
        >
          {darkMode ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-slate-700" />}
        </button>
      </div>
    </header>
  );
}
