# RAG Mutual Fund FAQ Assistant

A Retrieval-Augmented Generation (RAG) based chatbot for answering questions about mutual funds.

## Project Overview

This project is a 6-phase development of a RAG-based chatbot that answers mutual fund questions using:

- **Phase 1**: Data Collection & Processing
- **Phase 2**: RAG Pipeline (Embeddings & Vector Database)
- **Phase 3**: Backend API (FastAPI)
- **Phase 4**: Frontend UI (Streamlit)
- **Phase 5**: Testing & QA
- **Phase 6**: Deployment & Documentation

## Quick Start

### Local Development

1. Clone the repository:
```bash
git clone <repository-url>
cd RAG-MutualFund-ChatBot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp Docs/Deployment/6.4_environment_config/.env.example .env
# Edit .env with your GROQ_API_KEY
```

4. Run the backend API:
```bash
uvicorn Docs.src.phase3.api.main:app --reload --host 0.0.0.0 --port 8000
```

5. Run the frontend UI:
```bash
streamlit run Docs/src/phase4/app.py
```

## Deployment

### Railway (Recommended)

The easiest way to deploy this application is using Railway.

**Quick Setup:**
1. Push code to GitHub
2. Go to [railway.app](https://railway.app) and connect your repository
3. Railway will auto-detect the project structure
4. Configure environment variables (GROQ_API_KEY, etc.)
5. Deploy!

**Detailed Instructions:** See [Docs/Deployment/6.7_railway_deployment/README.md](Docs/Deployment/6.7_railway_deployment/README.md)

### Docker (Local Development)

```bash
cd Docs/Deployment/6.1_containerization
docker-compose up
```

### AWS ECS (Enterprise)

For enterprise deployments, see [Docs/Deployment/6.2_cloud_infrastructure/README.md](Docs/Deployment/6.2_cloud_infrastructure/README.md)

## Project Structure

```
RAG-MutualFund-ChatBot/
├── Docs/
│   ├── src/                    # Source code for all phases
│   │   ├── phase1/            # Data collection
│   │   ├── phase2/            # RAG pipeline
│   │   ├── phase3/            # Backend API
│   │   └── phase4/            # Frontend UI
│   ├── Deployment/            # Deployment configurations
│   │   ├── 6.1_containerization/
│   │   ├── 6.2_cloud_infrastructure/
│   │   ├── 6.3_cicd_pipeline/
│   │   ├── 6.4_environment_config/
│   │   ├── 6.5_documentation/
│   │   ├── 6.6_monitoring_maintenance/
│   │   └── 6.7_railway_deployment/
│   └── Phase*_*/               # Phase-specific documentation
├── Tests/                      # Test suites for each phase
├── data/                       # Data files (raw, processed, chunks)
├── chroma_db/                  # Vector database storage
├── railway.toml               # Railway configuration
├── Procfile                   # Railway process definitions
└── requirements.txt           # Python dependencies
```

## Environment Variables

Required environment variables:

- `GROQ_API_KEY`: Your Groq API key for LLM
- `CHROMA_PERSIST_DIR`: Path to ChromaDB storage
- `EMBEDDING_MODEL`: Model name for embeddings (default: BAAI/bge-small-en-v1.5)

See `.env.example` for complete list.

## Testing

Run tests for specific phases:
```bash
python Tests/Phase1/run_tests.py
python Tests/Phase2/run_tests.py
python Tests/Phase3/run_tests.py
python Tests/Phase5/run_tests.py
python Tests/Phase6/run_tests.py
```

## Documentation

- [Architecture](Docs/Architecture.md) - System architecture and design
- [Phase 1: Data Collection](Docs/Phase1_DataCollection/README.md)
- [Phase 2: RAG Pipeline](Docs/Phase2_RAGPipeline/README.md)
- [Phase 3: Backend API](Docs/Phase3_BackendAPI/README.md)
- [Phase 4: Frontend UI](Docs/Phase4_FrontendUI/README.md)
- [Phase 5: Testing & QA](Docs/Phase5_TestingQA/README.md)
- [Phase 6: Deployment](Docs/Phase6_Deployment/README.md)

## Technology Stack

- **Backend**: FastAPI, Python 3.11
- **Frontend**: Streamlit
- **Vector Database**: ChromaDB
- **Embeddings**: BAAI/bge-small-en-v1.5
- **LLM**: Groq API
- **Testing**: Pytest
- **Deployment**: Railway, Docker, AWS ECS

## License

[Your License Here]

## Contributing

[Contributing Guidelines Here]
