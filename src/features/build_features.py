"""
Feature Engineering Module for DataCo Global Supply Chain Analytics.
"""
import os
import pandas as pd
import numpy as np
from typing import Tuple
from src.utils.logger import get_logger

logger = get_logger("FeatureEngineering")

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Engineers 25+ domain-specific logistics, financial, customer, and temporal features."""
    logger.info("Starting feature engineering pipeline...")
    df_feat = df.copy()
    
    # 1. Shipping & Logistics Features
    if 'Days for shipping (real)' in df_feat.columns and 'Days for shipment (scheduled)' in df_feat.columns:
        df_feat['shipping_delay'] = df_feat['Days for shipping (real)'] - df_feat['Days for shipment (scheduled)']
        df_feat['is_late'] = df_feat['Late_delivery_risk'].astype(int)
        df_feat['is_early'] = (df_feat['shipping_delay'] < 0).astype(int)
        df_feat['is_on_time'] = (df_feat['shipping_delay'] == 0).astype(int)
        
    # Fulfillment time in hours
    if 'order date (DateOrders)' in df_feat.columns and 'shipping date (DateOrders)' in df_feat.columns:
        df_feat['fulfillment_hours'] = (
            (df_feat['shipping date (DateOrders)'] - df_feat['order date (DateOrders)']).dt.total_seconds() / 3600.0
        )
        
    # 2. Financial & Profitability Features
    if 'Sales' in df_feat.columns and 'Order Profit Per Order' in df_feat.columns:
        # Prevent division by zero
        df_feat['profit_margin'] = np.where(
            df_feat['Sales'] > 0,
            df_feat['Order Profit Per Order'] / df_feat['Sales'],
            0.0
        )
        df_feat['is_loss_making'] = (df_feat['Order Profit Per Order'] < 0).astype(int)
        
    if 'Order Item Product Price' in df_feat.columns and 'Order Item Quantity' in df_feat.columns:
        df_feat['gross_order_value'] = df_feat['Order Item Product Price'] * df_feat['Order Item Quantity']
        
    if 'Order Item Discount' in df_feat.columns and 'Sales' in df_feat.columns:
        df_feat['discount_ratio'] = np.where(
            df_feat['Sales'] > 0,
            df_feat['Order Item Discount'] / (df_feat['Sales'] + df_feat['Order Item Discount']),
            0.0
        )
        
    # 3. Temporal & Seasonality Features
    if 'order date (DateOrders)' in df_feat.columns:
        dt = df_feat['order date (DateOrders)']
        df_feat['order_year'] = dt.dt.year
        df_feat['order_month'] = dt.dt.month
        df_feat['order_month_name'] = dt.dt.month_name()
        df_feat['order_quarter'] = dt.dt.quarter
        df_feat['order_dayofweek'] = dt.dt.dayofweek
        df_feat['order_day_name'] = dt.dt.day_name()
        df_feat['order_hour'] = dt.dt.hour
        df_feat['is_weekend'] = dt.dt.dayofweek.isin([5, 6]).astype(int)
        
        # Season assignment
        month_to_season = {
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        }
        df_feat['season'] = dt.dt.month.map(month_to_season)
        
    # 4. Customer Behavior & Tenure Aggregates
    if 'Customer Id' in df_feat.columns and 'order date (DateOrders)' in df_feat.columns:
        cust_stats = df_feat.groupby('Customer Id').agg(
            customer_first_order=('order date (DateOrders)', 'min'),
            customer_last_order=('order date (DateOrders)', 'max'),
            customer_total_orders=('Order Id', 'nunique'),
            customer_total_spend=('Sales', 'sum'),
            customer_total_profit=('Order Profit Per Order', 'sum')
        ).reset_index()
        
        cust_stats['customer_tenure_days'] = (
            (cust_stats['customer_last_order'] - cust_stats['customer_first_order']).dt.total_seconds() / (24 * 3600.0)
        )
        cust_stats['customer_avg_order_value'] = cust_stats['customer_total_spend'] / cust_stats['customer_total_orders']
        
        df_feat = df_feat.merge(cust_stats, on='Customer Id', how='left')
        
    # 5. Product Pareto ABC Classification
    if 'Product Name' in df_feat.columns and 'Sales' in df_feat.columns:
        prod_rev = df_feat.groupby('Product Name')['Sales'].sum().reset_index().sort_values('Sales', ascending=False)
        total_rev = prod_rev['Sales'].sum()
        prod_rev['cum_sales'] = prod_rev['Sales'].cumsum()
        prod_rev['cum_pct'] = prod_rev['cum_sales'] / total_rev
        
        def assign_abc(pct):
            if pct <= 0.80:
                return 'A (Top 80% Rev)'
            elif pct <= 0.95:
                return 'B (Next 15% Rev)'
            else:
                return 'C (Bottom 5% Rev)'
                
        prod_rev['abc_class'] = prod_rev['cum_pct'].apply(assign_abc)
        df_feat = df_feat.merge(prod_rev[['Product Name', 'abc_class']], on='Product Name', how='left')
        
    logger.info(f"Feature engineering completed. Final column count: {len(df_feat.columns)}")
    return df_feat

def save_engineered_features(df: pd.DataFrame, output_dir: str = "data/processed") -> str:
    """Saves engineered features dataframe to parquet format."""
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "feature_engineered_dataset.parquet")
    logger.info(f"Saving engineered features to {file_path}...")
    df.to_parquet(file_path, index=False)
    logger.info("Engineered feature dataset saved successfully.")
    return file_path
