"""
Main Analysis Logic Module
Phase 4: Defining Monitoring and Trigger Logic
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


def analyze_grid_event(
    target_timestamp: str,
    df: pd.DataFrame,
    agent
) -> Dict[str, Any]:
    """
    Analyze a grid event at a specific timestamp.
    
    Main control function that:
    1. Checks if an anomaly exists at the target timestamp
    2. If no anomaly, returns "System Normal"
    3. If anomaly detected, triggers the Agent for deep analysis
    
    Args:
        target_timestamp: Timestamp string (e.g., "2025-01-15 14:30:00")
        df: Grid data DataFrame with Is_Anomaly column
        agent: LangChain pandas dataframe agent
        
    Returns:
        Dictionary with analysis results
    """
    print("\n" + "="*60)
    print(f"ANALYZING GRID EVENT AT: {target_timestamp}")
    print("="*60)
    
    # Convert string timestamp to datetime
    try:
        target_dt = pd.to_datetime(target_timestamp)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Invalid timestamp format: {e}",
            "timestamp": target_timestamp
        }
    
    # Check if timestamp exists in dataframe
    if target_dt not in df.index:
        return {
            "status": "error",
            "message": f"Timestamp {target_timestamp} not found in dataset",
            "timestamp": target_timestamp
        }
    
    # Get the row at target timestamp
    row = df.loc[target_dt]
    
    print(f"\nChecking anomaly status...")
    print(f"  Grid Frequency: {row['Grid Frequency (Hz)']:.4f} Hz")
    print(f"  Is_Anomaly: {row['Is_Anomaly']}")
    
    # Check if anomaly exists
    if not row['Is_Anomaly']:
        print("\n[OK] System Normal - No anomaly detected")
        return {
            "status": "normal",
            "message": "System Normal",
            "timestamp": target_timestamp,
            "grid_frequency": row['Grid Frequency (Hz)'],
            "analysis": None
        }
    
    # Anomaly detected - trigger Agent analysis
    print("\n[WARNING] ANOMALY DETECTED - Triggering AI Agent Analysis...")
    
    # Calculate timestamp 30 minutes prior
    prior_dt = target_dt - timedelta(minutes=30)
    prior_timestamp = prior_dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Construct detailed prompt for the agent - simplified version for better compatibility
    # Get the actual data first
    prior_row = df.loc[prior_dt] if prior_dt in df.index else None
    current_row = df.loc[target_dt]
    
    if prior_row is not None:
        # Calculate changes manually
        freq_change = current_row['Grid Frequency (Hz)'] - prior_row['Grid Frequency (Hz)']
        solar_change_pct = ((current_row['Solar PV Output (kW)'] - prior_row['Solar PV Output (kW)']) / prior_row['Solar PV Output (kW)'] * 100) if prior_row['Solar PV Output (kW)'] > 0 else 0
        wind_change_pct = ((current_row['Wind Power Output (kW)'] - prior_row['Wind Power Output (kW)']) / prior_row['Wind Power Output (kW)'] * 100) if prior_row['Wind Power Output (kW)'] > 0 else 0
        cloud_change = current_row['Cloud Cover (%)'] - prior_row['Cloud Cover (%)']
        
        # Calculate confidence score based on data quality and correlation strength
        confidence = 100
        if abs(freq_change) < 0.1:
            confidence -= 20  # Small frequency change reduces confidence
        if abs(solar_change_pct) > 50 or abs(wind_change_pct) > 50:
            confidence -= 10  # Extreme changes may indicate data quality issues
        
        # Determine primary root cause
        root_cause = "Unknown"
        if solar_change_pct < -10 and cloud_change > 10:
            root_cause = "Weather Impact: Cloud cover increase caused solar generation drop"
            confidence += 15  # Strong correlation increases confidence
        elif solar_change_pct < -10:
            root_cause = "Solar Generation Drop: Significant decrease in solar output"
        elif wind_change_pct < -10:
            root_cause = "Wind Generation Drop: Significant decrease in wind power"
        elif abs(solar_change_pct) > 10 or abs(wind_change_pct) > 10:
            root_cause = "Renewable Generation Loss: Combined renewable capacity reduction"
        
        confidence = min(100, max(0, confidence))  # Clamp between 0-100
        
        # Generate recommendations based on severity
        recommendations = []
        if abs(freq_change) > 0.2:
            recommendations.append("URGENT: Activate backup power sources immediately")
        else:
            recommendations.append("Monitor situation closely")
        
        if cloud_change > 10:
            recommendations.append("Weather-related: Monitor forecasts for recovery timeline")
        
        if current_row['Grid Frequency (Hz)'] < 49.5:
            recommendations.append("CRITICAL: Consider load shedding to stabilize frequency")
        
        # Create structured JSON output
        analysis_json = {
            "root_cause": root_cause,
            "confidence_score": confidence,
            "recommendations": recommendations,
            "metrics": {
                "frequency_change_hz": round(freq_change, 4),
                "solar_change_percent": round(solar_change_pct, 2),
                "wind_change_percent": round(wind_change_pct, 2),
                "cloud_cover_change": round(cloud_change, 2)
            }
        }
        
        # Create formatted text output (backward compatible)
        agent_output = f"""
