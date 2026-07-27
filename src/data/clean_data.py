"""
Data Cleaning Module for DataCo Global Supply Chain Analytics.
"""
import os
import pandas as pd
import numpy as np
from typing import Tuple
from src.utils.logger import get_logger

logger = get_logger("DataCleaner")

def clean_supply_chain_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans and standardizes raw DataCo supply chain dataframe."""
    logger.info("Starting data cleaning pipeline...")
    df_clean = df.copy()
    
    # 1. Clean column names (strip whitespace)
    df_clean.columns = [col.strip() for col in df_clean.columns]
    
    # 2. Parse Datetime fields
    datetime_cols = ['order date (DateOrders)', 'shipping date (DateOrders)']
    for col in datetime_cols:
        if col in df_clean.columns:
            logger.info(f"Parsing datetime column: {col}")
            df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
            
    # 3. Handle Missing Values
    # Product Description is 100% missing -> drop column
    if 'Product Description' in df_clean.columns:
        logger.info("Dropping 100% null column: Product Description")
        df_clean.drop(columns=['Product Description'], inplace=True)
        
    # Customer Lname -> fill missing with empty string or Unknown
    if 'Customer Lname' in df_clean.columns:
        df_clean['Customer Lname'] = df_clean['Customer Lname'].fillna('')
        
    # Customer Zipcode
    if 'Customer Zipcode' in df_clean.columns:
        df_clean['Customer Zipcode'] = df_clean['Customer Zipcode'].fillna(0).astype(int).astype(str)
        
    # Order Zipcode
    if 'Order Zipcode' in df_clean.columns:
        df_clean['Order Zipcode'] = df_clean['Order Zipcode'].fillna(0).astype(str)

        
    # 4. Standardize text fields
    text_cols = ['Customer City', 'Customer Country', 'Customer Segment', 'Customer State',
                 'Market', 'Order City', 'Order Country', 'Order Region', 'Order State',
                 'Order Status', 'Delivery Status', 'Shipping Mode', 'Category Name', 'Department Name', 'Product Name']
    for col in text_cols:
        if col in df_clean.columns and df_clean[col].dtype == 'object':
            df_clean[col] = df_clean[col].astype(str).str.strip()
            
    # 5. Ensure non-negative quantity & price sanity
    if 'Order Item Quantity' in df_clean.columns:
        df_clean = df_clean[df_clean['Order Item Quantity'] > 0]
        
    logger.info(f"Data cleaning completed. Final shape: {df_clean.shape}")
    return df_clean

def save_clean_data(df: pd.DataFrame, output_dir: str = "data/processed") -> str:
    """Saves cleaned dataframe to parquet format."""
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, "clean_dataco_dataset.parquet")
    logger.info(f"Saving clean data to {file_path}...")
    df.to_parquet(file_path, index=False)
    logger.info("Clean dataset saved successfully.")
    return file_path
