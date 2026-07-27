"""
Fraud Detection Model Module for DataCo Global Supply Chain Analytics.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from src.utils.logger import get_logger

logger = get_logger("FraudModel")

def train_fraud_model(df: pd.DataFrame) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Trains a Fraud Detection model to predict SUSPECTED_FRAUD orders."""
    logger.info("Training Fraud Detection Model...")
    
    # Target: 1 if Order Status == 'SUSPECTED_FRAUD', else 0
    df_fraud = df.copy()
    df_fraud['is_fraud'] = (df_fraud['Order Status'] == 'SUSPECTED_FRAUD').astype(int)
    
    feature_cols = [
        'Sales', 'Order Item Quantity', 'Order Item Product Price',
        'Order Item Discount', 'Latitude', 'Longitude'
    ]
    categorical_cols = ['Type', 'Customer Segment', 'Market', 'Order Region', 'Shipping Mode']
    
    avail_num = [c for c in feature_cols if c in df_fraud.columns]
    avail_cat = [c for c in categorical_cols if c in df_fraud.columns]
    
    X = pd.get_dummies(df_fraud[avail_num + avail_cat], columns=avail_cat, drop_first=True)
    y = df_fraud['is_fraud']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    rf_fraud = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, class_weight='balanced', n_jobs=-1)
    rf_fraud.fit(X_train, y_train)
    
    y_pred = rf_fraud.predict(X_test)
    y_proba = rf_fraud.predict_proba(X_test)[:, 1]
    
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }
    
    importances = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_fraud.feature_importances_
    }).sort_values('importance', ascending=False)
    
    logger.info(f"Fraud Model Evaluation -> ROC-AUC: {metrics['roc_auc']:.4f}, Recall: {metrics['recall']:.4f}")
    return metrics, importances.head(15)
