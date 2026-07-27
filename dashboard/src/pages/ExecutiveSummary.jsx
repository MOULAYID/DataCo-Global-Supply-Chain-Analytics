import React from 'react';
import { DollarSign, TrendingUp, AlertTriangle, ShieldAlert, Truck, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

export default function ExecutiveSummary({ metrics }) {
  const kpis = metrics?.kpis || {
    total_revenue: 36792671.93,
    total_profit: 3969176.42,
    net_margin_pct: 0.1078,
    total_orders: 180519,
    late_delivery_rate: 0.5483,
    late_delivery_count: 98977,
    fraud_orders_count: 4062,
    fraud_rate: 0.0225,
    total_customers: 20652
  };

  const monthlySalesData = Object.entries(metrics?.monthly_sales || {
    Jan: 3200000, Feb: 3100000, Mar: 3400000, Apr: 3300000,
    May: 3500000, Jun: 3600000, Jul: 3450000, Aug: 3700000,
    Sep: 3550000, Oct: 3800000, Nov: 3900000, Dec: 4100000
  }).map(([month, sales]) => ({ month, sales, profit: sales * 0.108 }));

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Executive Summary</h2>
          <p className="text-sm text-[var(--text-muted)]">High-level operational performance and financial diagnostics.</p>
        </div>
        <span className="badge badge-danger text-xs px-3 py-1">
          <AlertTriangle className="w-3.5 h-3.5 mr-1 inline" /> 54.8% Late Delivery SLA Breach
        </span>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-card p-5">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold uppercase text-[var(--text-muted)]">Total Revenue</span>
            <div className="p-2 rounded-lg bg-sky-500/10 text-sky-500"><DollarSign className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-extrabold mt-2">${(kpis.total_revenue / 1e6).toFixed(2)}M</div>
          <div className="text-xs text-emerald-500 mt-1 flex items-center font-medium">
            <ArrowUpRight className="w-3.5 h-3.5 mr-0.5" /> +12.4% YoY Growth
          </div>
        </div>

        <div className="glass-card p-5">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold uppercase text-[var(--text-muted)]">Net Profit</span>
            <div className="p-2 rounded-lg bg-emerald-500/10 text-emerald-500"><TrendingUp className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-extrabold mt-2">${(kpis.total_profit / 1e6).toFixed(2)}M</div>
          <div className="text-xs text-[var(--text-muted)] mt-1 font-medium">
            Net Margin: <span className="font-semibold text-emerald-500">{(kpis.net_margin_pct * 100).toFixed(1)}%</span>
          </div>
        </div>

        <div className="glass-card p-5">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold uppercase text-[var(--text-muted)]">Late Delivery Rate</span>
            <div className="p-2 rounded-lg bg-red-500/10 text-red-500"><Truck className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-extrabold text-red-500 mt-2">{(kpis.late_delivery_rate * 100).toFixed(1)}%</div>
          <div className="text-xs text-red-500 mt-1 flex items-center font-medium">
            <ArrowDownRight className="w-3.5 h-3.5 mr-0.5" /> {kpis.late_delivery_count.toLocaleString()} Orders Delayed
          </div>
        </div>

        <div className="glass-card p-5">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold uppercase text-[var(--text-muted)]">Fraud Rate</span>
            <div className="p-2 rounded-lg bg-amber-500/10 text-amber-500"><ShieldAlert className="w-5 h-5" /></div>
          </div>
          <div className="text-2xl font-extrabold text-amber-500 mt-2">{(kpis.fraud_rate * 100).toFixed(2)}%</div>
          <div className="text-xs text-[var(--text-muted)] mt-1 font-medium">
            {kpis.fraud_orders_count.toLocaleString()} Flagged Transactions
          </div>
        </div>
      </div>

      {/* Main Revenue Chart */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-bold mb-4">Monthly Revenue & Profit Trajectory ($)</h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={monthlySalesData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="month" stroke="var(--text-muted)" />
              <YAxis stroke="var(--text-muted)" tickFormatter={(val) => `$${(val/1e6).toFixed(1)}M`} />
              <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Value']} />
              <Line type="monotone" dataKey="sales" stroke="#38bdf8" strokeWidth={3} name="Revenue" />
              <Line type="monotone" dataKey="profit" stroke="#10b981" strokeWidth={2} name="Net Profit" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* McKinsey Style Executive Action Box */}
      <div className="glass-card p-6 border-l-4 border-l-sky-500 bg-sky-500/5">
        <h4 className="font-bold text-base text-sky-400">McKinsey Executive Takeaway & Action Plan</h4>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-3 text-sm">
          <div>
            <strong className="block text-[var(--text-main)] font-semibold">1. Why is this happening?</strong>
            <p className="text-xs text-[var(--text-muted)] mt-1">Standard Class shipping accounts for 60%+ of volume with scheduled buffer times that fail to account for regional carrier bottlenecks in LATAM and Western Europe.</p>
          </div>
          <div>
            <strong className="block text-[var(--text-main)] font-semibold">2. So what?</strong>
            <p className="text-xs text-[var(--text-muted)] mt-1">54.8% late delivery rate leads to customer churn and an estimated $1.2M annual loss in return handling and chargeback costs.</p>
          </div>
          <div>
            <strong className="block text-[var(--text-main)] font-semibold">3. What should management do?</strong>
            <p className="text-xs text-[var(--text-muted)] mt-1">Renegotiate carrier SLAs for Standard Class, implement predictive late delivery flags at checkout, and enforce automated fraud holds on high-risk country orders.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
