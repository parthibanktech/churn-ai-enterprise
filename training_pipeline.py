import pandas as pd
import numpy as np
import joblib
import os
import logging
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, classification_report
from scipy.stats import ks_2samp
from xgboost import XGBClassifier

from features.feature_engineering import engineer_enterprise_features
from preprocessing_pipeline import get_preprocessing_pipeline
from src.config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("MASTER-TRAINER")

def run_production_training():
    """
    [PROCESS 7 & 8: CHAMPION TRAINING & EVALUATION]
    Strict 1:1 Port of Masterclass Notebook Methodology.
    """
    logger.info("🎬 [PROCESS 1-2] Ingesting Institutional Data...")
    if not os.path.exists(Config.RAW_DATA_PATH):
        logger.error("🛑 Raw data missing.")
        return

    df_raw = pd.read_csv(Config.RAW_DATA_PATH)
    # Ensure numeric TotalCharges (Masterclass Step 2)
    df_raw['TotalCharges'] = pd.to_numeric(df_raw['TotalCharges'], errors='coerce')

    # [PROCESS 4] Zero-Leakage Policy: Split FIRST
    train_df, test_df = train_test_split(
        df_raw, test_size=0.2, random_state=42, stratify=df_raw['Churn']
    )
    logger.info("✅ [PROCESS 4] Zero-Leakage Split Complete.")

    # [PROCESS 5] Behavioral Feature Synthesis
    train_eng = engineer_enterprise_features(train_df)
    test_eng = engineer_enterprise_features(test_df)

    # Define Feature Sets (Step 6)
    num_features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'clv_proxy', 'price_sensitivity', 'service_count']
    cat_features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Contract', 'PaymentMethod', 'tenure_bin']

    # [PROCESS 6] Build Pipeline
    preprocessor = get_preprocessing_pipeline(num_features, cat_features)

    # [PROCESS 7] Champion Algorithm (Gradient Boosting)
    # Swapped from XGBoost to Gradient Boosting as it achieved 0.8437 in benchmarks
    from sklearn.ensemble import GradientBoostingClassifier
    clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
    
    champion_pipeline = Pipeline([
        ('prep', preprocessor),
        ('clf', clf)
    ])

    # Training
    X_train = train_eng.drop('Churn', axis=1)
    y_train = train_eng['Churn'].map({'Yes': 1, 'No': 0})
    
    logger.info("🚀 [PROCESS 7] Fitting Champion Engine (Gradient Boosting)...")
    champion_pipeline.fit(X_train, y_train)

    # [PROCESS 8] Professional Metric Evaluation
    X_test = test_eng.drop('Churn', axis=1)
    y_test = test_eng['Churn'].map({'Yes': 1, 'No': 0})
    
    probs = champion_pipeline.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probs)
    ks_stat, _ = ks_2samp(probs[y_test == 1], probs[y_test == 0])
    
    logger.info("🏆 [PROCESS 8] Meta-Metrics: AUC=%.4f, KS=%.4f", auc, ks_stat)

    # Serialization
    bundle = {
        'pipeline': champion_pipeline,
        'metadata': {
            'auc_score': float(auc),
            'ks_stat': float(ks_stat),
            'features': X_train.columns.tolist(),
            'standard': "ChurnAI Masterclass 2.0",
            'engine': "Gradient Boosting Champion"
        }
    }
    
    os.makedirs(Config.MODELS_DIR, exist_ok=True)
    bundle_path = os.path.join(Config.MODELS_DIR, "production_pipeline_bundle.joblib")
    joblib.dump(bundle, bundle_path)
    logger.info("⛳️ Bundle Serialized: %s", bundle_path)

if __name__ == "__main__":
    run_production_training()
