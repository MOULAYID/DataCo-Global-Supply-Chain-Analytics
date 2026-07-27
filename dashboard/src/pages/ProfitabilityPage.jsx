import React from 'react';
import { DollarSign, AlertCircle, TrendingDown, ArrowRight } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ProfitabilityPage({ metrics }) {
  const topProfitCategories = Object.entries(metrics?.top_categories_profit || {
    "Corporate Apparel": 450000, "Footwear": 410000, "Fitness": 380000, "Golf": 350000, "Fan Shop": 320000
  }).map(([category, profit]) => ({ category, profit }));

  const lossCategories = Object.entries(metrics?.loss_making_categories || {
    "Electronics": -42000, "Computers": -31000, "Health & Beauty": -18000
  }).map(([category, profit]) => ({ category, profit }));

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Profitability Deep Dive</h2>
          <p className="text-sm text-[var(--text-muted)]">Margin analysis, profit leaks, and loss-making location detection.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-lg font-bold mb-4 text-emerald-500 flex items-center">
            <DollarSign className="w-5 h-5 mr-2" /> Top Net Profit Categories ($)
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topProfitCategories}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="category" stroke="var(--text-muted)" tick={{ fontSize: 11 }} />
                <YAxis stroke="var(--text-muted)" tickFormatter={(val) => `$${(val/1e3).toFixed(0)}k`} />
                <Tooltip formatter={(val) => `$${val.toLocaleString()}`} />
                <Bar dataKey="profit" fill="#10b981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-red-500">
          <h3 className="text-lg font-bold mb-4 text-red-500 flex items-center">
            <TrendingDown className="w-5 h-5 mr-2" /> Top Financial Leak / Loss Categories ($)
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={lossCategories}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="category" stroke="var(--text-muted)" tick={{ fontSize: 11 }} />
                <YAxis stroke="var(--text-muted)" tickFormatter={(val) => `$${(val/1e3).toFixed(0)}k`} />
                <Tooltip formatter={(val) => `$${val.toLocaleString()}`} />
                <Bar dataKey="profit" fill="#ef4444" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="glass-card p-6">
        <h3 className="text-lg font-bold mb-3">Profit Leakage Root Cause Analysis</h3>
        <p className="text-sm text-[var(--text-muted)]">
          Financial regression analysis indicates that <strong>Order Item Discount Rate</strong> exceeding 15% combined with <strong>Same Day / First Class air freight costs</strong> in high-distance markets (e.g. Central America, South Asia) turns otherwise profitable orders into net-negative margin transactions.
        </p>
      </div>
    </div>
  );
}
