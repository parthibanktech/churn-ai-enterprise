import pytest
import pandas as pd
import numpy as np
import os
import joblib
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from features.feature_engineering import engineer_enterprise_features
from training_pipeline import run_production_training
from src.config import Config

def test_feature_engineering_robustness():
    # Create sample data with potential issues
    df = pd.DataFrame({
        'tenure': [1, 0, 50],
        'MonthlyCharges': [10.0, 20.0, 30.0],
        'TotalCharges': ['10.0', ' ', '1500.0'], # String with space
        'Contract': ['Month-to-month', 'One year', 'Two year'],
        'PaymentMethod': ['Electronic check', 'Mailed check', 'Bank transfer'],
        'PhoneService': ['Yes', 'No', 'Yes'],
        'MultipleLines': ['No', 'No phone service', 'Yes'],
        'InternetService': ['DSL', 'No', 'Fiber optic'],
        'OnlineSecurity': ['No', 'No internet service', 'Yes'],
        'OnlineBackup': ['Yes', 'No internet service', 'No'],
        'DeviceProtection': ['No', 'No internet service', 'Yes'],
        'TechSupport': ['No', 'No internet service', 'No'],
        'StreamingTV': ['Yes', 'No internet service', 'Yes'],
        'StreamingMovies': ['No', 'No internet service', 'Yes']
    })
    
    df_eng = engineer_enterprise_features(df)
    
    assert 'tenure_bin' in df_eng.columns
    assert 'service_count' in df_eng.columns
    assert df_eng['TotalCharges'].astype(float).sum() > 0
    assert not df_eng['TotalCharges'].isna().any()
    assert df_eng.loc[1, 'TotalCharges'] == 0 # 0 * 20.0

def test_pipeline_training():
    # Only run if raw data exists
    if not os.path.exists(Config.RAW_DATA_PATH):
        pytest.skip("Raw data not found")
        
    pipeline, bundle_path = run_production_training()
    
    assert pipeline is not None
    assert os.path.exists(bundle_path)
    
    # Load and check
    payload = joblib.load(bundle_path)
    assert 'pipeline' in payload
    assert 'auc_score' in payload

if __name__ == "__main__":
    # Manual run
    test_feature_engineering_robustness()
    print("Tests passed locally!")
