# 💎 ChurnAI Enterprise: Institutional Prediction System
### *15-Year Standard Machine Learning Production Framework*

---

## 🏢 1. Executive Problem Statement
Customer Retention is the primary driver of profitability in the subscription economy. 
*   **The Problem**: Our client is experiencing "Silent Churn"—customers leaving without overt complaints, leading to a significant decay in **LTV (Lifetime Value)** and **ARR (Annual Recurring Revenue)**.
*   **The Mandate**: Build a production-ready AI system that:
    1.  **Identifies** high-risk individuals with >85% precision.
    2.  **Explains** the "Why" (Reason Codes) for intervention.
    3.  **Forecasts** the exact survival window (Expected Churn Month).
*   **Business Impact**: Reducing churn by just **5%** can increase profits by **25% to 95%**.

---

## 🚀 2. Digital Project Architecture (Point 20.0)
This project is organized into modular "Institutional Sheets" representing the 20-point production standard:

| Module | Core Responsibility | Standard |
| :--- | :--- | :--- |
| `data_validation/` | Pandera Schema & Drift Gates | 1.1 |
| `features/` | Behavioral Synthesis (CLV, Intensity) | 2.0 |
| `preprocessing_pipeline.py`| Leakage-Safe ColumnTransformers | 4.0 |
| `model_training.py` | Stratified K-Fold Meta-Validation | 7.0 |
| `model_evaluation.py` | KS Statistic, PR-AUC, Calibration | 8.0 |
| `explainability.py` | SHAP Global/Local Intelligence | 9.0 |
| `forecasting.py` | Survival Attrition Horizons | 11.0 |
| `api_service/` | FastAPI Inference Hub | 13.0 |
| `docs/` | Model Cards & Data Dictionary | 18.0 |

---

## 🛡️ 3. The 20-Point ML Production Standard
1.  **Data Security**: PII Masking and Access Control.
2.  **Zero Leakage**: Strict `Split-First` policy for all preprocessing.
3.  **Calibration**: Probability matching using Brier scores.
4.  **Monitoring**: Real-time drift detection and latency tracking.

---

## 🛠️ 4. Quick Start
1.  **Training**: `python training_pipeline.py`
2.  **Launch SaaS**: `start.bat`
3.  **Research**: Open `single_file_DS_Masterclass.ipynb` for the full experimental walkthrough.

---
*Created by AntiGravity - 15-Year Data Science Professional Protocol.*
