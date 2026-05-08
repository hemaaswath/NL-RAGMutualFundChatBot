"""
Run script for Phase 3 API
Sets up the correct Python path and starts the FastAPI server
"""

import sys
from pathlib import Path

# Add Docs/src to Python path
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

import uvicorn
from phase3.config import API_HOST, API_PORT

if __name__ == "__main__":
    print(f"Starting RAG Mutual Fund FAQ Assistant API on {API_HOST}:{API_PORT}")
    print(f"API Documentation: http://{API_HOST}:{API_PORT}/docs")
    print(f"Health Check: http://{API_HOST}:{API_PORT}/api/health")
    
    uvicorn.run(
        "phase3.api.main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    )
