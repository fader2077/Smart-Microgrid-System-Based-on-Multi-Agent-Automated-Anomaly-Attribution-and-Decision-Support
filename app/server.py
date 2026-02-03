"""
FastAPI Server - Smart Microgrid AI System
Main entry point for the enterprise-grade backend service

This server provides:
1. REST API endpoints for grid data access
2. Chainlit AI chat interface mounted at /chat
3. Automatic API documentation at /docs
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from chainlit.utils import mount_chainlit
import pandas as pd
from datetime import datetime
from typing import Optional, List
import os

from app.data_loader import load_data, get_anomaly_timestamps, get_latest_status, get_statistics

# Initialize FastAPI application
app = FastAPI(
    title="Smart Microgrid AI System",
    description="Enterprise-grade AI-powered microgrid monitoring and analysis system",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global DataFrame - loaded once at startup
df: Optional[pd.DataFrame] = None

# Determine data file path
DATA_FILE = os.path.join("data", "smart_city_energy_dataset.csv")
if not os.path.exists(DATA_FILE):
    # Fallback to root directory
    DATA_FILE = "smart_city_energy_dataset.csv"


@app.on_event("startup")
async def startup_event():
    """Load data on server startup"""
    global df
    try:
        print("\n" + "="*60)
        print("SMART MICROGRID AI SYSTEM - STARTUP")
        print("="*60)
        df = load_data(DATA_FILE)
        print("✅ Data loaded successfully")
        print("✅ FastAPI server ready")
        print("="*60 + "\n")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        raise


@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "name": "Smart Microgrid AI System",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "api_docs": "/docs",
            "chat_interface": "/chat",
            "grid_status": "/api/grid/status",
            "anomalies": "/api/grid/anomalies",
            "statistics": "/api/grid/statistics"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    if df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    return {
        "status": "healthy",
        "data_loaded": True,
        "records": len(df),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/grid/statistics")
async def get_grid_statistics():
    """
    Get overall grid statistics
    
    Returns:
        Statistical summary of the grid data
    """
    if df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    return get_statistics(df)


@app.get("/api/grid/status")
async def get_current_status():
    """
    Get the most recent grid status
    
    Returns:
        Latest grid metrics
    """
    if df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    return get_latest_status(df)


@app.get("/api/grid/status/{timestamp}")
async def get_grid_status_at_time(timestamp: str):
    """
    Get grid status at a specific timestamp
    
    Args:
        timestamp: ISO format timestamp (e.g., "2021-01-01 00:00:00")
    
    Returns:
        Grid data at specified timestamp
    """
    if df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    try:
        # Parse timestamp
        ts = pd.to_datetime(timestamp)
        
        # Get row at timestamp
        if ts not in df.index:
            raise HTTPException(status_code=404, detail=f"Timestamp {timestamp} not found in dataset")
        
        row = df.loc[ts]
        
        # Convert to dictionary
        result = row.to_dict()
        result['timestamp'] = ts.strftime('%Y-%m-%d %H:%M:%S')
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid timestamp format: {e}")
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Timestamp {timestamp} not found")


@app.get("/api/grid/anomalies")
async def get_anomalies(limit: int = 10, offset: int = 0):
    """
    Get list of anomaly events
    
    Args:
        limit: Maximum number of results (default: 10, max: 100)
        offset: Number of results to skip (default: 0)
    
    Returns:
        List of anomaly events with timestamps
    """
    if df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    # Validate parameters
    if limit > 100:
        limit = 100
    if limit < 1:
        limit = 10
    if offset < 0:
        offset = 0
    
    # Get anomalies
    anomaly_df = df[df['Is_Anomaly'] == True]
    total_anomalies = len(anomaly_df)
    
    # Apply pagination
    anomaly_df = anomaly_df.iloc[offset:offset+limit]
    
    # Convert to list of dictionaries
    results = []
    for ts, row in anomaly_df.iterrows():
        results.append({
            "timestamp": ts.strftime('%Y-%m-%d %H:%M:%S'),
            "grid_frequency": float(row['Grid Frequency (Hz)']),
            "solar_output": float(row['Solar PV Output (kW)']),
            "wind_output": float(row['Wind Power Output (kW)']),
            "z_score": float(row['Z_Score']) if pd.notna(row['Z_Score']) else None
        })
    
    return {
        "total": total_anomalies,
        "limit": limit,
        "offset": offset,
        "results": results
    }


@app.get("/api/grid/range")
async def get_grid_data_range(start: str, end: str):
    """
    Get grid data for a time range
    
    Args:
        start: Start timestamp (ISO format)
        end: End timestamp (ISO format)
    
    Returns:
        Grid data within the specified range
    """
    if df is None:
        raise HTTPException(status_code=503, detail="Data not loaded")
    
    try:
        start_ts = pd.to_datetime(start)
        end_ts = pd.to_datetime(end)
        
        # Validate range
        if start_ts > end_ts:
            raise HTTPException(status_code=400, detail="Start time must be before end time")
        
        # Extract data
        range_df = df.loc[start_ts:end_ts]
        
        if len(range_df) == 0:
            raise HTTPException(status_code=404, detail="No data found in specified range")
        
        # Convert to records format
        results = []
        for ts, row in range_df.iterrows():
            record = row.to_dict()
            record['timestamp'] = ts.strftime('%Y-%m-%d %H:%M:%S')
            results.append(record)
        
        return {
            "start": start,
            "end": end,
            "count": len(results),
            "data": results
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid timestamp format: {e}")


# Mount Chainlit application
# This makes the AI chat interface available at /chat
print("Mounting Chainlit application at /chat")
mount_chainlit(app=app, target="app/chainlit_app.py", path="/chat")


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("STARTING SMART MICROGRID AI SYSTEM")
    print("="*60)
    print("FastAPI Server: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("AI Chat Interface: http://localhost:8000/chat")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
