import joblib
import pandas as pd
import logging
from src.config import Config

def generate_churn_report(X_scaled, customer_ids):
    """Loads best model and generates prediction report."""
    logging.info(f"Loading best model for inference...")
    
    model_data = joblib.load(Config.BEST_MODEL_PATH)
    model = model_data['model']
    model_name = model_data['model_name']
    
    probs = model.predict_proba(X_scaled)[:, 1]
    preds = (probs > 0.5).astype(int)
    
    report = pd.DataFrame({
        'CustomerID': customer_ids,
        'ConfidenceScore': probs,
        'Prediction': ['Churn' if p == 1 else 'Retain' for p in preds]
    })
    
    def get_risk_level(prob):
        if prob > 0.8: return "Critical"
        if prob > 0.6: return "High"
        if prob > 0.4: return "Moderate"
        return "Low"
        
    report['RiskLevel'] = report['ConfidenceScore'].apply(get_risk_level)
    
    logging.info(f"Report generated using {model_name}.")
    return report
