import React from 'react';
import { Globe, MapPin, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function GeographyAnalytics({ metrics }) {
  const topCountries = Object.entries(metrics?.top_countries_profit || {
    "United States": 1250000, "France": 620000, "Mexico": 580000, "Germany": 540000, "United Kingdom": 490000
  }).map(([country, profit]) => ({ country, profit }));

  const lossCountries = Object.entries(metrics?.loss_making_countries || {
    "Honduras": -45000, "Nigeria": -32000, "Pakistan": -28000
  }).map(([country, profit]) => ({ country, profit }));

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Geospatial Intelligence & Regional Profitability</h2>
          <p className="text-sm text-[var(--text-muted)]">Global market mapping, profitable countries, and high-loss territory pinpointing.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="glass-card p-6">
          <h3 className="text-lg font-bold mb-4 flex items-center">
            <Globe className="w-5 h-5 mr-2 text-emerald-500" /> Top Profitable Countries ($)
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={topCountries} layout="vertical" margin={{ left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis type="number" stroke="var(--text-muted)" tickFormatter={(val) => `$${(val/1e3).toFixed(0)}k`} />
                <YAxis dataKey="country" type="category" stroke="var(--text-muted)" width={110} tick={{ fontSize: 11 }} />
                <Tooltip formatter={(val) => `$${val.toLocaleString()}`} />
                <Bar dataKey="profit" fill="#10b981" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="glass-card p-6 border-l-4 border-l-red-500">
          <h3 className="text-lg font-bold mb-4 flex items-center">
            <MapPin className="w-5 h-5 mr-2 text-red-500" /> Top Net Loss Destination Countries ($)
          </h3>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={lossCountries} layout="vertical" margin={{ left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
                <XAxis type="number" stroke="var(--text-muted)" tickFormatter={(val) => `$${(val/1e3).toFixed(0)}k`} />
                <YAxis dataKey="country" type="category" stroke="var(--text-muted)" width={110} tick={{ fontSize: 11 }} />
                <Tooltip formatter={(val) => `$${val.toLocaleString()}`} />
                <Bar dataKey="profit" fill="#ef4444" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
