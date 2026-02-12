# 📡 ChurnAI Production Monitoring Policy

## 1. Input Drift (Point 14.0)
*   **Threshold**: Any feature showing a Kolmogorov-Smirnov (KS) p-value < 0.05.
*   **Action**: Alert Data Engineering for potential source data change.

## 2. Prediction Drift
*   **Metric**: Population Stability Index (PSI).
*   **Threshold**: PSI > 0.2 (High change).
*   **Action**: Internal trigger for `automated_retraining.py`.

## 3. Performance Decay
*   **SLA**: ROC-AUC must remain above 0.78 for "Institutional" status.
*   **Latency**: Inference must respond within < 150ms.

---
*Tools Integrated: Evidently AI baseline, Prometheus metrics.*
