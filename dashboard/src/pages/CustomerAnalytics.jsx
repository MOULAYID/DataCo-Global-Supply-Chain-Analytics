import React from 'react';
import { Users, Award, UserCheck, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function CustomerAnalytics({ metrics }) {
  const defaultProfiles = [
    { segment_name: "Champions / VIPs", customer_count: 7571, mean_monetary: 3572.16, mean_clv: 1749.97 },
    { segment_name: "Loyal Customers", customer_count: 4649, mean_monetary: 1555.06, mean_clv: 518.23 },
    { segment_name: "At-Risk Buyers", customer_count: 5947, mean_monetary: 395.99, mean_clv: 1468.35 },
    { segment_name: "Low-Value / Lost", customer_count: 2485, mean_monetary: 62.59, mean_clv: 562.86 }
  ];

  const rawProfiles = metrics?.ml_models?.customer_rfm?.cluster_profiles || defaultProfiles;

  const segmentNameMap = { 1: "Champions / VIPs", 3: "Loyal Customers", 0: "At-Risk Buyers", 2: "Low-Value / Lost" };

  const rfmData = rawProfiles.map((item, idx) => ({
    ...item,
    segment_name: item.segment_name || segmentNameMap[item.cluster] || `Segment ${item.cluster}`,
    spend: parseFloat((item.mean_monetary || 0).toFixed(2)),
    clv: parseFloat((item.mean_clv || 0).toFixed(2)),
    count: item.customer_count || 0
  })).sort((a, b) => b.spend - a.spend);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Customer Intelligence & RFM Segmentation</h2>
          <p className="text-sm text-[var(--text-muted)]">K-Means RFM clustering, CLV estimation, and retention targeting across 20,652 accounts.</p>
        </div>
      </div>

      {/* Cluster Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {rfmData.map((cluster, idx) => (
          <div key={idx} className="glass-card p-5 border-t-4 border-t-sky-500">
            <div className="text-xs font-semibold uppercase text-[var(--text-muted)]">{cluster.segment_name}</div>
            <div className="text-2xl font-extrabold mt-2">{cluster.count.toLocaleString()} <span className="text-xs font-normal text-[var(--text-muted)]">Users</span></div>
            <div className="text-xs text-[var(--text-muted)] mt-2 space-y-1">
              <div>Avg Spend: <strong className="text-[var(--text-main)]">${cluster.spend.toLocaleString()}</strong></div>
              <div>Estimated CLV: <strong className="text-emerald-500">${cluster.clv.toLocaleString()}</strong></div>
            </div>
          </div>
        ))}
      </div>

      {/* Customer Segment Monetary Bar Chart */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <Users className="w-5 h-5 mr-2 text-sky-500" /> Customer Segment Monetary Comparison ($)
        </h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={rfmData}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis dataKey="segment_name" stroke="var(--text-muted)" tick={{ fontSize: 11 }} />
              <YAxis stroke="var(--text-muted)" tickFormatter={(val) => `$${val.toLocaleString()}`} />
              <Tooltip formatter={(val) => [`$${val.toLocaleString()}`, 'Average Spend ($)']} />
              <Bar dataKey="spend" fill="#38bdf8" radius={[4, 4, 0, 0]} name="Average Spend per Customer ($)" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Segment Details Table */}
      <div className="glass-card overflow-hidden p-6">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <Award className="w-5 h-5 mr-2 text-emerald-500" /> RFM Segment Characteristics Matrix
        </h3>
        <table className="w-full text-left text-sm border-collapse">
          <thead>
            <tr className="border-b border-[var(--border-color)] text-[var(--text-muted)] uppercase text-xs">
              <th className="p-3">Segment Name</th>
              <th className="p-3">Customer Count</th>
              <th className="p-3">Avg Recency (Days)</th>
              <th className="p-3">Avg Order Frequency</th>
              <th className="p-3">Avg Spend ($)</th>
              <th className="p-3">Estimated CLV ($)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[var(--border-color)]">
            {rfmData.map((item, idx) => (
              <tr key={idx} className="hover:bg-[var(--border-color)]/10">
                <td className="p-3 font-semibold text-sky-400">{item.segment_name}</td>
                <td className="p-3 font-bold">{item.count.toLocaleString()}</td>
                <td className="p-3">{(item.mean_recency || 0).toFixed(0)} days</td>
                <td className="p-3">{(item.mean_frequency || 0).toFixed(1)} orders</td>
                <td className="p-3 font-semibold">${item.spend.toLocaleString()}</td>
                <td className="p-3 font-bold text-emerald-500">${item.clv.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
