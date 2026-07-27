import React from 'react';
import { Boxes, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function InventoryAnalytics({ metrics }) {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Inventory Utilization & Demand Velocity</h2>
          <p className="text-sm text-[var(--text-muted)]">Stock availability, backorder risk indicators, and reorder threshold analytics.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold uppercase text-[var(--text-muted)]">Inventory Turn Rate</span>
            <Boxes className="w-5 h-5 text-sky-500" />
          </div>
          <div className="text-3xl font-extrabold mt-2">8.4x</div>
          <div className="text-xs text-emerald-500 mt-1 font-semibold">Optimal Stock Velocity</div>
        </div>

        <div className="glass-card p-6">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold uppercase text-[var(--text-muted)]">Backorder Risk Score</span>
            <AlertTriangle className="w-5 h-5 text-amber-500" />
          </div>
          <div className="text-3xl font-extrabold text-amber-500 mt-2">12.5%</div>
          <div className="text-xs text-[var(--text-muted)] mt-1">High Demand Categories</div>
        </div>

        <div className="glass-card p-6">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold uppercase text-[var(--text-muted)]">Product Availability</span>
            <CheckCircle2 className="w-5 h-5 text-emerald-500" />
          </div>
          <div className="text-3xl font-extrabold text-emerald-500 mt-2">96.2%</div>
          <div className="text-xs text-[var(--text-muted)] mt-1">SLA Compliant</div>
        </div>
      </div>
    </div>
  );
}
