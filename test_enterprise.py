"""
Test Script for Enterprise Architecture
Validates all components before running the full system
"""

import sys
import os

print("="*60)
print("SMART MICROGRID SYSTEM - COMPONENT TEST")
print("="*60)

# Test 1: Data Loader
print("\n[1/4] Testing Data Loader...")
try:
    from app.data_loader import load_data, get_statistics, get_latest_status
    
    # Try to load data
    data_file = "data/smart_city_energy_dataset.csv"
    if not os.path.exists(data_file):
        data_file = "smart_city_energy_dataset.csv"
    
    df = load_data(data_file)
    stats = get_statistics(df)
    latest = get_latest_status(df)
    
    print(f"✅ Data Loader OK")
    print(f"   - Records: {stats['total_records']}")
    print(f"   - Anomalies: {stats['anomalies']['count']}")
    print(f"   - Latest frequency: {latest['grid_frequency']:.4f} Hz")
    
except Exception as e:
    print(f"❌ Data Loader FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Agent Setup
print("\n[2/4] Testing Agent Setup...")
try:
    from app.agent_setup import create_agent
    
    agent = create_agent(df)
    print(f"✅ Agent Setup OK")
    print(f"   - Agent type: {type(agent).__name__}")
    
except Exception as e:
    print(f"❌ Agent Setup FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: FastAPI Server (import only)
print("\n[3/4] Testing FastAPI Server Import...")
try:
    from app.server import app
    print(f"✅ FastAPI Server OK")
    print(f"   - App title: {app.title}")
    print(f"   - Version: {app.version}")
    
except Exception as e:
    print(f"❌ FastAPI Server FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Chainlit App (import only - can't run without event loop)
print("\n[4/4] Testing Chainlit App Import...")
try:
    import app.chainlit_app
    print(f"✅ Chainlit App OK")
    
except Exception as e:
    print(f"❌ Chainlit App FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("ALL TESTS PASSED!")
print("="*60)
print("\n🚀 Ready to launch:")
print("   python app/server.py")
print("   or")
print("   uvicorn app.server:app --reload")
print("\n📚 API Documentation: http://localhost:8000/docs")
print("💬 Chat Interface: http://localhost:8000/chat")
print("="*60)
