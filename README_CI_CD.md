# ChurnAI CI/CD & Deployment Guide

This project is now equipped with a professional CI/CD pipeline and a production-ready Docker configuration.

## 🚀 1. GitHub CI/CD Pipeline
The `.github/workflows/pipeline.yml` file is configured to:
1.  **Backend CI**: Install Python dependencies and run `pytest` on the `tests/` directory.
2.  **Frontend CI**: Install Node.js dependencies and run `npm run build` to verify the frontend.
3.  **CD (Deployment)**: A placeholder step for auto-deployment to Render/Railway.

### Setting up Auto-Deployment (e.g., Render)
1.  Connect your GitHub repository to **Render**.
2.  In Render, create a new **Web Service**.
3.  Use the `Dockerfile` for the build.
4.  Set the following environment variable in Render:
    *   `PORT`: `8080` (or leave as default if Render provides it).

## 🐳 2. Docker Production Build
The `Dockerfile` has been upgraded to a **Multi-Stage Build**:
*   **Stage 1**: Builds the React frontend using Node.js.
*   **Stage 2**: Sets up the Python environment, copies the backend code, and copies the compiled frontend `dist` from Stage 1.
*   **Serving**: In production, the FastAPI backend serves the frontend static files directly from `/`, while the API remains under `/api`.

To test locally with Docker:
```bash
docker build -t churnai .
docker run -p 8080:8080 churnai
```

## 📂 3. Repository Preparation
I have initialized a `.gitignore` and prepared a GitHub Actions workflow. 

### How to push to GitHub:
1.  Create a new repository on GitHub.
2.  Open your terminal in this folder and run:
    ```bash
    git remote add origin YOUR_GITHUB_REPO_URL
    git branch -M main
    git push -u origin main
    ```

---

