"""
Customer RFM Segmentation & K-Means Clustering Module for DataCo Global Supply Chain Analytics.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from src.utils.logger import get_logger

logger = get_logger("CustomerSegmentation")

def run_customer_rfm_segmentation(df: pd.DataFrame, n_clusters: int = 4) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """Calculates RFM metrics, applies K-Means clustering, and estimates CLV."""
    logger.info("Executing Customer RFM & K-Means Segmentation...")
    
    ref_date = df['order date (DateOrders)'].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby('Customer Id').agg(
        recency=('order date (DateOrders)', lambda x: (ref_date - x.max()).days),
        frequency=('Order Id', 'nunique'),
        monetary=('Sales', 'sum'),
        profit=('Order Profit Per Order', 'sum'),
        avg_order_value=('Sales', 'mean')
    ).reset_index()
    
    # Estimate Customer Lifetime Value (CLV)
    # Simple CLV = Avg Order Value * Frequency * (1 / (Recency / 365 + 1))
    rfm['clv_estimate'] = rfm['avg_order_value'] * rfm['frequency'] * (365.0 / (rfm['recency'] + 30))
    
    # Scale Features for Clustering
    features = ['recency', 'frequency', 'monetary']
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(np.log1p(rfm[features]))
    
    # Fit K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    rfm['cluster'] = kmeans.fit_predict(rfm_scaled)
    
    # Calculate Silhouette Score (subsample if large)
    sample_scaled = rfm_scaled[np.random.choice(rfm_scaled.shape[0], min(5000, rfm_scaled.shape[0]), replace=False)]
    sample_labels = rfm['cluster'].iloc[:len(sample_scaled)]
    sil_score = float(silhouette_score(sample_scaled, sample_labels))
    
    # Cluster Profiling & Naming
    cluster_profiles = rfm.groupby('cluster').agg(
        customer_count=('Customer Id', 'count'),
        mean_recency=('recency', 'mean'),
        mean_frequency=('frequency', 'mean'),
        mean_monetary=('monetary', 'mean'),
        mean_clv=('clv_estimate', 'mean')
    ).reset_index()
    
    # Map friendly segment names based on monetary & frequency rank
    cluster_profiles = cluster_profiles.sort_values('mean_monetary', ascending=False)
    segment_names = ['Champions / VIPs', 'Loyal Customers', 'At-Risk Buyers', 'Low-Value / Lost']
    cluster_mapping = {row['cluster']: segment_names[i] for i, row in enumerate(cluster_profiles.to_dict('records'))}
    cluster_profiles['segment_name'] = cluster_profiles['cluster'].map(cluster_mapping)
    rfm['segment_name'] = rfm['cluster'].map(cluster_mapping)

    
    metrics = {
        "n_clusters": n_clusters,
        "silhouette_score": sil_score,
        "total_customers": len(rfm),
        "cluster_profiles": cluster_profiles.to_dict(orient='records')
    }
    
    logger.info(f"Customer Segmentation Completed -> Silhouette Score: {sil_score:.4f}")
    return metrics, rfm
