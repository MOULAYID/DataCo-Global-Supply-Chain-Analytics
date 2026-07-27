# Spec-Driven Development (SDD): Project Specification

## 1. Project Overview
- **Project Title**: DataCo Global Supply Chain Analytics & Executive Decision Support System
- **Organization**: DataCo Global Logistics & Retail
- **Dataset Scope**: 180,519 line items (Jan 1, 2015 – Jan 31, 2018), 53 features per record, plus tokenized web access logs (`tokenized_access_logs.csv`).
- **Primary Objective**: Perform a complete senior-level consulting analytics engagement to identify financial leakage, operational bottlenecks, late delivery risk factors, fraud vectors, product profitability drivers, customer lifetime value, and demand forecasting.

## 2. System Architecture & Components
- **Data Layer**: Standardized Parquet files (`data/processed/clean_dataco_dataset.parquet`, `data/processed/access_logs_summary.parquet`).
- **Processing Layer**: Modular Python package (`src/`) with type-hinted, tested, and logged modules for cleaning, feature engineering, statistical modeling, and ML.
- **Machine Learning Suite**: 5 specialized models (Late Delivery Risk, Profitability Prediction, Fraud Classifier, RFM Customer Clustering, Demand Forecasting).
- **Executive Notebook**: Comprehensive Jupyter notebook (`notebooks/01_DataCo_Executive_Supply_Chain_Analytics.ipynb`) with full narrative, Plotly visuals, and statistical rigor.
- **Modern SaaS Dashboard**: 11-page responsive Vite+React web application with dark/light mode, custom CSS, Lucide icons, and interactive chart visualizations.
- **Executive Deliverables**: Slide-deck style markdown report (`reports/executive_report.md`) and operational root cause analysis (`reports/root_cause_analysis.md`).

## 3. Technology Stack Requirements
- **Language**: Python 3.10+
- **Data Engineering & Analytics**: Pandas, NumPy, SciPy, Statsmodels, Scikit-Learn, LightGBM
- **Visualizations**: Plotly, Matplotlib, Seaborn
- **Dashboard**: Vite, React 18, Tailwind CSS, Recharts / Chart.js, Lucide Icons
- **Documentation & Testing**: Pytest, Markdown, Jupyter
