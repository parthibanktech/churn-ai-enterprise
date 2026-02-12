import joblib
import logging
import pandas as pd
import time
from sklearn.metrics import accuracy_score, roc_auc_score
from src.models_factory import get_algorithm_suite
from src.config import Config

def train_and_benchmark(X_train, X_test, y_train, y_test, feature_names):
    """Benchmarks 20 algorithms and saves the best one."""
    logging.info(f"Starting benchmark of 20 algorithms on {len(X_train)} samples...")
    
    models = get_algorithm_suite(Config.RANDOM_STATE)
    results = []
    best_auc = 0
    best_model_obj = None
    best_model_name = ""

    for name, model in models.items():
        start_time = time.time()
        try:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            if hasattr(model, "predict_proba"):
                y_prob = model.predict_proba(X_test)[:, 1]
                auc = roc_auc_score(y_test, y_prob)
            else:
                auc = roc_auc_score(y_test, y_pred)
            
            acc = accuracy_score(y_test, y_pred)
            elapsed = time.time() - start_time
            
            results.append({
                "Algorithm": name,
                "ROC-AUC": auc,
                "Accuracy": acc,
                "Training Time (s)": elapsed
            })
            
            logging.info(f"✅ {name:20} | AUC: {auc:.4f}")
            
            if auc > best_auc:
                best_auc = auc
                best_model_obj = model
                best_model_name = name
                
        except Exception as e:
            logging.error(f"❌ {name} failed: {e}")

    results_df = pd.DataFrame(results).sort_values(by="ROC-AUC", ascending=False)
    results_df.to_csv(Config.BENCHMARK_REPORT_PATH, index=False)
    
    payload = {
        'model': best_model_obj,
        'model_name': best_model_name,
        'auc': best_auc,
        'feature_names': feature_names
    }
    joblib.dump(payload, Config.BEST_MODEL_PATH)
    
    logging.info(f"🏆 BEST MODEL: {best_model_name} (AUC: {best_auc:.4f})")
    return results_df
