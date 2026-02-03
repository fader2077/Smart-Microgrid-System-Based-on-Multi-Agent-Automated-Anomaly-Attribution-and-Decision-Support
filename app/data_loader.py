"""
Smart Grid Data Loading Module (Refactored for FastAPI/Chainlit)
Provides cached data loading functions for the Smart Microgrid System
"""

import pandas as pd
from functools import lru_cache
from datetime import datetime
from typing import Optional


@lru_cache(maxsize=1)
def load_data(csv_path: str) -> pd.DataFrame:
    """
    Load and preprocess the smart city energy dataset with caching.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        Preprocessed pandas DataFrame with Timestamp index and anomaly detection
        
    Note:
        Uses @lru_cache to avoid reloading the same file multiple times.
        Cache size is 1 since we typically only load one dataset.
    """
    print(f"[DATA LOADER] Loading dataset from: {csv_path}")
    
    # Load the CSV file
    df = pd.read_csv(csv_path)
    
    # Parse Timestamp column to datetime objects
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Set Timestamp as index
    df.set_index('Timestamp', inplace=True)
    
    # Force numeric type conversion for critical columns
    numeric_cols = [
        'Grid Frequency (Hz)', 'Solar PV Output (kW)', 'Wind Power Output (kW)',
        'Cloud Cover (%)', 'Wind Speed (m/s)', 'Temperature (C)', 'Humidity (%)'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop rows with NaN in critical columns
    critical_cols = ['Grid Frequency (Hz)']
    df = df.dropna(subset=critical_cols)
    
    # Dynamic Anomaly Detection using Z-Score (Statistical Process Control)
    # This is more sophisticated than fixed thresholds
    window = 60  # 30 hours (assuming 30-min intervals)
    rolling_mean = df['Grid Frequency (Hz)'].rolling(window=window, min_periods=1).mean()
    rolling_std = df['Grid Frequency (Hz)'].rolling(window=window, min_periods=1).std()
    
    # Z-Score calculation: deviation from rolling mean in units of standard deviation
    z_score = (df['Grid Frequency (Hz)'] - rolling_mean) / rolling_std
    
    # Define anomaly: |Z-Score| > 3 OR frequency < 49.8 Hz (hybrid approach)
    df['Is_Anomaly'] = (z_score.abs() > 3) | (df['Grid Frequency (Hz)'] < 49.8)
    df['Z_Score'] = z_score  # Store for analysis
    
    # Sort dataframe by Timestamp
    df.sort_index(inplace=True)
    
    print(f"[DATA LOADER] Dataset loaded successfully")
    print(f"  - Total rows: {len(df)}")
    print(f"  - Date range: {df.index.min()} to {df.index.max()}")
    print(f"  - Anomalies: {df['Is_Anomaly'].sum()} ({df['Is_Anomaly'].sum()/len(df)*100:.2f}%)")
    print(f"  - Total columns: {len(df.columns)}")
    
    return df


def get_anomaly_timestamps(df: pd.DataFrame, limit: Optional[int] = None) -> list:
    """
    Get list of timestamps where anomalies occurred.
    
    Args:
        df: DataFrame with Is_Anomaly column
        limit: Optional limit on number of results
        
    Returns:
        List of timestamp strings
    """
    anomaly_df = df[df['Is_Anomaly'] == True]
    if limit:
        anomaly_df = anomaly_df.head(limit)
    return [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in anomaly_df.index]


def get_latest_status(df: pd.DataFrame) -> dict:
    """
    Get the most recent grid status.
    
    Args:
        df: Grid data DataFrame
        
    Returns:
        Dictionary with latest status metrics
    """
    latest = df.iloc[-1]
    return {
        "timestamp": latest.name.strftime('%Y-%m-%d %H:%M:%S'),
        "grid_frequency": float(latest['Grid Frequency (Hz)']),
        "solar_output": float(latest['Solar PV Output (kW)']),
        "wind_output": float(latest['Wind Power Output (kW)']),
        "is_anomaly": bool(latest['Is_Anomaly']),
        "z_score": float(latest['Z_Score']) if pd.notna(latest['Z_Score']) else None
    }


def get_statistics(df: pd.DataFrame) -> dict:
    """
    Calculate key statistics for the dataset.
    
    Args:
        df: Grid data DataFrame
        
    Returns:
        Dictionary with statistical metrics
    """
    return {
        "total_records": len(df),
        "date_range": {
            "start": df.index.min().strftime('%Y-%m-%d %H:%M:%S'),
            "end": df.index.max().strftime('%Y-%m-%d %H:%M:%S')
        },
        "anomalies": {
            "count": int(df['Is_Anomaly'].sum()),
            "percentage": float(df['Is_Anomaly'].sum() / len(df) * 100)
        },
        "avg_frequency": float(df['Grid Frequency (Hz)'].mean()),
        "avg_solar": float(df['Solar PV Output (kW)'].mean()),
        "avg_wind": float(df['Wind Power Output (kW)'].mean())
    }


if __name__ == "__main__":
    # Test the data loader
    import sys
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "data/smart_city_energy_dataset.csv"
    
    try:
        df = load_data(csv_file)
        
        print("\n" + "="*60)
        print("DATA LOADER TEST RESULTS")
        print("="*60)
        
        stats = get_statistics(df)
        print(f"Total records: {stats['total_records']}")
        print(f"Anomalies: {stats['anomalies']['count']} ({stats['anomalies']['percentage']:.2f}%)")
        
        latest = get_latest_status(df)
        print(f"\nLatest status:")
        print(f"  Timestamp: {latest['timestamp']}")
        print(f"  Frequency: {latest['grid_frequency']:.4f} Hz")
        print(f"  Is Anomaly: {latest['is_anomaly']}")
        
        print("\n✅ Data loader test passed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
