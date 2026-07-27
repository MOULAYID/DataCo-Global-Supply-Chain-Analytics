"""
Master Orchestration Pipeline for DataCo Global Supply Chain Analytics.
Executes cleaning, validation, feature engineering, statistical testing, ML models, and JSON metric export.
"""
import os
import json
import pandas as pd
import numpy as np

from src.utils.logger import get_logger
from src.data.loader import load_raw_dataset
from src.data.clean_data import clean_supply_chain_data, save_clean_data
from src.data.validate import validate_supply_chain_data
from src.features.build_features import engineer_features, save_engineered_features
from src.stats.statistical_analysis import run_statistical_suite
from src.ml.late_delivery_model import train_late_delivery_model
from src.ml.profit_model import train_profit_model
from src.ml.fraud_model import train_fraud_model
from src.ml.customer_segmentation import run_customer_rfm_segmentation
from src.ml.demand_forecasting import train_demand_forecasting

logger = get_logger("MasterPipeline")

def convert_to_json_serializable(obj):
    """Recursively converts NumPy and Pandas data types to native Python types."""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, (np.ndarray, list)):
        return [convert_to_json_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {str(k): convert_to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (pd.Timestamp, pd.DatetimeIndex)):
        return str(obj)
    elif pd.isna(obj):
        return None
    return obj

def run_full_pipeline():
    logger.info("==================================================================")
    logger.info("STARTING DATACO GLOBAL SUPPLY CHAIN EXECUTIVE ANALYTICS PIPELINE")
    logger.info("==================================================================")
    
    # 1. Load Data
    raw_df = load_raw_dataset("DataCoSupplyChainDataset.csv")
    
    # 2. Clean Data
    clean_df = clean_supply_chain_data(raw_df)
    save_clean_data(clean_df)
    
    # 3. Validate Data
    val_results = validate_supply_chain_data(clean_df)
    if not val_results["valid"]:
        logger.error(f"Data validation failed: {val_results['errors']}")
        raise ValueError("Pipeline aborted due to data validation errors.")
        
    # 4. Feature Engineering
    feat_df = engineer_features(clean_df)
    save_engineered_features(feat_df)
    
    # 5. Statistical Testing
    stats_results = run_statistical_suite(feat_df)
    
    # 6. Machine Learning Models
    late_metrics, late_imp = train_late_delivery_model(feat_df)
    profit_metrics, profit_imp = train_profit_model(feat_df)
    fraud_metrics, fraud_imp = train_fraud_model(feat_df)
    rfm_metrics, rfm_df = run_customer_rfm_segmentation(feat_df)
    forecast_metrics, forecast_df = train_demand_forecasting(feat_df)
    
    # 7. Executive Summary & Dashboard Metrics Aggregation
    total_sales = float(feat_df['Sales'].sum())
    total_profit = float(feat_df['Order Profit Per Order'].sum())
    overall_profit_margin = float(total_profit / total_sales) if total_sales > 0 else 0.0
    total_orders = int(feat_df['Order Id'].nunique())
    late_delivery_count = int((feat_df['Late_delivery_risk'] == 1).sum())
    late_delivery_rate = float(late_delivery_count / len(feat_df))
    fraud_orders_count = int((feat_df['Order Status'] == 'SUSPECTED_FRAUD').sum())
    fraud_rate = float(fraud_orders_count / len(feat_df))
    
    # Monthly Trends
    monthly_sales = feat_df.groupby('order_month_name', observed=False)['Sales'].sum().to_dict()
    category_sales = feat_df.groupby('Category Name')['Sales'].sum().sort_values(ascending=False).head(10).to_dict()
    category_profit = feat_df.groupby('Category Name')['Order Profit Per Order'].sum().sort_values(ascending=False).head(10).to_dict()
    loss_categories = feat_df.groupby('Category Name')['Order Profit Per Order'].sum().sort_values(ascending=True).head(5).to_dict()
    
    country_profit = feat_df.groupby('Order Country')['Order Profit Per Order'].sum().sort_values(ascending=False).head(10).to_dict()
    loss_countries = feat_df.groupby('Order Country')['Order Profit Per Order'].sum().sort_values(ascending=True).head(10).to_dict()
    
    shipping_mode_perf = feat_df.groupby('Shipping Mode').agg(
        total_orders=('Order Id', 'nunique'),
        late_rate=('Late_delivery_risk', 'mean'),
        avg_delay=('shipping_delay', 'mean'),
        total_profit=('Order Profit Per Order', 'sum')
    ).reset_index().to_dict(orient='records')
    
    abc_breakdown = feat_df.groupby('abc_class')['Sales'].agg(['count', 'sum']).reset_index().to_dict(orient='records')
    
    dashboard_payload = {
        "kpis": {
            "total_revenue": total_sales,
            "total_profit": total_profit,
            "net_margin_pct": overall_profit_margin,
            "total_orders": total_orders,
            "late_delivery_rate": late_delivery_rate,
            "late_delivery_count": late_delivery_count,
            "fraud_orders_count": fraud_orders_count,
            "fraud_rate": fraud_rate,
            "total_customers": int(feat_df['Customer Id'].nunique())
        },
        "monthly_sales": monthly_sales,
        "top_categories_sales": category_sales,
        "top_categories_profit": category_profit,
        "loss_making_categories": loss_categories,
        "top_countries_profit": country_profit,
        "loss_making_countries": loss_countries,
        "shipping_performance": shipping_mode_perf,
        "abc_breakdown": abc_breakdown,
        "statistical_tests": stats_results,
        "ml_models": {
            "late_delivery": {
                "metrics": late_metrics,
                "feature_importances": late_imp.to_dict(orient='records')
            },
            "profitability": {
                "metrics": profit_metrics,
                "feature_importances": profit_imp.to_dict(orient='records')
            },
            "fraud_detection": {
                "metrics": fraud_metrics,
                "feature_importances": fraud_imp.to_dict(orient='records')
            },
            "customer_rfm": rfm_metrics,
            "demand_forecast": forecast_metrics
        }
    }
    
    output_json_path = os.path.join("data", "processed", "dashboard_metrics.json")
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    with open(output_json_path, "w") as f:
        json.dump(convert_to_json_serializable(dashboard_payload), f, indent=2)
        
    logger.info(f"Dashboard metrics successfully exported to {output_json_path}")
    logger.info("==================================================================")
    logger.info("DATACO GLOBAL PIPELINE EXECUTED SUCCESSFULLY!")
    logger.info("==================================================================")

if __name__ == "__main__":
    run_full_pipeline()
