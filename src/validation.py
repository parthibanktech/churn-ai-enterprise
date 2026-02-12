import pandera as pa
from pandera import Check, Column, DataFrameSchema
import pandas as pd
import logging

# Configure Enterprise Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataValidator:
    """
    Enterprise Data Validation Layer (15-Year Standard)
    Implements Schema Validation, Duplicate Detection, and Null Policy auditing.
    """
    
    # Institutional Schema Definition
    SCHEMA = DataFrameSchema({
        "customerID": Column(str, unique=True, required=False),
        "tenure": Column(int, Check.greater_than_or_equal_to(0), required=False),
        "MonthlyCharges": Column(float, Check.in_range(0, 1000), required=False),
        "TotalCharges": Column(float, nullable=True, required=False),
        "Churn": Column(str, Check.isin(["Yes", "No"]), required=False)
    })

    @staticmethod
    def validate(df: pd.DataFrame, context: str = "Production") -> tuple[bool, str]:
        """
        Executes the full validation suite. Returns (is_valid, error_message).
        """
        logger.info(f"🛡️ Initializing {context} Data Validation Protocol...")
        
        # 1. Schema Validation (Pandera)
        try:
            DataValidator.SCHEMA.validate(df, lazy=True)
            logger.info("✅ Schema Validation: SUCCESS")
        except pa.errors.SchemaErrors as err:
            err_msg = f"Schema mapping violation: {str(err)}"
            logger.error(f"❌ Schema Validation: FAILED\n{err_msg}")
            # Format error message to be more human readable if it's a type error
            if "expected series" in err_msg and "TotalCharges" in err_msg:
                err_msg = "Critical Type Skew: 'TotalCharges' contains non-numeric characters (e.g. spaces). Ensure data is cleaned."
            return False, err_msg

        # 2. Duplicate Detection
        if "customerID" in df.columns:
            duplicates = df.duplicated("customerID").sum()
            if duplicates > 0:
                err_msg = f"Institutional Safety violation: {duplicates} non-unique customer instances detected."
                logger.error(f"❌ Duplicate Detection: FAILED ({err_msg})")
                return False, err_msg
        logger.info("✅ Duplicate Detection: SUCCESS")

        # 3. Null Policy & Sparsity Audit
        null_counts = df.isnull().sum()
        sparsity = (null_counts / len(df)) * 100
        critical_nulls = sparsity[sparsity > 25].index.tolist() # Slightly more relaxed for serves
        
        if critical_nulls:
            err_msg = f"Data Quality violation: Features {critical_nulls} exceed the 25% null threshold."
            logger.error(f"❌ Null Policy Audit: FAILED ({err_msg})")
            return False, err_msg
            
        logger.info("✅ Null Policy Audit: COMPLETE")

        return True, ""

    @staticmethod
    def detect_drift(current_df: pd.DataFrame, reference_df: pd.DataFrame) -> dict:
        """
        Basic Statistical Drift Detection (KS-Test)
        """
        from scipy.stats import ks_2samp
        drift_report = {}
        
        num_cols = current_df.select_dtypes(include=['number']).columns
        for col in num_cols:
            if col in reference_df.columns:
                stat, p_val = ks_2samp(current_df[col].dropna(), reference_df[col].dropna())
                drift_report[col] = {"drift_detected": p_val < 0.05, "p_value": p_val}
        
        return drift_report
