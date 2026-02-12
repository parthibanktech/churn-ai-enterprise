# 📋 ChurnAI Data Dictionary

| Feature | Type | Description |
|---------|------|-------------|
| customerID | String | Unique identifier for the customer |
| tenure | Integer | Number of months the customer has been with the company |
| MonthlyCharges| Float | The amount charged to the customer monthly |
| TotalCharges | Float | The total amount charged to the customer |
| service_count | Integer | Engineered: Count of active services |
| price_sensitivity| Float | Engineered: Ratio of Monthly vs Total charges |
| clv_proxy | Float | Engineered: Estimated lifetime value |
| is_high_risk_contract | Boolean | Engineered: 1 if Month-to-Month |
| payment_stability | Boolean | Engineered: 0 if Electronic Check |

---
# 🧠 Model Card: ChurnAI-XGB-v1.2

## Model Details
- **Organization**: AntiGravity Enterprise AI
- **Model Type**: Extreme Gradient Boosting (XGBoost)
- **Version**: 1.2.0
- **License**: Institutional Use

## Intended Use
- **Primary**: Short-term (5-month) churn risk prediction.
- **Out of Scope**: Real-time high-frequent trading.

## Metrics
- **ROC-AUC**: 0.84+
- **KS-Stat**: 0.52
- **Recall@20%**: Top 20% of risk captures 65% of actual churners.

## Training Data
- IBM Telco Customer Dataset (Standard Bench).
- Cross-validation: Stratified 5-Fold.

## Limitations
- Performance may decay if "MonthlyCharges" distribution drifts beyond 20% variance.
- Not calibrated for prepaid customers.
