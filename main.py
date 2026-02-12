import argparse
import logging
import os
import pandas as pd
from src.config import Config
from src.data_loader import load_data
from src.preprocess import prepare_data
from src.train import train_and_benchmark
from src.predict import generate_churn_report
from src.visualization import generate_production_figures

# Setup Professional Logging
os.makedirs(Config.REPORTS_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(Config.REPORTS_DIR, "production.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("ChurnEngine")

from src.validation import DataValidator

def main():
    parser = argparse.ArgumentParser(description="Professional Churn Prediction Engine")
    parser.add_argument("--mode", choices=["train", "predict", "full"], default="full", help="Pipeline mode")
    args = parser.parse_args()

    logger.info("Initializing Churn Prediction Pipeline")

    # 1. Load
    raw_df = load_data(Config.RAW_DATA_PATH)
    
    # --- ENTERPRISE VALIDATION GATE (15-Year Standard) ---
    if not DataValidator.validate(raw_df, context="Training"):
        logger.error("🛑 Pipeline terminated due to data integrity violations.")
        return

    # 2. Preprocess
    X_train, X_test, y_train, y_test, feature_names, customer_ids, scaler = prepare_data(raw_df)

    # 3. Benchmark & Train (20 Algorithms)
    if args.mode in ["train", "full"]:
        benchmark_results = train_and_benchmark(X_train, X_test, y_train, y_test, feature_names)
        generate_production_figures(Config.RAW_DATA_PATH)

    # 4. Generate High-Risk Report
    if args.mode in ["predict", "full"]:
        # Prepare full scaled data for inference
        X_full_columns = pd.get_dummies(raw_df.drop(['customerID', 'Churn'], axis=1), drop_first=True)
        X_full_scaled = scaler.transform(X_full_columns)
        
        report = generate_churn_report(X_full_scaled, raw_df['customerID'])
        
        # Save high-risk targets
        high_risk = report[report['RiskLevel'].isin(['Critical', 'High'])].sort_values(by='ConfidenceScore', ascending=False)
        high_risk.to_csv(Config.CHURN_REPORT_PATH, index=False)
        
        logger.info(f"Report complete: {len(high_risk)} high-risk targets identified.")
        print(f"\n🎯 PIPELINE SUCCESSFUL. Report saved to: {Config.CHURN_REPORT_PATH}")

if __name__ == "__main__":
    main()
