"""
Data Loader Module for DataCo Global Supply Chain Analytics.
"""
import os
import pandas as pd
from typing import Tuple, Optional
from src.utils.logger import get_logger

logger = get_logger("DataLoader")

def load_raw_dataset(file_path: str = "DataCoSupplyChainDataset.csv") -> pd.DataFrame:
    """Loads the main DataCo Supply Chain CSV dataset."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        raise FileNotFoundError(f"Dataset path {file_path} does not exist.")
        
    logger.info(f"Loading raw dataset from {file_path}...")
    df = pd.read_csv(file_path, encoding="ISO-8859-1")
    logger.info(f"Successfully loaded dataset with shape: {df.shape}")
    return df

def load_access_logs(file_path: str = "tokenized_access_logs.csv") -> pd.DataFrame:
    """Loads the web access logs CSV dataset."""
    if not os.path.exists(file_path):
        logger.warning(f"Access log file not found: {file_path}")
        return pd.DataFrame()
        
    logger.info(f"Loading web access logs from {file_path}...")
    df = pd.read_csv(file_path)
    logger.info(f"Successfully loaded access logs with shape: {df.shape}")
    return df
