# Spec-Driven Development (SDD): Dashboard Design Specification

## 1. UX & Visual Design System
- **Theme Concept**: Modern Premium SaaS (Inspired by Stripe, Vercel, Linear, Notion).
- **Color Palette**:
  - Dark Mode: `#0B0F17` background, `#161C28` card background, `#1E2638` border, `#38BDF8` primary accent (sky blue), `#10B981` success (emerald green), `#EF4444` danger (red), `#F59E0B` warning (amber).
  - Light Mode: `#F8FAFC` background, `#FFFFFF` card background, `#E2E8F0` border, `#0284C7` primary accent.
- **Typography**: Inter / system sans-serif with clear hierarchical weights (bold stat numbers, muted uppercase micro-labels).
- **Layout Structure**: Top executive nav bar + left sidebar navigation with 11 dynamic page views + top KPI summary toolbar + live theme switcher (Dark/Light).

## 2. Interactive Dashboard Pages (11 Pages)
1. **Executive Summary**: Core KPI Scorecard (Revenue, Net Profit, Profit Margin %, Late Delivery %, Fraud Rate, Active Orders), Revenue vs Profit multi-axis timeline, Top Risk Alert Banner, Quick Bottleneck Breakdown.
2. **Sales Analytics**: Revenue by Product Category, Top 10 Best Sellers by Revenue, Discount impact on sales volume, Monthly sales growth trajectory.
3. **Profitability Deep Dive**: Net Margin % breakdown by region, Loss-making product detector table, Discount vs Profit Margin scatter, Gross Profit waterfall analysis.
4. **Customer Intelligence**: RFM Segment distribution matrix, High-Value Customer leaderboard, CLV estimation by segment, Regional customer value heatmap.
5. **Product & Inventory Analysis**: ABC Inventory Pareto Curve, Top/Bottom Margin products, Product cancellation & return rates, Category pricing distribution.
6. **Shipping & Logistics**: Late Delivery Rate by Shipping Mode, Actual vs Scheduled shipping time distributions, Regional fulfillment delay ranking, Shipping cost ratio.
7. **Geospatial Intelligence**: Global Profit & Order density map/table, Market performance matrix (LATAM, Europe, USCA, Pacific Asia, Africa), High-loss country pinpointing.
8. **Inventory Utilization & Demand**: Backorder risk indicators, Category demand velocity, Seasonal order patterns.
9. **Fraud & Risk Management**: Suspected fraud breakdown by payment type & market, Fraud volume ($) by country, Risk scoring engine insights.
10. **Forecasting & ML Predictive Suite**: 30-Day Sales Demand Forecast with confidence bands, Late Delivery Risk Feature Importance chart, Fraud risk prediction controls.
11. **Executive KPI Benchmark Scorecard**: Target SLA vs Current performance metrics with status indicators (On Track / At Risk / Critical).
