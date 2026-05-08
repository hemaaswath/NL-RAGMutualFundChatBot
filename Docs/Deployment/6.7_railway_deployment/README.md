# Railway Deployment Guide

This guide explains how to deploy the RAG Mutual Fund ChatBot to Railway.

## Prerequisites

- GitHub account
- Railway account (sign up at [railway.app](https://railway.app))
- Project code pushed to GitHub

## Deployment Steps

### 1. Prepare Your Repository

Ensure your code is pushed to GitHub:
```bash
git add .
git commit -m "Add Railway deployment configuration"
git push origin main
```

### 2. Connect Railway to GitHub

1. Go to [railway.app](https://railway.app) and log in
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will automatically detect the project structure

### 3. Configure Backend Service

1. Railway will create a service for your backend
2. Set the **Build Command**:
   ```
   pip install -r requirements.txt
   ```
3. Set the **Start Command**:
   ```
   uvicorn Docs.src.phase3.api.main:app --host 0.0.0.0 --port $PORT
   ```
4. Add Environment Variables:
   - `GROQ_API_KEY`: Your Groq API key
   - `CHROMA_PERSIST_DIR`: `./data/chroma`
   - `CHROMA_COLLECTION_NAME`: `mutual_fund_chunks`
   - `EMBEDDING_MODEL`: `BAAI/bge-small-en-v1.5`
   - `PYTHONPATH`: `/app`

### 4. Configure Frontend Service

1. Click "New Service" → "GitHub Repo"
2. Select the same repository
3. Set the **Build Command**:
   ```
   pip install -r requirements.txt
   ```
4. Set the **Start Command**:
   ```
   streamlit run Docs/src/phase4/app.py --server.port=$PORT --server.address=0.0.0.0
   ```
5. Add Environment Variables:
   - `PYTHONPATH`: `/app`
   - `BACKEND_URL`: Your backend service URL (from Railway)

### 5. Connect Services

1. Go to your backend service
2. Copy the backend URL (e.g., `https://your-backend.railway.app`)
3. Go to your frontend service
4. Add environment variable `BACKEND_URL` with the backend URL
5. Update the frontend code to use this environment variable

### 6. Deploy

1. Railway will automatically deploy on every push to GitHub
2. Monitor the deployment logs in the Railway dashboard
3. Once deployed, you'll get public URLs for both services

## Environment Variables Reference

### Backend Service
- `GROQ_API_KEY`: Required - Your Groq API key
- `CHROMA_PERSIST_DIR`: `./data/chroma`
- `CHROMA_COLLECTION_NAME`: `mutual_fund_chunks`
- `EMBEDDING_MODEL`: `BAAI/bge-small-en-v1.5`
- `CHUNK_SIZE`: `500`
- `CHUNK_OVERLAP`: `50`
- `MAX_RETRIEVED_CHUNKS`: `5`
- `SIMILARITY_THRESHOLD`: `0.7`
- `CACHE_ENABLED`: `true`
- `CACHE_TTL`: `3600`
- `LOG_LEVEL`: `INFO`
- `PYTHONPATH`: `/app`

### Frontend Service
- `BACKEND_URL`: Your backend service URL
- `PYTHONPATH`: `/app`
- `STREAMLIT_SERVER_PORT`: `$PORT`

## Database Setup

Railway provides managed PostgreSQL. If you want to use it instead of ChromaDB:

1. Add a PostgreSQL service in Railway
2. Update your code to use PostgreSQL instead of ChromaDB
3. Add `DATABASE_URL` environment variable to backend

## Monitoring

- View logs in Railway dashboard
- Monitor resource usage (CPU, memory)
- Set up alerts for errors
- Check deployment status

## Scaling

Railway automatically scales based on traffic:
- Free tier: 512MB RAM, 0.5 vCPU
- Paid plans: More resources available
- Configure scaling limits in service settings

## Troubleshooting

### Build Failures
- Check the build logs in Railway dashboard
- Ensure all dependencies are in requirements.txt
- Verify Python version compatibility (3.11)

### Runtime Errors
- Check runtime logs
- Verify all environment variables are set
- Ensure backend URL is correct in frontend

### Service Not Starting
- Check start command syntax
- Verify port configuration ($PORT variable)
- Review logs for specific error messages

### Database Connection Issues
- If using Railway PostgreSQL: Check DATABASE_URL
- If using ChromaDB: Ensure data directory exists and is writable

## Cost

- **Free Tier**: $5/month credit (good for development)
- **Paid Plans**: Start at $5/month per service
- Pay only for what you use (CPU, memory, storage)

## Alternative: Single Service Deployment

If you prefer a single service deployment:

1. Create one Railway service
2. Modify the start command to run both backend and frontend
3. Use a reverse proxy (nginx) to route traffic
4. This is more complex but cheaper

## Updating Deployment

To update your deployment:
```bash
git add .
git commit -m "Update application"
git push origin main
```
Railway will automatically redeploy.

## Rollback

If a deployment fails:
1. Go to Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Click "Rollback" on a previous successful deployment

## Support

- Railway Documentation: [docs.railway.app](https://docs.railway.app)
- Railway Discord: [discord.gg/railway](https://discord.gg/railway)
- GitHub Issues: Check repository issues
