import React from 'react';
import {
  LayoutDashboard, TrendingUp, DollarSign, Users, Package,
  Truck, Globe, Boxes, ShieldAlert, Cpu, Target
} from 'lucide-react';

const navItems = [
  { id: 'executive', label: 'Executive Summary', icon: LayoutDashboard },
  { id: 'sales', label: 'Sales Analytics', icon: TrendingUp },
  { id: 'profitability', label: 'Profitability Deep Dive', icon: DollarSign },
  { id: 'customers', label: 'Customer Intelligence', icon: Users },
  { id: 'products', label: 'Product Analysis', icon: Package },
  { id: 'shipping', label: 'Shipping & Logistics', icon: Truck },
  { id: 'geography', label: 'Geospatial Intelligence', icon: Globe },
  { id: 'inventory', label: 'Inventory & Demand', icon: Boxes },
  { id: 'fraud', label: 'Fraud & Risk Management', icon: ShieldAlert },
  { id: 'forecasting', label: 'Forecasting & ML Suite', icon: Cpu },
  { id: 'kpi', label: 'KPI SLA Scorecard', icon: Target },
];

export default function Sidebar({ activePage, setActivePage }) {
  return (
    <aside className="w-64 border-r border-[var(--border-color)] bg-[var(--bg-card)] p-4 flex flex-col justify-between shrink-0">
      <div className="space-y-1">
        <div className="px-3 py-2 text-xs font-semibold text-[var(--text-muted)] uppercase tracking-wider">
          Analytics Navigation
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activePage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-sky-500 text-white shadow-sm font-semibold'
                  : 'text-[var(--text-muted)] hover:bg-[var(--border-color)] hover:text-[var(--text-main)]'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      <div className="pt-4 border-t border-[var(--border-color)] px-3 text-xs text-[var(--text-muted)]">
        <div>DataCo Global Analytics v1.0</div>
        <div className="mt-1 font-mono text-[10px]">SDD Spec-Driven Portfolio</div>
      </div>
    </aside>
  );
}
