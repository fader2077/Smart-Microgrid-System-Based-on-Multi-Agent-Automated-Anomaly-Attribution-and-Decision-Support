"""
Quick Test Script - Verify System Components
Run this to test the full pipeline before using the Streamlit UI
"""

from data_loader import load_grid_data, get_anomaly_timestamps
from agent_setup import create_smart_grid_agent
from main_analysis import analyze_grid_event
import sys


def main():
    print("="*70)
    print("SMART GRID AI OPERATOR - SYSTEM TEST")
    print("="*70)
    
    # Step 1: Load Data
    print("\n[1/4] Loading dataset...")
    try:
        df = load_grid_data('smart_city_energy_dataset.csv')
        print("[OK] Data loaded successfully")
    except Exception as e:
        print(f"[FAIL] Error loading data: {e}")
        return False
    
    # Step 2: Get anomaly timestamps
    print("\n[2/4] Identifying anomalies...")
    try:
        anomaly_timestamps = get_anomaly_timestamps(df)
        if len(anomaly_timestamps) == 0:
            print("[FAIL] No anomalies found in dataset")
            return False
        print(f"[OK] Found {len(anomaly_timestamps)} anomalies")
        print(f"   First anomaly: {anomaly_timestamps[0]}")
    except Exception as e:
        print(f"[FAIL] Error finding anomalies: {e}")
        return False
    
    # Step 3: Initialize AI Agent
    print("\n[3/4] Initializing AI Agent (this may take a moment)...")
    print("   Note: Make sure Ollama is running with 'ollama serve'")
    try:
        llm, agent = create_smart_grid_agent(df)
        print("[OK] AI Agent initialized successfully")
    except Exception as e:
        print(f"[FAIL] Error initializing agent: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure Ollama is installed and running")
        print("  2. Run: ollama serve")
        print("  3. Run: ollama pull llama3.1")
        return False
    
    # Step 4: Test Analysis
    print("\n[4/4] Running test analysis on first anomaly...")
    print("   This will take 30-60 seconds...")
    try:
        target_timestamp = anomaly_timestamps[0]
        result = analyze_grid_event(target_timestamp, df, agent)
        
        if result['status'] == 'anomaly':
            print("[OK] Analysis completed successfully!")
            print("\n" + "="*70)
            print("SAMPLE ANALYSIS RESULT")
            print("="*70)
            print(f"Timestamp: {result['timestamp']}")
            print(f"Grid Frequency: {result['grid_frequency']:.4f} Hz")
            if result['analysis']:
                analysis_preview = str(result['analysis'])[:500]
                print(f"\nAI Analysis:\n{analysis_preview}...")
            
        else:
            print(f"[FAIL] Unexpected result status: {result['status']}")
            return False
            
    except Exception as e:
        print(f"[FAIL] Error during analysis: {e}")
        return False
    
    # Success!
    print("\n" + "="*70)
    print("[OK] ALL TESTS PASSED - SYSTEM READY!")
    print("="*70)
    print("\nYou can now run the Streamlit UI:")
    print("  streamlit run app.py")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
