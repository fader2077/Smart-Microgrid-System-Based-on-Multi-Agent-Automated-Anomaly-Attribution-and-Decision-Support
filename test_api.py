"""
Test script for FastAPI endpoints
"""
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Test all API endpoints"""
    print("="*60)
    print("FASTAPI ENDPOINT TESTING")
    print("="*60)
    
    # Give server time to start
    sleep(2)
    
    tests = [
        ("Health Check", "/api/health", {}),
        ("Grid Statistics", "/api/grid/statistics", {}),
        ("Latest Status", "/api/grid/status", {}),
        ("Anomaly List", "/api/grid/anomalies", {"limit": 3}),
        ("Specific Timestamp", "/api/grid/status/2021-01-01 01:30:00", {}),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, endpoint, params in tests:
        print(f"\n[TEST] {test_name}")
        print(f"       {endpoint}")
        
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ PASS - Status: {response.status_code}")
                print(f"   Response preview: {json.dumps(data, indent=2)[:200]}...")
                passed += 1
            else:
                print(f"❌ FAIL - Status: {response.status_code}")
                print(f"   Error: {response.text}")
                failed += 1
                
        except requests.exceptions.ConnectionError:
            print(f"❌ FAIL - Connection Error")
            print(f"   Server not running on {BASE_URL}")
            failed += 1
        except Exception as e:
            print(f"❌ FAIL - {type(e).__name__}: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    return passed, failed

if __name__ == "__main__":
    passed, failed = test_endpoints()
    exit(0 if failed == 0 else 1)
