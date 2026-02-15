import pandas as pd
import numpy as np

def engineer_enterprise_features(df_in):
    """
    [PROCESS 5: ADVANCED FEATURE ENGINEERING]
    Strict 1:1 Port of Masterclass Notebook Logic.
    """
    df = df_in.copy()
    
    # 0. Clean numeric types & Handle ID (Institutional Standard)
    if 'customerID' not in df.columns:
        df['customerID'] = [f"CUST-{1000+i}" for i in range(len(df))]
        
    if 'TotalCharges' in df.columns:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    
    # 1. Tenure Categorization (Step 5.1)
    if 'tenure' in df.columns:
        df['tenure_bin'] = pd.cut(df['tenure'], 
                                  bins=[0, 12, 24, 48, 72, 100], 
                                  labels=['New', 'Junior', 'Middle', 'Senior', 'Legend'])
    
    # 2. Risk Indicators (Step 5.2)
    if 'Contract' in df.columns:
        df['is_high_risk_contract'] = df['Contract'].apply(lambda x: 1 if x == 'Month-to-month' else 0)
    
    if 'PaymentMethod' in df.columns:
        df['unstable_payment'] = df['PaymentMethod'].apply(lambda x: 1 if x == 'Electronic check' else 0)
    
    # 3. Behavioral Intensity (Step 5.3)
    # Using the notebook's summation logic for active services
    services = ['PhoneService', 'MultipleLines', 'OnlineSecurity', 
                'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    available_services = [s for s in services if s in df.columns]
    if available_services:
        df['service_count'] = (df[available_services] == 'Yes').sum(axis=1)
    else:
        df['service_count'] = 0
        
    # 4. Economic Value & Price Sensitivity (Step 5.4)
    if 'MonthlyCharges' in df.columns and 'TotalCharges' in df.columns:
        df['price_sensitivity'] = df['MonthlyCharges'] / (df['TotalCharges'].fillna(0) + 1)
        
    if 'MonthlyCharges' in df.columns and 'tenure' in df.columns:
        df['clv_proxy'] = df['MonthlyCharges'] * df['tenure']
        
    return df

if __name__ == "__main__":
    print("✅ [Point 2.0] Masterclass Feature Core Synchronized.")
