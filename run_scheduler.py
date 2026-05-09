"""
Scheduler script to update mutual fund data and rebuild vector store
Can be run locally or scheduled via cron/systemd
"""

import sys
from pathlib import Path
import logging
from datetime import datetime

# Add Docs/src to Python path
sys.path.insert(0, str(Path(__file__).parent / "Docs" / "src"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_data_update():
    """Run the data update pipeline."""
    logger.info("=" * 80)
    logger.info("Starting Data Update Scheduler")
    logger.info("=" * 80)
    
    try:
        # Import and run Phase 1 pipeline
        from phase1.pipeline import run_pipeline
        
        logger.info("Running data collection and processing pipeline...")
        run_pipeline(skip_scrape=False)  # Force fresh scrape
        
        logger.info("Data update completed successfully")
        return True
    except Exception as e:
        logger.error(f"Data update failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_vector_store_update():
    """Update the vector store with new data."""
    logger.info("Updating vector store...")
    
    try:
        from phase2.pipeline import initialize_vector_store
        
        # Re-initialize vector store to include new data
        initialize_vector_store()
        
        logger.info("Vector store updated successfully")
        return True
    except Exception as e:
        logger.error(f"Vector store update failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_tests():
    """Run tests to verify the update."""
    logger.info("Running verification tests...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, "test_phase1.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("Phase 1 tests passed")
            return True
        else:
            logger.error(f"Phase 1 tests failed: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Tests failed: {e}")
        return False

def main():
    """Main scheduler function."""
    start_time = datetime.now()
    
    logger.info(f"Scheduler started at {start_time}")
    
    # Step 1: Update data
    data_success = run_data_update()
    
    # Step 2: Update vector store
    if data_success:
        vector_success = run_vector_store_update()
    else:
        logger.error("Skipping vector store update due to data update failure")
        vector_success = False
    
    # Step 3: Run tests
    if vector_success:
        test_success = run_tests()
    else:
        logger.error("Skipping tests due to vector store update failure")
        test_success = False
    
    end_time = datetime.now()
    duration = end_time - start_time
    
    logger.info("=" * 80)
    logger.info(f"Scheduler completed at {end_time}")
    logger.info(f"Total duration: {duration}")
    logger.info(f"Data update: {'✓' if data_success else '✗'}")
    logger.info(f"Vector store update: {'✓' if vector_success else '✗'}")
    logger.info(f"Tests: {'✓' if test_success else '✗'}")
    logger.info("=" * 80)
    
    if data_success and vector_success and test_success:
        logger.info("All tasks completed successfully")
        return 0
    else:
        logger.error("Some tasks failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
