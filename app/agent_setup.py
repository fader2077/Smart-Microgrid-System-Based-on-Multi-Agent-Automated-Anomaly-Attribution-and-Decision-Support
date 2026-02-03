"""
LangChain Ollama Agent Setup Module (Refactored for FastAPI/Chainlit)
Provides agent creation functions for the Smart Microgrid System
"""

from langchain_ollama import ChatOllama
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
import pandas as pd
from functools import lru_cache


def initialize_llm(model: str = "llama3:8b-instruct-q4_K_M", temperature: float = 0.0) -> ChatOllama:
    """
    Initialize the ChatOllama LLM for local inference.
    
    Args:
        model: Ollama model name (default: llama3:8b-instruct-q4_K_M)
        temperature: Temperature for generation (0 = deterministic)
        
    Returns:
        ChatOllama instance
    """
    print(f"[AGENT SETUP] Initializing LLM: {model} with temperature={temperature}")
    
    llm = ChatOllama(
        model=model,
        temperature=temperature,
    )
    
    print("[AGENT SETUP] LLM initialized successfully")
    return llm


def create_agent(df: pd.DataFrame, model: str = "llama3:8b-instruct-q4_K_M"):
    """
    Create a Pandas DataFrame Agent specialized for grid operations.
    
    Args:
        df: Preprocessed grid data DataFrame
        model: Ollama model name
        
    Returns:
        Configured pandas dataframe agent
    """
    print("[AGENT SETUP] Creating Grid Operator Agent...")
    
    # Initialize LLM
    llm = initialize_llm(model=model, temperature=0.0)
    
    # Get actual column names from the DataFrame
    column_list = '\n'.join([f"  - {col}" for col in df.columns])
    
    # Define the agent's role and context with explicit column names
    prefix = f"""
You are an expert grid operator analyzing smart city microgrid data.

Your primary responsibilities:
1. Analyze correlations between Grid Frequency drops and renewable generation changes
2. Investigate how weather conditions (Cloud Cover, Wind Speed) impact Solar/Wind generation
3. Identify curtailment risks and provide actionable recommendations
4. Calculate percentage changes and trends in the data

When analyzing anomalies:
- Look for patterns: Does falling Grid Frequency correlate with drops in Solar PV Output or Wind Power Output?
- Check weather: Did Cloud Cover increase? Did Wind Speed drop?
- Consider timing: Is this during peak demand hours?
- Assess risk: Is there a Curtailment Event Flag set?

Always provide:
1. Data-driven analysis with specific numbers
2. Root cause identification  
3. Short, actionable recommendations

CRITICAL: EXACT DataFrame column names (use these EXACTLY as shown):
{column_list}

IMPORTANT Instructions:
1. When filtering data, ALWAYS use df.loc[] with proper indexing
2. If specific rows are needed, filter the dataframe first using Python logic
3. The Timestamp is the INDEX - access it with df.index, not df['Timestamp']
4. When asked to analyze a specific timestamp:
   a) Show the exact values at that timestamp using df.loc[timestamp]
   b) Compare with 30 minutes prior
   c) Calculate percentage changes
   d) Explain causation based on weather and generation data
5. Output your analysis in structured format with clear sections
"""
    
    # Create the agent with dangerous code enabled (safe for local use)
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        allow_dangerous_code=True,
        prefix=prefix,
        max_iterations=10
    )
    
    print("[AGENT SETUP] Grid Operator Agent created successfully")
    print(f"  - Agent type: Zero-Shot ReAct")
    print(f"  - Max iterations: 10")
    print(f"  - Dataset shape: {df.shape}")
    
    return agent


# Cached version for Chainlit (avoid recreating agent on every message)
_cached_agent = None
_cached_df_id = None


def get_or_create_agent(df: pd.DataFrame, model: str = "llama3:8b-instruct-q4_K_M"):
    """
    Get cached agent or create new one if DataFrame changed.
    
    Args:
        df: Grid data DataFrame
        model: Ollama model name
        
    Returns:
        Cached or new agent instance
    """
    global _cached_agent, _cached_df_id
    
    # Use id(df) to check if it's the same DataFrame object
    current_df_id = id(df)
    
    if _cached_agent is None or _cached_df_id != current_df_id:
        print("[AGENT SETUP] Creating new agent (cache miss or DataFrame changed)")
        _cached_agent = create_agent(df, model)
        _cached_df_id = current_df_id
    else:
        print("[AGENT SETUP] Using cached agent")
    
    return _cached_agent


if __name__ == "__main__":
    print("This module provides LangChain Ollama agent setup.")
    print("Import and use create_agent(df) to initialize the system.")
    print("\nExample usage:")
    print("  from app.data_loader import load_data")
    print("  from app.agent_setup import create_agent")
    print("  ")
    print("  df = load_data('data/smart_city_energy_dataset.csv')")
    print("  agent = create_agent(df)")
