"""
Run script for Phase 4 UI (Streamlit)
Sets up the correct Python path and starts the Streamlit server
"""

import sys
from pathlib import Path

# Add Docs/src to Python path
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

import subprocess

if __name__ == "__main__":
    app_path = Path(__file__).parent / "Docs" / "src" / "phase4" / "app.py"
    
    print("=" * 80)
    print("Starting RAG Mutual Fund FAQ Assistant UI")
    print("=" * 80)
    print(f"App path: {app_path}")
    print("=" * 80)
    print()
    
    # Run streamlit with the app
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", str(app_path),
        "--server.headless", "false",
        "--server.port", "8501"
    ])
