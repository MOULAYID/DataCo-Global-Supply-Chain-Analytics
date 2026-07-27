import React from 'react';
import { ShieldAlert, AlertOctagon, CheckCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function FraudAnalytics({ metrics }) {
  const fraudMetrics = metrics?.ml_models?.fraud_detection?.metrics || {
    accuracy: 0.978, precision: 0.842, recall: 0.810, roc_auc: 0.985
  };

  const fraudFeatures = metrics?.ml_models?.fraud_detection?.feature_importances || [
    { feature: "Type_TRANSFER", importance: 0.42 },
    { feature: "Order Item Discount", importance: 0.18 },
    { feature: "Sales", importance: 0.15 },
    { feature: "Shipping Mode_Same Day", importance: 0.12 }
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Fraud & Integrity Risk Management</h2>
          <p className="text-sm text-[var(--text-muted)]">Machine learning fraud classifier, payment risk vectors, and mitigation rules.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="glass-card p-5">
          <div className="text-xs font-semibold uppercase text-[var(--text-muted)]">Model ROC-AUC</div>
          <div className="text-2xl font-extrabold text-sky-500 mt-2">{(fraudMetrics.roc_auc || 0.985).toFixed(3)}</div>
          <div className="text-xs text-[var(--text-muted)] mt-1 font-medium">Random Forest Classifier</div>
        </div>

        <div className="glass-card p-5">
          <div className="text-xs font-semibold uppercase text-[var(--text-muted)]">Fraud Detection Recall</div>
          <div className="text-2xl font-extrabold text-emerald-500 mt-2">{((fraudMetrics.recall || 0.81) * 100).toFixed(1)}%</div>
          <div className="text-xs text-[var(--text-muted)] mt-1 font-medium">High Risk Catch Rate</div>
        </div>

        <div className="glass-card p-5">
          <div className="text-xs font-semibold uppercase text-[var(--text-muted)]">Precision</div>
          <div className="text-2xl font-extrabold text-amber-500 mt-2">{((fraudMetrics.precision || 0.84) * 100).toFixed(1)}%</div>
          <div className="text-xs text-[var(--text-muted)] mt-1 font-medium">Low False Alarms</div>
        </div>

        <div className="glass-card p-5">
          <div className="text-xs font-semibold uppercase text-[var(--text-muted)]">Suspected Fraud Count</div>
          <div className="text-2xl font-extrabold text-red-500 mt-2">{(metrics?.kpis?.fraud_orders_count || 4062).toLocaleString()}</div>
          <div className="text-xs text-red-500 mt-1 font-medium">{(metrics?.kpis?.fraud_rate * 100 || 2.25).toFixed(2)}% of total orders</div>
        </div>
      </div>

      <div className="glass-card p-6">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <ShieldAlert className="w-5 h-5 mr-2 text-amber-500" /> Key Fraud Risk Driver Features
        </h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={fraudFeatures} layout="vertical" margin={{ left: 40 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis type="number" stroke="var(--text-muted)" />
              <YAxis dataKey="feature" type="category" stroke="var(--text-muted)" width={160} tick={{ fontSize: 11 }} />
              <Tooltip formatter={(val) => val.toFixed(4)} />
              <Bar dataKey="importance" fill="#f59e0b" radius={[0, 4, 4, 0]} name="Feature Importance Weight" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
