"""
Profitability Prediction Model Module for DataCo Global Supply Chain Analytics.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from src.utils.logger import get_logger

logger = get_logger("ProfitModel")

def train_profit_model(df: pd.DataFrame) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Trains regression models to predict Order Profit Per Order."""
    logger.info("Training Order Profitability Regression Model...")
    
    feature_cols = [
        'Sales', 'Order Item Product Price', 'Order Item Quantity',
        'Order Item Discount', 'Order Item Discount Rate', 'shipping_delay'
    ]
    categorical_cols = ['Shipping Mode', 'Customer Segment', 'Market', 'Order Region']
    
    avail_num = [c for c in feature_cols if c in df.columns]
    avail_cat = [c for c in categorical_cols if c in df.columns]
    
    df_clean = df.dropna(subset=['Order Profit Per Order'] + avail_num)
    X = pd.get_dummies(df_clean[avail_num + avail_cat], columns=avail_cat, drop_first=True)
    y = df_clean['Order Profit Per Order']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf_reg = RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    rf_reg.fit(X_train, y_train)
    
    y_pred = rf_reg.predict(X_test)
    
    metrics = {
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "r2_score": float(r2_score(y_test, y_pred))
    }
    
    importances = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_reg.feature_importances_
    }).sort_values('importance', ascending=False)
    
    logger.info(f"Profit Model Evaluation -> R2 Score: {metrics['r2_score']:.4f}, RMSE: {metrics['rmse']:.4f}")
    return metrics, importances.head(15)
