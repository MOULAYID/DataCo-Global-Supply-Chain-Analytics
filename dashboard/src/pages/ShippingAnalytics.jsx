import React from 'react';
import { Truck, Clock, AlertTriangle, PackageCheck } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ShippingAnalytics({ metrics }) {
  const shippingPerf = metrics?.shipping_performance || [
    { "Shipping Mode": "Standard Class", total_orders: 39324, late_rate: 0.3807, avg_delay: -0.004, total_profit: 2370454.45 },
    { "Shipping Mode": "First Class", total_orders: 10079, late_rate: 0.9532, avg_delay: 1.0, total_profit: 643121.92 },
    { "Shipping Mode": "Second Class", total_orders: 12778, late_rate: 0.7663, avg_delay: 1.99, total_profit: 750308.17 },
    { "Shipping Mode": "Same Day", total_orders: 3571, late_rate: 0.4574, avg_delay: 0.478, total_profit: 203018.43 }
  ];

  const chartDataLate = shippingPerf.map(d => ({
    mode: d['Shipping Mode'] || d.Shipping_Mode || d.shipping_mode || 'Unknown',
    lateRatePct: parseFloat(((d.late_rate || 0) * 100).toFixed(1)),
    orders: d.total_orders || 0
  }));

  const chartDataDelay = shippingPerf.map(d => ({
    mode: d['Shipping Mode'] || d.Shipping_Mode || d.shipping_mode || 'Unknown',
    avgDelayDays: parseFloat((d.avg_delay || 0).toFixed(2)),
    profit: parseFloat((d.total_profit || 0).toFixed(0))
  }));

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Shipping & Fulfillment Logistics</h2>
          <p className="text-sm text-[var(--text-muted)]">Shipping mode benchmarks, delay distributions, and SLA breaches.</p>
        </div>
      </div>

      {/* Metric Cards Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {chartDataLate.map((item, idx) => (
          <div key={idx} className="glass-card p-5 border-t-4 border-t-sky-500">
            <div className="text-xs font-semibold uppercase text-[var(--text-muted)]">{item.mode}</div>
            <div className="text-2xl font-extrabold mt-2 text-red-500">{item.lateRatePct}% <span className="text-xs font-normal text-[var(--text-muted)]">Late</span></div>
            <div className="text-xs text-[var(--text-muted)] mt-1 font-medium">
              Orders: <strong className="text-[var(--text-main)]">{item.orders.toLocaleString()}</strong>
            </div>
          </div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-lg font-bold mb-4 flex items-center">
            <AlertTriangle className="w-5 h-5 mr-2 text-red-500" /> Late Delivery Rate by Shipping Mode (%)
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartDataLate}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="mode" stroke="var(--text-muted)" tick={{ fontSize: 11 }} />
                <YAxis stroke="var(--text-muted)" unit="%" />
                <Tooltip formatter={(val) => [`${val}%`, 'Late Delivery Rate']} />
                <Bar dataKey="lateRatePct" fill="#ef4444" radius={[4, 4, 0, 0]} name="Late Delivery Rate (%)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-card p-6">
          <h3 className="text-lg font-bold mb-4 flex items-center">
            <Clock className="w-5 h-5 mr-2 text-amber-500" /> Average Days Delay (Real vs Scheduled)
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartDataDelay}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis dataKey="mode" stroke="var(--text-muted)" tick={{ fontSize: 11 }} />
                <YAxis stroke="var(--text-muted)" unit=" days" />
                <Tooltip formatter={(val) => [`${val} days`, 'Avg Shipping Delay']} />
                <Bar dataKey="avgDelayDays" fill="#f59e0b" radius={[4, 4, 0, 0]} name="Avg Delay (Days)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Fulfillment Table */}
      <div className="glass-card overflow-hidden p-6">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <PackageCheck className="w-5 h-5 mr-2 text-sky-500" /> Shipping Performance Matrix
        </h3>
        <table className="w-full text-left text-sm border-collapse">
          <thead>
            <tr className="border-b border-[var(--border-color)] text-[var(--text-muted)] uppercase text-xs">
              <th className="p-3">Shipping Mode</th>
              <th className="p-3">Total Orders</th>
              <th className="p-3">Late Delivery Rate</th>
              <th className="p-3">Average Delay</th>
              <th className="p-3">Net Profit Contribution</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[var(--border-color)]">
            {shippingPerf.map((item, idx) => (
              <tr key={idx} className="hover:bg-[var(--border-color)]/10">
                <td className="p-3 font-semibold">{item['Shipping Mode'] || item.Shipping_Mode}</td>
                <td className="p-3">{(item.total_orders || 0).toLocaleString()}</td>
                <td className="p-3 font-bold text-red-500">{((item.late_rate || 0) * 100).toFixed(1)}%</td>
                <td className="p-3">{(item.avg_delay || 0).toFixed(2)} days</td>
                <td className="p-3 font-semibold text-emerald-500">${(item.total_profit || 0).toLocaleString(undefined, {maximumFractionDigits: 0})}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
