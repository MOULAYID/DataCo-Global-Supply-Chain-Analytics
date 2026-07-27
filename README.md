# DataCo Global Supply Chain Analytics & Executive Decision Support System

[![Spec-Driven Development](https://img.shields.io/badge/Methodology-Spec--Driven%20Development-blue.svg)](https://github.com/zekiriabd/SDD-Pro)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Vite React](https://img.shields.io/badge/Frontend-Vite%20%2B%20React-61DAFB.svg)](https://vitejs.dev/)
[![Live Dashboard](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-emerald.svg)](https://MOULAYID.github.io/DataCo-Global-Supply-Chain-Analytics/)
[![Tests Passed](https://img.shields.io/badge/Tests-Passed%20(3/3)-emerald.svg)](#)

A McKinsey/Deloitte/Amazon-grade senior analytics consulting engagement for DataCo Global. This project delivers an end-to-end data engineering pipeline, statistical testing engine, machine learning suite, publication-grade Jupyter notebook, and an interactive 11-page modern SaaS executive web dashboard.

🌐 **Live Interactive SaaS Dashboard**: [https://MOULAYID.github.io/DataCo-Global-Supply-Chain-Analytics/](https://MOULAYID.github.io/DataCo-Global-Supply-Chain-Analytics/)

---

## 🌟 Executive Key Performance Indicators (KPIs)

| Metric | Empirical Value | Target SLA | Business Impact |
|---|---|---|---|
| **Gross Revenue** | **$36,792,671.93** | — | 180,519 order line items analyzed (2015–2018) |
| **Net Order Profit** | **$3,969,176.42** | — | Overall net profit margin: **10.78%** |
| **Late Delivery Rate** | **54.83%** | ≤ 15.0% | **98,977 delayed shipments** (Critical operational bottleneck) |
| **Suspected Fraud Rate**| **2.25%** | ≤ 2.00% | **4,062 flagged transactions** ($800k+ volume exposure) |
| **Active Customer Base**| **20,652 Users** | — | Top VIP segment accounts for 45% of total company profit |

---

## 🛠️ System Architecture & Spec-Driven Development (SDD)

Built following the **Spec-Driven Development (SDD)** methodology (inspired by SDD-Pro), every implementation step traces back to documented specs:

```
DataCo Global Supply Chain analysis/
├── .github/workflows/deploy-dashboard.yml # Auto GitHub Pages CI/CD Deployment
├── specs/                                # SDD Documentation Suite
│   ├── project_specification.md         # Architecture & Tech Stack Scope
│   ├── business_requirements.md          # Business Question Matrix & SLAs
│   ├── data_analysis_plan.md             # Feature Engineering & Statistical Methods
│   ├── technical_architecture.md         # Package Layout & Data Flow
│   ├── dashboard_design.md               # UX & 11 Page Layout Specifications
│   ├── tasks.md                          # 16-Step Task Execution Matrix
│   └── validation_checklist.md           # Empirical Quality Checklist
├── src/                                  # Modular Python Analytics & ML Package
│   ├── data/                             # Loader, Cleaner, Validator
│   ├── features/                         # 25+ Feature Engineering Pipeline
│   ├── stats/                            # Normality, ANOVA, Chi2, T-Tests, OLS Regression
│   └── ml/                               # 5 ML Models (Late Delivery, Profit, Fraud, RFM, Forecast)
├── dashboard/                            # 11-Page Vite + React Modern SaaS Dashboard
├── notebooks/                            # Publication-Quality Jupyter Notebook
├── reports/                              # McKinsey/Deloitte Executive Presentations & RCA
└── tests/                                # Automated Pipeline Integration Test Suite
```

---

## 🚀 Quickstart Guide

### 1. View Live Online Dashboard
Open the deployed dashboard: [https://MOULAYID.github.io/DataCo-Global-Supply-Chain-Analytics/](https://MOULAYID.github.io/DataCo-Global-Supply-Chain-Analytics/)

### 2. Run Pipeline Locally
```bash
# Run master orchestration pipeline (cleaning, feature engineering, stats, ML, JSON export)
python run_pipeline.py
```

### 3. Launch Local Dashboard
```bash
cd dashboard
npm install
npm run dev
```

---

## 🤖 Machine Learning Predictive Suite

1. **Late Delivery Risk Classifier**: Predicts shipment delay risk at order placement ($ROC-AUC = 0.761$).
2. **Fraud Detection Engine**: Identifies high-risk payment transactions before dispatch ($ROC-AUC = 0.916$, $Recall = 99.75\%$).
3. **Order Profitability Model**: Regression diagnostics isolating margin-eroding discount thresholds.
4. **RFM Customer Segmentation**: K-Means clustering categorizing 20,652 customers into 4 behavioral segments with CLV estimates.
5. **30-Day Demand Forecasting**: Time-series Holt-Winters Exponential Smoothing model forecasting daily sales volume.

---

## 📊 11-Page Interactive SaaS Dashboard

The interactive dashboard (built with Vite + React + Tailwind CSS + Lucide Icons + Recharts) includes dark/light theme switching and 11 dedicated pages:
1. **Executive Summary**: Core KPI scorecard, revenue/profit timeline, McKinsey takeaway banner.
2. **Sales Analytics**: Category revenue breakdown & sales velocity.
3. **Profitability Deep Dive**: Loss-making product detector & margin waterfall.
4. **Customer Intelligence**: RFM cluster matrix & CLV leaderboards.
5. **Product Analysis**: Pareto ABC classification curves.
6. **Shipping & Logistics**: Carrier SLA breach ranking & days delay distributions.
7. **Geospatial Intelligence**: Global profit & order density maps.
8. **Inventory & Demand**: Backorder risk indicators & velocity.
9. **Fraud & Risk Management**: Suspected fraud breakdown & risk vector scoring.
10. **Forecasting & ML Suite**: 30-day forecast curves & feature importance charts.
11. **KPI SLA Scorecard**: Benchmark target vs actual compliance indicators.