--- DATA COMPARISON ---
Time: {prior_timestamp} -> {target_timestamp}

Grid Frequency: {prior_row['Grid Frequency (Hz)']:.2f} Hz -> {current_row['Grid Frequency (Hz)']:.2f} Hz (Change: {freq_change:.2f} Hz)
Solar PV Output: {prior_row['Solar PV Output (kW)']:.2f} kW -> {current_row['Solar PV Output (kW)']:.2f} kW (Change: {solar_change_pct:.1f}%)
Wind Power Output: {prior_row['Wind Power Output (kW)']:.2f} kW -> {current_row['Wind Power Output (kW)']:.2f} kW (Change: {wind_change_pct:.1f}%)
Cloud Cover: {prior_row['Cloud Cover (%)']:.1f}% -> {current_row['Cloud Cover (%)']:.1f}% (Change: {cloud_change:.1f}%)

--- ROOT CAUSE ANALYSIS ---
**{root_cause}** (Confidence: {confidence}%)

The grid frequency dropped by {abs(freq_change):.2f} Hz. """
        
        if solar_change_pct < -10 and cloud_change > 10:
            agent_output += f"Solar generation decreased by {abs(solar_change_pct):.1f}% due to {cloud_change:.1f}% increase in cloud cover. "
        elif solar_change_pct < -10:
            agent_output += f"Solar generation dropped significantly ({abs(solar_change_pct):.1f}%). "
        
        if wind_change_pct < -10:
            agent_output += f"Wind power also decreased by {abs(wind_change_pct):.1f}%. "
        
        if abs(solar_change_pct) > 10 or abs(wind_change_pct) > 10:
            agent_output += "The loss of renewable generation capacity is the primary cause of frequency instability."
        
        agent_output += f"""

--- RECOMMENDATIONS ---
"""
        for i, rec in enumerate(recommendations, 1):
            agent_output += f"{i}. {rec}\n"
        
    else:
        analysis_json = {
            "root_cause": "Insufficient data",
            "confidence_score": 0,
            "recommendations": ["Collect more historical data"],
            "metrics": {}
        }
        agent_output = f"Unable to retrieve comparison data for {prior_timestamp}. Analysis limited to current state only."
    
    print("\n" + "-"*60)
    print("ANALYSIS COMPLETE")
    print("-"*60)
    
    return {
        "status": "anomaly",
        "message": "Anomaly detected and analyzed",
        "timestamp": target_timestamp,
        "grid_frequency": row['Grid Frequency (Hz)'],
        "solar_output": row['Solar PV Output (kW)'],
        "wind_output": row['Wind Power Output (kW)'],
        "cloud_cover": row['Cloud Cover (%)'],
        "analysis": agent_output,
        "structured_analysis": analysis_json,  # NEW: JSON structured output
        "raw_data": row.to_dict()
    }



def get_event_context(
    target_timestamp: str,
    df: pd.DataFrame,
    hours_before: int = 1,
    hours_after: int = 1
) -> pd.DataFrame:
    """
    Get surrounding context for a grid event.
    
    Args:
        target_timestamp: Target timestamp string
        df: Grid data DataFrame
        hours_before: Hours of data before the event
        hours_after: Hours of data after the event
        
    Returns:
        DataFrame with surrounding context
    """
    target_dt = pd.to_datetime(target_timestamp)
    start_dt = target_dt - timedelta(hours=hours_before)
    end_dt = target_dt + timedelta(hours=hours_after)
    
    context_df = df.loc[start_dt:end_dt].copy()
    return context_df


if __name__ == "__main__":
    print("This module provides the main analysis logic.")
    print("Use analyze_grid_event(timestamp, df, agent) to investigate anomalies.")
    print("\nExample usage:")
    print("  from data_loader import load_grid_data")
    print("  from agent_setup import create_smart_grid_agent")
    print("  from main_analysis import analyze_grid_event")
    print("  ")
    print("  df = load_grid_data('smart_city_energy_dataset.csv')")
    print("  llm, agent = create_smart_grid_agent(df)")
    print("  result = analyze_grid_event('2025-01-15 14:30:00', df, agent)")
    print("  print(result)")
