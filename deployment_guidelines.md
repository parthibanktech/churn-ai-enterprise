# 🚀 Deployment Guidelines for ChurnAI

This document provides a step-by-step guide to deploying the **ChurnAI Enterprise Platform** to **Render** with a fully automated **CI/CD pipeline**.

---

## 🏗️ 1. Architecture Overview
- **Backend**: FastAPI (Python 3.11)
- **Frontend**: React + Vite (Node.js 20)
- **Containerization**: Multi-stage `Dockerfile`
- **Orchestration**: `render.yaml` (Blueprint)
- **CI/CD**: GitHub Actions (`.github/workflows/pipeline.yml`)

---

## 📦 2. Deployment to Render (The "Blueprint" Way)

The easiest way to deploy is using the `render.yaml` file included in this repository.

### Step 1: Connect GitHub to Render
1. Log in to your [Render Dashboard](https://dashboard.render.com/).
2. Click **"New +"** and select **"Blueprint"**.
3. Connect your GitHub repository.
4. Render will automatically detect `render.yaml` and prompt you to create the resources.

### Step 2: Manual Web Service (Alternative)
If you prefer not to use Blueprints:
1. Click **"New +"** -> **"Web Service"**.
2. Select your repository.
3. **Runtime**: `Docker`.
4. **Plan**: `Free` or `Starter`.
5. Under **Advanced**, add the Environment Variable:
   - `PORT`: `8080`

---

## 🔄 3. Setting up CI/CD (GitHub Actions)

The repository is configured to run tests and build the frontend on every push. To enable **Auto-Deployment** to Render after tests pass:

1. Go to your **Render Web Service Dashboard**.
2. Find the **"Deploy Hook"** URL (it looks like `https://api.render.com/deploy/srv-...`).
3. Go to your **GitHub Repository Settings**.
4. Navigate to **Secrets and variables** -> **Actions**.
5. Click **"New repository secret"**.
6. Name: `RENDER_DEPLOY_HOOK_URL`
7. Value: *Paste your Render Deploy Hook URL*.

Now, every time you push to the `main` branch, GitHub will:
1. Run Backend Tests.
2. Build the Frontend.
3. If both pass, trigger Render to pull the latest code and deploy.

---

## 🛠️ 4. Local Verification
Before pushing, ensure everything works locally:

```bash
# Build the Docker image
docker build -t churn-ai .

# Run the container
docker run -p 8080:8080 churn-ai
```
Visit `http://localhost:8080` to see the app.

---

## 🧪 5. Post-Deployment Checklist
- [ ] Check Render logs to ensure the server started successfully.
- [ ] Verify the `/api/stats` endpoint returns model metrics.
- [ ] Upload the sample file `data/raw/Telco-Customer-Churn.csv` to test the prediction engine.
- [ ] Ensure the "Algorithm Benchmark" tab displays the performance report.

---

## ⚠️ Troubleshooting
- **Model not found**: Ensure `training_pipeline.py` has been run at least once to generate `models/production_pipeline_bundle.joblib`. Docker builds include the current `models/` folder.
- **Port issue**: Render assigns a dynamic port. The Dockerfile is configured to use the `$PORT` environment variable provided by Render.
- **Frontend not loading**: Check if `frontend/dist` exists in the Docker image. The multi-stage build handles this automatically.

---
*Created by Antigravity AI*
