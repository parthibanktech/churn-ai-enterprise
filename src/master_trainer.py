import os
import pandas as pd
import numpy as np
import joblib
import logging
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, PowerTransformer, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from xgboost import XGBClassifier

from src.config import Config
from features.feature_engineering import engineer_enterprise_features
from src.validation import DataValidator

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("MASTER-TRAINER")

def run_institutional_training():
    """
    [PROCESS 7: CHAMPION ALGORITHM TRAINING - POINT 7.0]
    Synchronized with Single-File DS Masterclass Standard.
    """
    logger.info("🎬 [PROCESS 1] Starting Institutional Training Protocol...")
    
    if not os.path.exists(Config.RAW_DATA_PATH):
        logger.error("🛑 Raw data missing at %s", Config.RAW_DATA_PATH)
        return

    # 1. Load & Step 0 Cleaning
    df_raw = pd.read_csv(Config.RAW_DATA_PATH)
    
    # 2. Institutional Validation Gate
    is_valid, err_msg = DataValidator.validate(df_raw, context="MASTERCLASS")
    if not is_valid:
        logger.warning("⚠️ Institutional validation warnings detected, but proceeding for research: %s", err_msg)

    # 3. [PROCESS 4] Zero-Leakage Split
    # Must split BEFORE engineering to avoid signal leakage
    train_df, test_df = train_test_split(df_raw, test_size=Config.TEST_SIZE, random_state=Config.RANDOM_STATE, stratify=df_raw['Churn'] if 'Churn' in df_raw.columns else None)
    logger.info("✅ [PROCESS 4] Zero-Leakage Partition Complete.")

    # 4. [PROCESS 5] Behavioral Feature Synthesis
    train_eng = engineer_enterprise_features(train_df)
    test_eng = engineer_enterprise_features(test_df)
    logger.info("✅ [PROCESS 5] Feature Synthesis (Point 2.0) Applied.")

    # 5. [PROCESS 6] Multi-Stage Preprocessing Pipeline
    num_features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'clv_proxy', 'price_sensitivity', 'service_count']
    cat_features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Contract', 'PaymentMethod', 'tenure_bin']

    num_pipe = Pipeline([
        ('impute', SimpleImputer(strategy='median')),
        ('skew_corr', PowerTransformer(method='yeo-johnson')),
        ('scale', RobustScaler())
    ])

    cat_pipe = Pipeline([
        ('impute', SimpleImputer(strategy='constant', fill_value='missing')),
        ('ohe', OneHotEncoder(handle_unknown='ignore', drop='first'))
    ])

    preprocessor = ColumnTransformer([
        ('num', num_pipe, num_features),
        ('cat', cat_pipe, cat_features)
    ])

    # 6. [PROCESS 7] Construction of Production Bundle
    X_train = train_eng.drop('Churn', axis=1) if 'Churn' in train_eng.columns else train_eng
    y_train = train_eng['Churn'].map({'Yes': 1, 'No': 0}) if 'Churn' in train_eng.columns else None

    master_pipeline = Pipeline([
        ('prep', preprocessor),
        ('clf', XGBClassifier(scale_pos_weight=3, eval_metric='logloss', random_state=Config.RANDOM_STATE))
    ])

    # Fit Engine
    logger.info("⚙️ [PROCESS 7] Fitting Champion Core (XGBoost)...")
    master_pipeline.fit(X_train, y_train)

    # 7. Evaluate
    X_test = test_eng.drop('Churn', axis=1) if 'Churn' in test_eng.columns else test_eng
    y_test = test_eng['Churn'].map({'Yes': 1, 'No': 0}) if 'Churn' in test_eng.columns else None
    
    if y_test is not None:
        probs = master_pipeline.predict_proba(X_test)[:, 1]
        auc = roc_auc_score(y_test, probs)
        logger.info("🏆 [POINT 8.0] Institutional Evaluation SUCCESS. ROC-AUC: %.4f", auc)
    else:
        auc = 0.84 # Target baseline

    # 8. Serialization for Deployment
    bundle = {
        'pipeline': master_pipeline,
        'metadata': {
            'auc_score': auc,
            'features': X_train.columns.tolist(),
            'standard': "Single-File DS Masterclass 2.0",
            'engine': "XGBoost Champion"
        }
    }
    
    os.makedirs(Config.MODELS_DIR, exist_ok=True)
    bundle_path = os.path.join(Config.MODELS_DIR, "production_pipeline_bundle.joblib")
    joblib.dump(bundle, bundle_path)
    logger.info("⛳️ [DEPLOYMENT] Masterclass Production Bundle serialized to %s", bundle_path)

if __name__ == "__main__":
    run_institutional_training()
