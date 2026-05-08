"""
Health Check Script for Monitoring
Checks the health of backend and frontend services
"""

import requests
import sys
import time
from typing import Dict, List


def check_backend_health(url: str = "http://localhost:8000") -> Dict:
    """Check backend API health."""
    try:
        response = requests.get(f"{url}/api/health", timeout=5)
        if response.status_code == 200:
            return {
                "service": "backend",
                "status": "healthy",
                "response_time": response.elapsed.total_seconds(),
                "data": response.json()
            }
        else:
            return {
                "service": "backend",
                "status": "unhealthy",
                "status_code": response.status_code
            }
    except Exception as e:
        return {
            "service": "backend",
            "status": "error",
            "error": str(e)
        }


def check_frontend_health(url: str = "http://localhost:8501") -> Dict:
    """Check frontend UI health."""
    try:
        response = requests.get(f"{url}/_stcore/health", timeout=5)
        if response.status_code == 200:
            return {
                "service": "frontend",
                "status": "healthy",
                "response_time": response.elapsed.total_seconds()
            }
        else:
            return {
                "service": "frontend",
                "status": "unhealthy",
                "status_code": response.status_code
            }
    except Exception as e:
        return {
            "service": "frontend",
            "status": "error",
            "error": str(e)
        }


def run_health_checks(services: List[str] = None) -> List[Dict]:
    """Run health checks for all services."""
    if services is None:
        services = ["backend", "frontend"]
    
    results = []
    
    if "backend" in services:
        results.append(check_backend_health())
    
    if "frontend" in services:
        results.append(check_frontend_health())
    
    return results


def main():
    """Main health check function."""
    print("=" * 80)
    print("Health Check - RAG Mutual Fund FAQ Assistant")
    print("=" * 80)
    print()
    
    results = run_health_checks()
    
    all_healthy = True
    for result in results:
        service = result["service"]
        status = result["status"]
        
        if status == "healthy":
            print(f"✅ {service.upper()}: Healthy (Response time: {result['response_time']:.3f}s)")
        else:
            print(f"❌ {service.upper()}: {status}")
            if "error" in result:
                print(f"   Error: {result['error']}")
            all_healthy = False
    
    print()
    print("=" * 80)
    if all_healthy:
        print("All services are healthy!")
        return 0
    else:
        print("Some services are unhealthy!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
