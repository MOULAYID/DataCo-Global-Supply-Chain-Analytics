"""
Statistical Testing Engine Module for DataCo Global Supply Chain Analytics.
"""
import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger("StatisticalAnalysis")

def run_statistical_suite(df: pd.DataFrame) -> Dict[str, Any]:
    """Runs a complete suite of statistical hypothesis tests, ANOVA, Chi-Square, and OLS regression."""
    logger.info("Executing comprehensive statistical testing suite...")
    results = {}
    
    # 1. Normality Tests (D'Agostino-Pearson & Shapiro-Wilk)
    logger.info("Running normality tests...")
    normality_results = {}
    target_vars = ['Sales', 'Order Profit Per Order', 'shipping_delay']
    for var in target_vars:
        if var in df.columns:
            clean_series = df[var].dropna()
            # Subsample for computational safety if size > 5000
            sample_sub = clean_series.sample(min(5000, len(clean_series)), random_state=42)
            
            # D'Agostino K2 test
            stat_k2, p_k2 = stats.normaltest(sample_sub)
            # Shapiro-Wilk
            stat_sw, p_sw = stats.shapiro(sample_sub)
            
            normality_results[var] = {
                "dagostino_stat": float(stat_k2),
                "dagostino_p": float(p_k2),
                "shapiro_stat": float(stat_sw),
                "shapiro_p": float(p_sw),
                "is_normal": bool(p_k2 > 0.05 and p_sw > 0.05)
            }
    results["normality_tests"] = normality_results
    
    # 2. T-Test: Profit comparison between Late Delivery vs On-Time/Early
    if 'is_late' in df.columns and 'Order Profit Per Order' in df.columns:
        logger.info("Running independent T-Test for Late Delivery vs On-Time Profit...")
        late_profit = df[df['is_late'] == 1]['Order Profit Per Order'].dropna()
        ontime_profit = df[df['is_late'] == 0]['Order Profit Per Order'].dropna()
        
        t_stat, p_val = stats.ttest_ind(late_profit, ontime_profit, equal_var=False)
        results["ttest_late_vs_ontime_profit"] = {
            "t_statistic": float(t_stat),
            "p_value": float(p_val),
            "late_mean_profit": float(late_profit.mean()),
            "ontime_mean_profit": float(ontime_profit.mean()),
            "significant_difference": bool(p_val < 0.05)
        }
        
    # 3. One-Way ANOVA: Profit variation across Shipping Modes
    if 'Shipping Mode' in df.columns and 'Order Profit Per Order' in df.columns:
        logger.info("Running One-Way ANOVA across Shipping Modes...")
        groups = [group['Order Profit Per Order'].dropna() for name, group in df.groupby('Shipping Mode')]
        f_stat, p_val = stats.f_oneway(*groups)
        results["anova_shipping_mode_profit"] = {
            "f_statistic": float(f_stat),
            "p_value": float(p_val),
            "significant_difference": bool(p_val < 0.05)
        }
        
    # 4. Chi-Square Test of Independence: Market vs Suspected Fraud
    if 'Market' in df.columns and 'Order Status' in df.columns:
        logger.info("Running Chi-Square Test for Market vs Order Status...")
        contingency_table = pd.crosstab(df['Market'], df['Order Status'] == 'SUSPECTED_FRAUD')
        chi2, p_val, dof, ex = stats.chi2_contingency(contingency_table)
        results["chi2_market_fraud"] = {
            "chi2_stat": float(chi2),
            "p_value": float(p_val),
            "degrees_of_freedom": int(dof),
            "significant_association": bool(p_val < 0.05)
        }
        
    # 5. Pearson & Spearman Correlation
    num_cols = ['Sales', 'Order Profit Per Order', 'Order Item Product Price', 'Order Item Quantity', 'Order Item Discount', 'shipping_delay']
    avail_num = [c for c in num_cols if c in df.columns]
    if len(avail_num) > 1:
        logger.info("Computing Pearson & Spearman correlations...")
        pearson_corr = df[avail_num].corr(method='pearson').to_dict()
        spearman_corr = df[avail_num].corr(method='spearman').to_dict()
        results["correlations"] = {
            "pearson": pearson_corr,
            "spearman": spearman_corr
        }
        
    # 6. OLS Regression Diagnostics
    reg_features = ['Sales', 'Order Item Product Price', 'Order Item Discount', 'shipping_delay', 'Order Item Quantity']
    avail_reg = [c for c in reg_features if c in df.columns]
    if 'Order Profit Per Order' in df.columns and len(avail_reg) > 0:
        logger.info("Fitting OLS Regression Model for Profit Drivers...")
        X = df[avail_reg].dropna()
        y = df.loc[X.index, 'Order Profit Per Order']
        X_const = sm.add_constant(X)
        
        ols_model = sm.OLS(y, X_const).fit()
        
        # Variance Inflation Factor (VIF)
        vif_data = pd.DataFrame()
        vif_data["feature"] = X_const.columns
        vif_data["VIF"] = [variance_inflation_factor(X_const.values, i) for i in range(X_const.shape[1])]
        
        results["ols_regression"] = {
            "r_squared": float(ols_model.rsquared),
            "adj_r_squared": float(ols_model.rsquared_adj),
            "f_statistic": float(ols_model.fvalue),
            "f_pvalue": float(ols_model.f_pvalue),
            "coefficients": ols_model.params.to_dict(),
            "p_values": ols_model.pvalues.to_dict(),
            "vif": vif_data.to_dict(orient='records')
        }
        
    logger.info("Statistical analysis suite completed successfully.")
    return results
