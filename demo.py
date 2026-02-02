"""
Simple Demo Script - Command Line Interface
Use this for quick testing without Streamlit
"""

from data_loader import load_grid_data, get_anomaly_timestamps
from agent_setup import create_smart_grid_agent
from main_analysis import analyze_grid_event, get_event_context
import sys


def print_header(text):
    """Print formatted header."""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")


def main():
    print_header("🔋 SMART GRID AI OPERATOR - DEMO MODE")
    
    # Load data
    print("Loading dataset...")
    df = load_grid_data('smart_city_energy_dataset.csv')
    
    # Get anomalies
    anomaly_timestamps = get_anomaly_timestamps(df)
    print(f"\nFound {len(anomaly_timestamps)} anomalies in the dataset")
    
    # Initialize agent
    print("\nInitializing AI Agent...")
    print("(Make sure Ollama is running: 'ollama serve')\n")
    
    try:
        llm, agent = create_smart_grid_agent(df)
    except Exception as e:
        print(f"\n❌ Error: Could not connect to Ollama")
        print(f"Details: {e}")
        print("\nPlease make sure:")
        print("  1. Ollama is installed (https://ollama.ai)")
        print("  2. Ollama server is running: ollama serve")
        print("  3. Llama 3.1 is installed: ollama pull llama3.1")
        sys.exit(1)
    
    # Interactive loop
    while True:
        print_header("SELECT AN ANOMALY TO ANALYZE")
        
        # Show first 20 anomalies
        print("Available anomaly timestamps (showing first 20):\n")
        for i, ts in enumerate(anomaly_timestamps[:20], 1):
            print(f"  {i:2d}. {ts}")
        
        print(f"\n  ... and {max(0, len(anomaly_timestamps)-20)} more")
        print("\nOptions:")
        print("  - Enter a number (1-20) to analyze that timestamp")
        print("  - Enter 'q' to quit")
        print("  - Enter 'list' to see more timestamps")
        
        choice = input("\nYour choice: ").strip().lower()
        
        if choice == 'q':
            print("\nThank you for using Smart Grid AI Operator! 👋")
            break
        
        elif choice == 'list':
            print("\nAll anomaly timestamps:\n")
            for i, ts in enumerate(anomaly_timestamps, 1):
                print(f"  {i:3d}. {ts}")
            input("\nPress Enter to continue...")
            continue
        
        else:
            try:
                index = int(choice) - 1
                if 0 <= index < len(anomaly_timestamps):
                    target_timestamp = anomaly_timestamps[index]
                    
                    print_header(f"ANALYZING: {target_timestamp}")
                    
                    # Get context
                    target_dt = df.index[df.index == target_timestamp][0]
                    row = df.loc[target_dt]
                    
                    # Show key metrics
                    print("📊 Key Metrics:")
                    print(f"  Grid Frequency: {row['Grid Frequency (Hz)']:.4f} Hz")
                    print(f"  Solar PV Output: {row['Solar PV Output (kW)']:.2f} kW")
                    print(f"  Wind Power Output: {row['Wind Power Output (kW)']:.2f} kW")
                    print(f"  Cloud Cover: {row['Cloud Cover (%)']:.1f}%")
                    print(f"  Wind Speed: {row['Wind Speed (m/s)']:.2f} m/s")
                    
                    # Run analysis
                    print("\n🤖 Running AI analysis (30-60 seconds)...\n")
                    
                    result = analyze_grid_event(target_timestamp, df, agent)
                    
                    if result['status'] == 'anomaly':
                        print_header("AI ANALYSIS RESULT")
                        print(result['analysis'])
                        print("\n" + "="*70)
                    else:
                        print(f"\nStatus: {result['status']}")
                        print(f"Message: {result['message']}")
                    
                    input("\nPress Enter to continue...")
                    
                else:
                    print(f"\n❌ Invalid number. Please enter 1-{min(20, len(anomaly_timestamps))}")
                    input("Press Enter to continue...")
                    
            except ValueError:
                print("\n❌ Invalid input. Please enter a number or 'q' to quit")
                input("Press Enter to continue...")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye! 👋")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        sys.exit(1)
