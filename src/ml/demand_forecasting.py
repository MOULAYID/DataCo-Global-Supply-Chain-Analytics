"""
Time Series Demand Forecasting Module for DataCo Global Supply Chain Analytics.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from src.utils.logger import get_logger

logger = get_logger("DemandForecasting")

def train_demand_forecasting(df: pd.DataFrame, forecast_days: int = 30) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Generates daily time-series demand forecasts using Holt-Winters Exponential Smoothing."""
    logger.info("Executing Demand Forecasting Time Series Analysis...")
    
    # Resample daily sales
    daily_sales = df.set_index('order date (DateOrders)')['Sales'].resample('D').sum().reset_index()
    daily_sales.columns = ['ds', 'y']
    daily_sales['y'] = daily_sales['y'].fillna(0)
    
    # 7-day and 30-day moving averages
    daily_sales['ma_7'] = daily_sales['y'].rolling(window=7, min_periods=1).mean()
    daily_sales['ma_30'] = daily_sales['y'].rolling(window=30, min_periods=1).mean()
    
    # Train / Test split for validation (last 30 days)
    train = daily_sales.iloc[:-forecast_days]
    test = daily_sales.iloc[-forecast_days:]
    
    # Fit Holt-Winters Exponential Smoothing
    logger.info("Fitting Holt-Winters Exponential Smoothing Model...")
    hw_model = ExponentialSmoothing(
        train['y'],
        trend='add',
        seasonal='add',
        seasonal_periods=7,
        initialization_method='estimated'
    ).fit()
    
    val_preds = hw_model.forecast(forecast_days)
    
    rmse = float(np.sqrt(mean_squared_error(test['y'], val_preds)))
    mape = float(mean_absolute_percentage_error(test['y'], val_preds))
    
    # Fit full model & forecast future 30 days
    full_model = ExponentialSmoothing(
        daily_sales['y'],
        trend='add',
        seasonal='add',
        seasonal_periods=7,
        initialization_method='estimated'
    ).fit()
    
    future_forecast = full_model.forecast(forecast_days)
    
    # Create forecast dates dataframe
    last_date = daily_sales['ds'].max()
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_days, freq='D')
    
    forecast_df = pd.DataFrame({
        'ds': future_dates,
        'yhat': future_forecast.values,
        'yhat_lower': future_forecast.values * 0.85,
        'yhat_upper': future_forecast.values * 1.15
    })
    
    metrics = {
        "rmse": rmse,
        "mape": mape,
        "history_days": len(daily_sales),
        "forecast_days": forecast_days
    }
    
    logger.info(f"Demand Forecasting Completed -> RMSE: ${rmse:,.2f}, MAPE: {mape*100:.2f}%")
    return metrics, pd.concat([daily_sales, forecast_df], ignore_index=True)
