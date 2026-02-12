import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(filepath):
    """Loads dataset from the given filepath."""
    logging.info(f"Loading data from {filepath}")
    try:
        df = pd.read_csv(filepath)
        
        # --- Institutional Type Safety (15-Year Standard) ---
        # TotalCharges often contains spaces in the raw CSV
        if 'TotalCharges' in df.columns:
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
            logging.info("TotalCharges converted to numeric (Float64).")
            
        logging.info(f"Data loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise e
