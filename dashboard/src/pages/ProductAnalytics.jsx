import React from 'react';
import { Package, BarChart2, Layers } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ProductAnalytics({ metrics }) {
  const abcData = metrics?.abc_breakdown || [
    { abc_class: "A (Top 80% Rev)", count: 18, sum: 29434137.54 },
    { abc_class: "B (Next 15% Rev)", count: 24, sum: 5518900.80 },
    { abc_class: "C (Bottom 5% Rev)", count: 76, sum: 1839633.59 }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Product & ABC Inventory Analysis</h2>
          <p className="text-sm text-[var(--text-muted)]">Pareto classification, product velocity, and SKU optimization.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {abcData.map((item, idx) => (
          <div key={idx} className="glass-card p-6">
            <div className="text-xs font-bold uppercase text-sky-500">{item.abc_class}</div>
            <div className="text-2xl font-extrabold mt-2">${(item.sum / 1e6).toFixed(2)}M</div>
            <div className="text-xs text-[var(--text-muted)] mt-1">
              SKU Count: <strong className="text-[var(--text-main)]">{item.count} Products</strong>
            </div>
          </div>
        ))}
      </div>

      <div className="glass-card p-6">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <Layers className="w-5 h-5 mr-2 text-sky-500" /> Pareto Revenue Contribution ($)
        </h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={abcData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="abc_class" stroke="var(--text-muted)" />
              <YAxis stroke="var(--text-muted)" tickFormatter={(val) => `$${(val/1e6).toFixed(1)}M`} />
              <Tooltip formatter={(val) => `$${val.toLocaleString()}`} />
              <Bar dataKey="sum" fill="#38bdf8" radius={[4, 4, 0, 0]} name="Total Revenue" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
