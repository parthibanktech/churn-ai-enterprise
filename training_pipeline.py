import pandas as pd
import numpy as np
import joblib
import os
import logging
import time
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score
from scipy.stats import ks_2samp

from features.feature_engineering import engineer_enterprise_features
from preprocessing_pipeline import get_preprocessing_pipeline
from src.config import Config
from src.models_factory import get_algorithm_suite

# Setup Logging
os.makedirs(Config.REPORTS_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(Config.REPORTS_DIR, "training.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("UNIFIED-TRAINER")

def run_benchmarking_and_training():
    """
    1. Ingest Data
    2. Zero-Leakage Split
    3. Feature Engineering
    4. Benchmark 20 Algorithms
    5. Select Champion
    6. Package Production Bundle
    """
    logger.info("🎬 Initializing Unified Training Pipeline...")
    
    if not os.path.exists(Config.RAW_DATA_PATH):
        logger.error(f"🛑 Raw data missing at {Config.RAW_DATA_PATH}")
        return

    # 1. Ingest
    df_raw = pd.read_csv(Config.RAW_DATA_PATH)
    df_raw['TotalCharges'] = pd.to_numeric(df_raw['TotalCharges'], errors='coerce')
    
    # 2. Split FIRST (Zero Leakage)
    train_df, test_df = train_test_split(
        df_raw, test_size=Config.TEST_SIZE, random_state=Config.RANDOM_STATE, stratify=df_raw['Churn']
    )
    logger.info("✅ Zero-Leakage Split Complete.")

    # 3. Feature Engineering
    train_eng = engineer_enterprise_features(train_df)
    test_eng = engineer_enterprise_features(test_df)
    
    # Define Features
    num_features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'clv_proxy', 'price_sensitivity', 'service_count']
    cat_features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Contract', 'PaymentMethod', 'tenure_bin']
    
    # 4. Preprocessing Pipeline
    preprocessor = get_preprocessing_pipeline(num_features, cat_features)
    
    X_train = train_eng.drop('Churn', axis=1)
    y_train = train_eng['Churn'].map({'Yes': 1, 'No': 0})
    X_test = test_eng.drop('Churn', axis=1)
    y_test = test_eng['Churn'].map({'Yes': 1, 'No': 0})

    # Prepare data for benchmarking (Sklearn models need numerical input)
    # We use the preprocessor to transform data once for benchmarking
    logger.info("🛠️ Preprocessing data for multi-algorithm benchmark...")
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)
    
    # 5. Benchmark 20 Algorithms
    logger.info("🚀 Starting Benchmark of 20 Algorithms...")
    suite = get_algorithm_suite(Config.RANDOM_STATE)
    benchmark_results = []
    
    best_auc = 0
    champion_model = None
    champion_name = ""

    for name, model in suite.items():
        start = time.time()
        try:
            model.fit(X_train_proc, y_train)
            
            if hasattr(model, "predict_proba"):
                probs = model.predict_proba(X_test_proc)[:, 1]
            else:
                probs = model.predict(X_test_proc)
                
            auc = roc_auc_score(y_test, probs)
            acc = accuracy_score(y_test, (probs > 0.5).astype(int))
            elapsed = time.time() - start
            
            benchmark_results.append({
                "algorithm": name,
                "roc_auc": float(auc),
                "accuracy": float(acc),
                "training_time": float(elapsed)
            })
            
            logger.info(f"✅ {name:25} | AUC: {auc:.4f} | Time: {elapsed:.2f}s")
            
            if auc > best_auc:
                best_auc = auc
                champion_model = model
                champion_name = name
                
        except Exception as e:
            logger.error(f"❌ {name} failed: {str(e)}")

    # Save Results
    results_df = pd.DataFrame(benchmark_results).sort_values(by="roc_auc", ascending=False)
    results_df.to_csv(Config.BENCHMARK_REPORT_PATH, index=False)
    logger.info(f"📊 Benchmark Report Saved to {Config.BENCHMARK_REPORT_PATH}")

    # 6. Serializing Champion Bundle
    logger.info(f"🏆 CHAMPION IDENTIFIED: {champion_name} (AUC: {best_auc:.4f})")
    
    # Re-wrap the best model into a full Pipeline for production
    # This ensures deployment only needs raw data
    production_pipeline = Pipeline([
        ('prep', preprocessor),
        ('clf', champion_model)
    ])
    
    # Calculate KS Stat for the champion
    champion_probs = production_pipeline.predict_proba(X_test)[:, 1]
    ks_stat, _ = ks_2samp(champion_probs[y_test == 1], champion_probs[y_test == 0])

    bundle = {
        'pipeline': production_pipeline,
        'metadata': {
            'auc_score': float(best_auc),
            'ks_stat': float(ks_stat),
            'engine': champion_name,
            'version': "2.5.0",
            'last_updated': time.strftime("%Y-%m-%d"),
            'features': X_train.columns.tolist()
        }
    }
    
    os.makedirs(Config.MODELS_DIR, exist_ok=True)
    bundle_path = os.path.join(Config.MODELS_DIR, "production_pipeline_bundle.joblib")
    joblib.dump(bundle, bundle_path)
    
    logger.info(f"⛳️ Production Bundle Serialized: {bundle_path}")
    logger.info("✨ Unified Training Pipeline Complete.")

if __name__ == "__main__":
    run_benchmarking_and_training()
