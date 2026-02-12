import pandas as pd
import numpy as np
import os
import joblib
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score, classification_report
from xgboost import XGBClassifier
import io

# ==========================================
# 💎 SINGLE-FILE DS MASTERCLASS: CHURNAI v2.0
# ==========================================

# 1. SETUP & CONFIGURATION
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("DS-Masterclass")

class MasterConfig:
    DATA_PATH = "data/raw/Telco-Customer-Churn.csv"
    MODEL_SAVE_PATH = "models/masterclass_pipeline.joblib"
    RANDOM_STATE = 42
    TEST_SIZE = 0.2

# 2. THE ENGINEERING CORE
def engineer_masterclass_features(df):
    """Institutional-Grade Feature Engineering."""
    df = df.copy()
    
    # Clean numeric errors
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    
    # Core Engineering
    df['tenure_group'] = pd.cut(df['tenure'], bins=[0, 12, 24, 48, 60, 100], labels=['0-1yr', '1-2yr', '2-4yr', '4-5yr', '5yr+'])
    
    services = ['PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity', 
                'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    
    available_services = [s for s in services if s in df.columns]
    df['service_count'] = df[available_services].apply(lambda x: sum((x != 'No') & (x != 'No internet service')), axis=1)
    
    df['high_monthly_risk'] = (df['MonthlyCharges'] > df['MonthlyCharges'].median()).astype(int)
    
    return df

# 3. PIPELINE ARCHITECTURE
def build_master_pipeline():
    """Constructs a production-ready sklearn pipeline."""
    numeric_features = ['tenure', 'MonthlyCharges', 'TotalCharges', 'service_count']
    categorical_features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Contract', 
                            'PaperlessBilling', 'PaymentMethod', 'tenure_group']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )
    
    model = XGBClassifier(
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        scale_pos_weight=3,  # Handling class imbalance
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    return Pipeline([
        ('preprocessor', preprocessor),
        ('classifier', model)
    ])

# 4. TRAINING PROTOCOL
def run_masterclass_training():
    """Executes the full training and serialization cycle."""
    if not os.path.exists(MasterConfig.DATA_PATH):
        logger.error("Dataset not found. Initiation aborted.")
        return
    
    df = pd.read_csv(MasterConfig.DATA_PATH)
    df = engineer_masterclass_features(df)
    
    X = df.drop(['customerID', 'Churn'], axis=1) if 'Churn' in df.columns else df.drop(['customerID'], axis=1)
    y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=MasterConfig.TEST_SIZE, random_state=MasterConfig.RANDOM_STATE)
    
    pipeline = build_master_pipeline()
    pipeline.fit(X_train, y_train)
    
    probs = pipeline.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, probs)
    
    logger.info(f"✅ Masterclass Protocol Complete. AUC: {auc:.4f}")
    
    # Serialize for Deployment
    os.makedirs(os.path.dirname(MasterConfig.MODEL_SAVE_PATH), exist_ok=True)
    joblib.dump({"pipeline": pipeline, "auc": auc, "features": X.columns.tolist()}, MasterConfig.MODEL_SAVE_PATH)
    return pipeline

# 5. DEPLOYMENT LAYER (FastAPI)
app = FastAPI(title="ChurnAI Masterclass API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "Institutional Grade - Operational"}

@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    if not os.path.exists(MasterConfig.MODEL_SAVE_PATH):
        # Trigger training if model missing
        run_masterclass_training()
    
    payload = joblib.load(MasterConfig.MODEL_SAVE_PATH)
    pipeline = payload['pipeline']
    
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    
    # Pre-processing & Engineering
    df_eng = engineer_masterclass_features(df)
    
    # Inference
    probs = pipeline.predict_proba(df_eng)[:, 1]
    
    results = df.copy()
    results['ChurnProbability'] = probs
    results['RiskLevel'] = ["Critical" if p > 0.8 else "High" if p > 0.6 else "Moderate" if p > 0.4 else "Low" for p in probs]
    
    return results[['customerID', 'MonthlyCharges', 'tenure', 'ChurnProbability', 'RiskLevel']].head(1000).to_dict(orient="records")

if __name__ == "__main__":
    import uvicorn
    # First, ensure we have a model
    if not os.path.exists(MasterConfig.MODEL_SAVE_PATH):
        run_masterclass_training()
    uvicorn.run(app, host="0.0.0.0", port=8001)
