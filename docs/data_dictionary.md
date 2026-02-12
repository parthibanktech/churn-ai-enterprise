# 📋 ChurnAI Institutional Data Dictionary

| Feature | Sheet | Description | Policy |
| :--- | :--- | :--- | :--- |
| **customerID** | Raw | Uniquely identifies the client. | PII Encrypted |
| **tenure** | Raw | Total months of account activity. | Non-negative |
| **clv_proxy** | Engineered | Estimated Lifetime Value (Monthly * Tenure) | Positive Float |
| **is_high_risk** | Engineered | Contract flag for Month-to-Month users. | Binary |
| **price_sensitivity**| Engineered | Ratio of monthly cost to total historical spend. | Float |
| **expected_churn** | Target | Predicted month of account closure. | Prediction Class |

---
*Note: Any feature with >10% drift will trigger an automated retraining event.*
