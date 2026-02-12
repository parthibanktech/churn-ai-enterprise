import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.metrics import make_scorer, roc_auc_score

def train_enterprise_models(X, y):
    """
    Implements Point 7.0 & 6.0: Cross-validation and Imbalance handling.
    """
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    
    # Define models with class_weight optimization (Point 6.0)
    models = {
        "XGBoost": XGBClassifier(scale_pos_weight=3, eval_metric='logloss', random_state=42),
        "LightGBM": LGBMClassifier(class_weight='balanced', random_state=42, verbose=-1),
        "CatBoost": CatBoostClassifier(auto_class_weights='Balanced', verbose=0, random_state=42),
        "Random Forest": RandomForestClassifier(class_weight='balanced', random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(random_state=42)
    }
    
    benchmark = []
    print("🚀 Training with Stratified 5-Fold Cross-Validation...")
    
    for name, model in models.items():
        # Point 7.0: Cross validation
        scores = cross_val_score(model, X, y, cv=skf, scoring='roc_auc')
        benchmark.append({
            "Algorithm": name,
            "Mean_AUC": np.mean(scores),
            "Std_AUC": np.std(scores)
        })
        print(f"🔹 {name:20} | Mean AUC: {np.mean(scores):.4f}")
        
    return pd.DataFrame(benchmark).sort_values(by="Mean_AUC", ascending=False)

if __name__ == "__main__":
    print("✅ Model Training Module Initialized (Point 7.0)")
