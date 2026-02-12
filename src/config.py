import os

class Config:
    # Project Root
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # Data Paths
    RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "Telco-Customer-Churn.csv")
    PROCESSED_DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "customers_processed.csv")
    
    # Model Paths
    MODELS_DIR = os.path.join(BASE_DIR, "models")
    BEST_MODEL_PATH = os.path.join(MODELS_DIR, "best_model.joblib")
    
    # Output Paths
    FIGURES_DIR = os.path.join(BASE_DIR, "outputs", "figures")
    REPORTS_DIR = os.path.join(BASE_DIR, "outputs", "reports")
    CHURN_REPORT_PATH = os.path.join(REPORTS_DIR, "high_risk_customers.csv")
    BENCHMARK_REPORT_PATH = os.path.join(REPORTS_DIR, "algorithm_benchmark.csv")
    
    # Random State
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
