import pandas as pd
import io
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DEBUG-CSV")

def clean_col(c):
    c = str(c).strip().strip('"').strip("'")
    c = re.sub(r'^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$', '', c)
    return c

path = 'd:/AI/customer_problem/data/raw/Telco-Customer-Churn.csv'

try:
    with open(path, 'rb') as f:
        contents = f.read()
    
    logger.info(f"File size: {len(contents)} bytes")
    logger.info(f"First 100 bytes: {contents[:100]}")

    df = pd.read_csv(io.BytesIO(contents), encoding='utf-8-sig', sep=None, engine='python')
    logger.info(f"Raw Columns: {df.columns.tolist()}")
    
    cleaned_cols = [clean_col(col) for col in df.columns]
    logger.info(f"Cleaned Columns: {cleaned_cols}")
    
    col_map_lower = {col.lower(): col for col in cleaned_cols}
    logger.info(f"Lowered Map Keys: {list(col_map_lower.keys())}")
    
    if 'customerid' in col_map_lower:
        logger.info("✅ customerid FOUND in cleaned columns.")
    else:
        logger.error("❌ customerid NOT FOUND in cleaned columns.")
        # Check if it's there but maybe joined?
        if any('customerid' in c.lower() for c in cleaned_cols):
            logger.warning("Found 'customerid' as substring in some column!")

except Exception as e:
    logger.error(f"Failed to process CSV: {e}")
