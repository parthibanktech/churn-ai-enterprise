import unittest
import pandas as pd
import os
from src.data_loader import load_data
from src.preprocess import prepare_data

class TestPipeline(unittest.TestCase):
    def setUp(self):
        self.raw_data_path = "data/raw/Telco-Customer-Churn.csv"

    def test_data_loading(self):
        if os.path.exists(self.raw_data_path):
            df = load_data(self.raw_data_path)
            self.assertFalse(df.empty)
            self.assertIn('customerID', df.columns)
            self.assertIn('Churn', df.columns)

    def test_preprocessing(self):
        if os.path.exists(self.raw_data_path):
            df = load_data(self.raw_data_path)
            X_train, X_test, y_train, y_test, feature_names, customer_ids, scaler = prepare_data(df)
            self.assertEqual(len(X_train) + len(X_test), len(df))
            self.assertTrue(len(feature_names) > 0)

if __name__ == '__main__':
    unittest.main()
