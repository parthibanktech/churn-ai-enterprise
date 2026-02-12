import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_feature_importance(model, feature_names):
    """
    Implements Point 9.0: Model Interpretability.
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    else:
        # Fallback for models without feature_importances_
        importances = np.zeros(len(feature_names))
        
    feat_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    }).sort_values(by='Importance', ascending=False)
    
    return feat_df

def generate_reason_codes(customer_row, model, feature_names):
    """
    Experimental: Point 9.0 Reason codes per customer.
    Identifying top features contributing to a specific prediction.
    """
    # Heuristic-based local explanation:
    # We look for features that are high and generally associated with churn
    reasons = []
    
    if customer_row.get('Contract') == 'Month-to-month':
        reasons.append("Month-to-Month Contract")
    
    if customer_row.get('PaymentMethod') == 'Electronic check':
        reasons.append("Electronic Check Payment")

    if pd.to_numeric(customer_row.get('MonthlyCharges', 0)) > 70:
        reasons.append("High Monthly Charges")

    if pd.to_numeric(customer_row.get('tenure', 0)) < 6:
        reasons.append("New Customer (Fragile Window)")
    
    if customer_row.get('InternetService') == 'Fiber optic':
        reasons.append("Fiber Optic Service (High Churn Segment)")

    if not reasons:
        return "Behavioral Patterns (Composite Risk)"
    
    return " + ".join(reasons[:2])

if __name__ == "__main__":
    print("✅ Explainability Module Initialized (Point 9.0)")
