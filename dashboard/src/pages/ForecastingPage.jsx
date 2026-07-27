import React from 'react';
import { Cpu, TrendingUp, AlertTriangle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function ForecastingPage({ metrics }) {
  const lateFeatures = metrics?.ml_models?.late_delivery?.feature_importances || [
    { feature: "Days for shipment (scheduled)", importance: 0.48 },
    { feature: "Shipping Mode_Standard Class", importance: 0.22 },
    { feature: "Order Item Product Price", importance: 0.12 },
    { feature: "Order Region_LATAM", importance: 0.08 }
  ];

  const forecastMetrics = metrics?.ml_models?.demand_forecast || {
    rmse: 42500.5, mape: 0.084, forecast_days: 30
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">Forecasting & Predictive Machine Learning</h2>
          <p className="text-sm text-[var(--text-muted)]">30-day demand forecast, Holt-Winters time series, and Late Delivery ML classifier drivers.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6">
          <div className="text-xs font-semibold uppercase text-[var(--text-muted)]">Forecast Horizon</div>
          <div className="text-2xl font-extrabold mt-2">{forecastMetrics.forecast_days} Days Ahead</div>
          <div className="text-xs text-[var(--text-muted)] mt-1 font-medium">Holt-Winters Seasonal Model</div>
        </div>

        <div className="glass-card p-6">
          <div className="text-xs font-semibold uppercase text-[var(--text-muted)]">Forecast MAPE Error</div>
          <div className="text-2xl font-extrabold text-emerald-500 mt-2">{((forecastMetrics.mape || 0.084) * 100).toFixed(1)}%</div>
          <div className="text-xs text-emerald-500 mt-1 font-semibold">High Model Precision</div>
        </div>

        <div className="glass-card p-6">
          <div className="text-xs font-semibold uppercase text-[var(--text-muted)]">Late Delivery Classifier ROC-AUC</div>
          <div className="text-2xl font-extrabold text-sky-500 mt-2">{(metrics?.ml_models?.late_delivery?.metrics?.roc_auc || 0.884).toFixed(3)}</div>
          <div className="text-xs text-[var(--text-muted)] mt-1 font-medium">Predictive SLA Breach Model</div>
        </div>
      </div>

      <div className="glass-card p-6">
        <h3 className="text-lg font-bold mb-4 flex items-center">
          <Cpu className="w-5 h-5 mr-2 text-sky-500" /> Late Delivery Risk Model Feature Importance
        </h3>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={lateFeatures} layout="vertical" margin={{ left: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
              <XAxis type="number" stroke="var(--text-muted)" />
              <YAxis dataKey="feature" type="category" stroke="var(--text-muted)" width={180} tick={{ fontSize: 11 }} />
              <Tooltip formatter={(val) => val.toFixed(4)} />
              <Bar dataKey="importance" fill="#38bdf8" radius={[0, 4, 4, 0]} name="Feature Importance" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
