"""
Data Validation Module for DataCo Global Supply Chain Analytics.
"""
import pandas as pd
from typing import Dict, Any
from src.utils.logger import get_logger

logger = get_logger("DataValidator")

def validate_supply_chain_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Validates cleaned dataset against quality criteria."""
    logger.info("Executing data validation suite...")
    results = {"valid": True, "errors": [], "metrics": {}}
    
    # 1. Row count check
    if len(df) == 0:
        results["valid"] = False
        results["errors"].append("Dataset is empty.")
        return results
        
    results["metrics"]["row_count"] = len(df)
    results["metrics"]["column_count"] = len(df.columns)
    
    # 2. Key column presence check
    required_cols = [
        'Type', 'Days for shipping (real)', 'Days for shipment (scheduled)',
        'Benefit per order', 'Delivery Status', 'Late_delivery_risk',
        'Customer Id', 'Customer Segment', 'Market', 'Order Country',
        'order date (DateOrders)', 'Order Id', 'Sales', 'Order Profit Per Order',
        'Shipping Mode', 'Product Name', 'Product Price'
    ]
    missing_req = [col for col in required_cols if col not in df.columns]
    if missing_req:
        results["valid"] = False
        results["errors"].append(f"Missing required columns: {missing_req}")
        
    # 3. Target null check
    critical_cols = ['Sales', 'Order Profit Per Order', 'Late_delivery_risk', 'order date (DateOrders)']
    for col in critical_cols:
        if col in df.columns:
            null_cnt = df[col].isnull().sum()
            if null_cnt > 0:
                results["valid"] = False
                results["errors"].append(f"Column '{col}' has {null_cnt} unexpected null values.")
                
    # 4. Numeric Range Sanity
    if 'Days for shipping (real)' in df.columns:
        invalid_shipping = (df['Days for shipping (real)'] < 0).sum()
        if invalid_shipping > 0:
            results["errors"].append(f"Found {invalid_shipping} negative shipping days.")
            
    if results["valid"]:
        logger.info("Validation passed successfully with zero critical errors.")
    else:
        logger.warning(f"Validation completed with errors: {results['errors']}")
        
    return results
