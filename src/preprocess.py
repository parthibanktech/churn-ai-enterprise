import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
import logging
from src.config import Config

def prepare_data(df):
    """
    Complete professional pipeline for data preparation.
    1. Cleaning
    2. Feature Extraction
    3. Splitting
    4. Scaling
    """
    logging.info("Preparing data for training...")
    
    # 1. Cleaning
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
    
    # --- ENTERPRISE OUTLIER POLICY (15-Year Standard) ---
    # Winsorization: Clipping extreme 1% outliers to prevent model distortion
    num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    for col in num_cols:
        upper = df[col].quantile(0.99)
        lower = df[col].quantile(0.01)
        df[col] = np.clip(df[col], lower, upper)
    logging.info("✅ Outlier policy applied (Winsorization 1%).")
    
    # 2. Extract Target and IDs
    customer_ids = df['customerID']
    y = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
    
    # 3. Drop non-features
    X = df.drop(['customerID', 'Churn'], axis=1)
    
    # 4. Encoding
    categorical_cols = X.select_dtypes(include=['object']).columns
    X_encoded = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    feature_names = X_encoded.columns.tolist()
    
    # 5. Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=Config.TEST_SIZE, random_state=Config.RANDOM_STATE, stratify=y
    )
    
    # 6. Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Save the scaler for future inference
    os.makedirs(Config.MODELS_DIR, exist_ok=True)
    joblib.dump(scaler, os.path.join(Config.MODELS_DIR, "scaler.joblib"))
    
    return X_train_scaled, X_test_scaled, y_train, y_test, feature_names, customer_ids, scaler

def prepare_for_inference(df, scaler):
    """Prepares raw data for prediction using a pre-trained scaler."""
    df_clean = df.copy()
    df_clean['TotalCharges'] = pd.to_numeric(df_clean['TotalCharges'], errors='coerce')
    df_clean['TotalCharges'].fillna(df_clean['TotalCharges'].median(), inplace=True)
    
    customer_ids = df_clean['customerID']
    if 'Churn' in df_clean.columns:
        df_clean.drop('Churn', axis=1, inplace=True)
    df_clean.drop('customerID', axis=1, inplace=True)
    
    X_encoded = pd.get_dummies(df_clean, drop_first=True)
    X_scaled = scaler.transform(X_encoded)
    
    return X_scaled, customer_ids
