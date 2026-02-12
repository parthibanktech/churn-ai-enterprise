# ChurnAI Enterprise - Production Readiness Guide

This document outlines the production-ready features implemented in the ChurnAI platform.

## 🚀 Key Features

1.  **Unified ML Pipeline**:
    *   Transitioned from manual scaling/encoding to a robust `sklearn.pipeline.Pipeline` with `ColumnTransformer`.
    *   Leakage prevention: Feature engineering and preprocessing are handled independently for train/test splits.
    *   Artifact bundling: Saves a unified `.joblib` containing the full pipeline, metadata, and evaluation scores.

2.  **Enterprise Data Validation**:
    *   Integrated `Pandera` for strict schema validation during both training and inference.
    *   Robust handling of Telco-specific data quirks (e.g., spaces in `TotalCharges`).

3.  **Production-Grade API (FastAPI)**:
    *   Consistent model loading with fallback logic.
    *   **Batch Prediction**: New `/api/predict` endpoint for CSV processing.
    *   **Single Prediction**: New `/api/predict/single` endpoint for real-time integration.
    *   **Simulated Projection**: Forward-looking 5-month risk trajectory simulation.
    *   **Health Checks**: Dedicated `/health` endpoint for monitoring.

4.  **Premium Institutional Dashboard (React + Vite)**:
    *   **Advanced Glassmorphism**: Stunning UI with backdrop blurs, rich gradients, and a dedicated sidebar navigation system.
    *   **Real-time Ingestion**: Drag-and-drop ingestion of CSV data sheets with instantaneous predictive scoring.
    *   **Scientific Visualizations**: Interactive Recharts integration for benchmarking, risk forecasting, and XAI feature drivers.
    *   **Adaptive Layout**: Fully responsive shell optimized for high-resolution enterprise monitoring.

5.  **DevOps & Reliability**:
    *   **Dockerization**: Multi-stage `Dockerfile` included for easy deployment.
    *   **Logging**: Centralized enterprise-grade logging across all modules.
    *   **Unit Testing**: Comprehensive test suite in `tests/` to verify pipeline integrity.

## 🛠️ How to Run

### Local Backend
1.  Install dependencies: `pip install -r requirements.txt`
2.  Train the model: `python training_pipeline.py`
3.  Start API: `python app.py`

### Docker Deployment
1.  Build: `docker build -t churn-ai .`
2.  Run: `docker run -p 8000:8000 churn-ai`

### Frontend Development
1.  `cd frontend`
2.  `npm install`
3.  `npm run dev`

## 📊 Evaluation
The current production model is based on an optimized **XGBoost** classifier, achieving approximately **0.84+ ROC-AUC** on the Telco Churn dataset.
