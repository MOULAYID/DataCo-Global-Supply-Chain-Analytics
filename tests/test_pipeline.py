"""
Automated Pipeline Validation Test Suite for DataCo Global Supply Chain Analytics.
"""
import os
import unittest
import pandas as pd
import json

class TestDataCoPipeline(unittest.TestCase):
    
    def test_01_processed_data_exists(self):
        parquet_path = os.path.join("data", "processed", "clean_dataco_dataset.parquet")
        self.assertTrue(os.path.exists(parquet_path), "Clean dataset parquet file missing.")
        
    def test_02_feature_dataset_schema(self):
        feat_path = os.path.join("data", "processed", "feature_engineered_dataset.parquet")
        self.assertTrue(os.path.exists(feat_path), "Engineered feature parquet file missing.")
        df = pd.read_parquet(feat_path)
        self.assertGreater(len(df), 100000, "Row count less than expected 100k.")
        self.assertIn("shipping_delay", df.columns)
        self.assertIn("profit_margin", df.columns)
        self.assertIn("abc_class", df.columns)
        self.assertIn("is_late", df.columns)
        
    def test_03_dashboard_metrics_json(self):
        json_path = os.path.join("data", "processed", "dashboard_metrics.json")
        self.assertTrue(os.path.exists(json_path), "Dashboard metrics JSON missing.")
        with open(json_path, "r") as f:
            data = json.load(f)
        self.assertIn("kpis", data)
        self.assertIn("ml_models", data)
        self.assertIn("statistical_tests", data)

if __name__ == "__main__":
    unittest.main()
