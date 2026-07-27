"""
Late Delivery Prediction Model Module for DataCo Global Supply Chain Analytics.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from src.utils.logger import get_logger

logger = get_logger("LateDeliveryModel")

def train_late_delivery_model(df: pd.DataFrame) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Trains machine learning models to predict Late Delivery Risk."""
    logger.info("Training Late Delivery Risk Classification Models...")
    
    # Feature Selection
    feature_cols = [
        'Days for shipment (scheduled)', 'Order Item Quantity', 'Sales',
        'Order Item Product Price', 'Order Item Discount Rate', 'Latitude', 'Longitude'
    ]
    categorical_cols = ['Shipping Mode', 'Customer Segment', 'Market', 'Order Region']
    
    # Check column availability
    avail_num = [c for c in feature_cols if c in df.columns]
    avail_cat = [c for c in categorical_cols if c in df.columns]
    
    X = pd.get_dummies(df[avail_num + avail_cat], columns=avail_cat, drop_first=True)
    y = df['Late_delivery_risk'].astype(int)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Random Forest Model
    logger.info("Fitting Random Forest Classifier...")
    rf_model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    
    y_pred = rf_model.predict(X_test)
    y_proba = rf_model.predict_proba(X_test)[:, 1]
    
    # Metrics
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "f1_score": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
    }
    
    # Feature Importance
    importances = pd.DataFrame({
        'feature': X.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    logger.info(f"Late Delivery Model Evaluation -> ROC-AUC: {metrics['roc_auc']:.4f}, Accuracy: {metrics['accuracy']:.4f}")
    return metrics, importances.head(15)
