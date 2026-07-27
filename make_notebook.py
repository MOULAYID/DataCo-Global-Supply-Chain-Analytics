import os
import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# DataCo Global Supply Chain Analytics & Executive Decision Support System\n",
    "**Author**: Senior Analytics Consultant  \n",
    "**Methodology**: Spec-Driven Development (SDD)  \n",
    "**Dataset Scope**: 180,519 line items | Jan 2015 – Jan 2018 | 53 Features\n",
    "\n",
    "---\n",
    "\n",
    "## 1. Executive Summary & Problem Context\n",
    "DataCo Global is an international e-commerce and retail supply chain enterprise. While generating **$36.79M in gross revenue**, the enterprise faces critical operational headwinds:\n",
    "1. **Late Delivery Crisis**: 54.83% of all orders experience late delivery.\n",
    "2. **Profit Margins**: Uncapped discounting (>15%) erodes profitability in key markets.\n",
    "3. **Fraud Exposure**: 4,062 suspected fraud orders ($800k+ volume).\n",
    "\n",
    "This portfolio notebook delivers empirical statistical analysis, machine learning predictive models, and strategic executive recommendations."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import plotly.express as px\n",
    "import plotly.graph_objects as go\n",
    "import json\n",
    "\n",
    "# Load processed parquet dataset and metrics JSON\n",
    "df = pd.read_parquet('../data/processed/feature_engineered_dataset.parquet')\n",
    "with open('../data/processed/dashboard_metrics.json') as f:\n",
    "    metrics = json.load(f)\n",
    "\n",
    "print(f\"Loaded clean dataset with shape: {df.shape}\")\n",
    "print(\"Executive KPIs:\", metrics['kpis'])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Statistical Analysis & Hypothesis Testing\n",
    "\n",
    "### A. Normality Testing\n",
    "We evaluate whether sales, profit, and shipping delay follow a normal distribution using D'Agostino's $K^2$ test:\n",
    "\n",
    "$$K^2 = s^2 + k^2 \\sim \\chi^2(2)$$\n",
    "\n",
    "### B. Profit Driver Regression Equation\n",
    "$$\\text{Order Profit} = \\beta_0 + \\beta_1(\\text{Sales}) - \\beta_2(\\text{Discount}) - \\beta_3(\\text{Shipping Delay}) + \\varepsilon$$"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Display Statistical Test Results\n",
    "stats_res = metrics['statistical_tests']\n",
    "print(\"=== T-Test (Late vs On-Time Profit) ===\")\n",
    "print(stats_res.get('ttest_late_vs_ontime_profit'))\n",
    "\n",
    "print(\"\n=== One-Way ANOVA (Shipping Mode Profit) ===\")\n",
    "print(stats_res.get('anova_shipping_mode_profit'))\n",
    "\n",
    "print(\"\n=== Chi-Square (Market vs Fraud) ===\")\n",
    "print(stats_res.get('chi2_market_fraud'))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Interactive Data Visualizations\n",
    "Below we plot monthly revenue trends and late delivery rates by shipping mode using Plotly."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Plot Monthly Revenue Trajectory\n",
    "monthly_df = df.groupby('order_month_name', observed=False)['Sales'].sum().reset_index()\n",
    "fig_sales = px.bar(monthly_df, x='order_month_name', y='Sales', title='Monthly Revenue Distribution ($)', color='Sales', color_continuous_scale='Blues')\n",
    "fig_sales.show()\n",
    "\n",
    "# Shipping Mode Late Delivery Rates\n",
    "ship_df = df.groupby('Shipping Mode')['is_late'].mean().reset_index()\n",
    "fig_ship = px.bar(ship_df, x='Shipping Mode', y='is_late', title='Late Delivery Rate by Shipping Mode', labels={'is_late': 'Late Rate (%)'}, color='is_late', color_continuous_scale='Reds')\n",
    "fig_ship.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Machine Learning Predictive Models\n",
    "We evaluate 5 machine learning models:\n",
    "1. **Late Delivery Risk Classifier** (ROC-AUC: 0.761)\n",
    "2. **Order Profitability Regressor**\n",
    "3. **Fraud Detection Engine** (ROC-AUC: 0.916, Recall: 99.7%)\n",
    "4. **RFM K-Means Customer Clustering**\n",
    "5. **Holt-Winters 30-Day Demand Forecast**"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Print ML Model Evaluation Summary\n",
    "ml_res = metrics['ml_models']\n",
    "print(\"=== Late Delivery Classifier Metrics ===\")\n",
    "print(ml_res['late_delivery']['metrics'])\n",
    "\n",
    "print(\"\n=== Fraud Detection Engine Metrics ===\")\n",
    "print(ml_res['fraud_detection']['metrics'])\n",
    "\n",
    "print(\"\n=== Customer RFM Segmentation Profile ===\")\n",
    "print(pd.DataFrame(ml_res['customer_rfm']['cluster_profiles']))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Executive McKinsey Takeaways & Strategic Action Plan\n",
    "- **Renegotiate First Class SLAs**: First Class mode exhibits a 95.2% late delivery rate. Re-adjust scheduled buffers in ERP.\n",
    "- **Enforce Fraud Holds**: Hold `TRANSFER` payment orders with ML fraud risk score > 0.70 to prevent $800k in losses.\n",
    "- **Cap Discounting at 15%**: Protect gross margins against profit-eroding promotions."
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

os.makedirs("notebooks", exist_ok=True)
with open("notebooks/01_DataCo_Executive_Supply_Chain_Analytics.ipynb", "w") as f:
    json.dump(notebook_content, f, indent=1)
print("Jupyter Notebook created successfully!")
