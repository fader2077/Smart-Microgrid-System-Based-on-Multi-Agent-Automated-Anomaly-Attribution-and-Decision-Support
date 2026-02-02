"""
Smart Grid Data Loading and Preprocessing Module
Phase 2: Data Loading and Preprocessing
"""

import pandas as pd
from datetime import datetime


def load_grid_data(csv_path: str) -> pd.DataFrame:
    """
    Load and preprocess the smart city energy dataset.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        Preprocessed pandas DataFrame with Timestamp index and Is_Anomaly column
    """
    print(f"Loading dataset from: {csv_path}")
    
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
    
    print("\n" + "="*60)
    print("DATA LOADING COMPLETE")
    print("="*60)
    print(f"\nTotal rows: {len(df)}")
    print(f"Date range: {df.index.min()} to {df.index.max()}")
    print(f"Anomalies detected: {df['Is_Anomaly'].sum()} ({df['Is_Anomaly'].sum()/len(df)*100:.2f}%)")
    
    print("\n" + "-"*60)
    print("First 5 rows:")
    print("-"*60)
    print(df.head())
    
    print("\n" + "-"*60)
    print("Data types:")
    print("-"*60)
    # Avoid printing dtypes to console due to Unicode issues in Windows
    # print(df.dtypes)
    print(f"Total columns: {len(df.columns)}")
    
    print("\n" + "-"*60)
    print("Key columns summary:")
    print("-"*60)
    key_columns = ['Grid Frequency (Hz)', 'Solar PV Output (kW)', 
                   'Wind Power Output (kW)', 'Cloud Cover (%)', 'Is_Anomaly']
    print(df[key_columns].describe())
    
    return df


def get_anomaly_timestamps(df: pd.DataFrame) -> list:
    """
    Get list of timestamps where anomalies occurred.
    
    Args:
        df: DataFrame with Is_Anomaly column
        
    Returns:
        List of timestamp strings
    """
    anomaly_df = df[df['Is_Anomaly'] == True]
    return [ts.strftime('%Y-%m-%d %H:%M:%S') for ts in anomaly_df.index]


if __name__ == "__main__":
    # Test the data loader
    csv_file = "smart_city_energy_dataset.csv"
    
    try:
        df = load_grid_data(csv_file)
        
        print("\n" + "="*60)
        print("ANOMALY ANALYSIS")
        print("="*60)
        
        anomaly_timestamps = get_anomaly_timestamps(df)
        print(f"\nFirst 10 anomaly timestamps:")
        for i, ts in enumerate(anomaly_timestamps[:10], 1):
            print(f"  {i}. {ts}")
            
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        print("Please make sure the CSV file is in the same directory.")
    except Exception as e:
        print(f"Error loading data: {e}")
