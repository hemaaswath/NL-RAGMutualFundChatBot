# Procfile for Railway deployment
# This file defines the processes to run for your application

# Backend API service
backend: uvicorn Docs.src.phase3.api.main:app --host 0.0.0.0 --port $PORT

# Frontend UI service
frontend: streamlit run Docs/src/phase4/app.py --server.port=$PORT --server.address=0.0.0.0
