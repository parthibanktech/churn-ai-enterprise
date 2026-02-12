import pandera as pa
from pandera import Check, Column, DataFrameSchema
import logging

# Institutional Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DataGate")

# [Point 1.1] Institutional Schema Gate
ENERP_SCHEMA = DataFrameSchema({
    "customerID": Column(str, unique=True),
    "tenure": Column(int, Check.greater_than_or_equal_to(0)),
    "MonthlyCharges": Column(float, Check.greater_than_or_equal_to(0)),
    "TotalCharges": Column(float, nullable=True),
    "Churn": Column(str, Check.isin(["Yes", "No"]), required=False)
})

def validate_dataset(df, stage="Inference"):
    """Enforces strict schema contract (15-Year Standard)"""
    logger.info(f"🛡️ Initializing {stage} Validation Gate...")
    try:
        ENERP_SCHEMA.validate(df, lazy=True)
        logger.info("✅ Schema Validation: SUCCESS")
        return True
    except Exception as e:
        logger.error(f"❌ Schema Validation: FAILED\n{e}")
        return False
