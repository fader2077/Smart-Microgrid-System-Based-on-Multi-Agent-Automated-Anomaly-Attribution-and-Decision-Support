"""
LangChain Ollama Agent Setup Module
Phase 3: Setting up Local Ollama Agent (The Core)
"""

from langchain_ollama import ChatOllama
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
import pandas as pd


def initialize_llm(model: str = "llama3:8b-instruct-q4_K_M", temperature: float = 0.0) -> ChatOllama:
    """
    Initialize the ChatOllama LLM for local inference.
    
    Args:
        model: Ollama model name (default: llama3:8b-instruct-q4_K_M)
        temperature: Temperature for generation (0 = deterministic, for precise data analysis)
        
    Returns:
        ChatOllama instance
    """
    print(f"Initializing LLM: {model} with temperature={temperature}")
    
    llm = ChatOllama(
        model=model,
        temperature=temperature,
    )
    
    print("[OK] LLM initialized successfully")
    return llm


def create_grid_agent(df: pd.DataFrame, llm: ChatOllama):
    """
    Create a Pandas DataFrame Agent specialized for grid operations.
    
    Args:
        df: Preprocessed grid data DataFrame
        llm: ChatOllama LLM instance
        
    Returns:
        Configured pandas dataframe agent
    """
    print("Creating Grid Operator Agent...")
    
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
    
    print("[OK] Grid Operator Agent created successfully")
    print(f"  - Agent type: Zero-Shot ReAct")
    print(f"  - Max iterations: 15")
    print(f"  - Dataset shape: {df.shape}")
    
    return agent


def create_smart_grid_agent(df: pd.DataFrame, model: str = "llama3:8b-instruct-q4_K_M") -> tuple:
    """
    Convenience function to initialize both LLM and Agent.
    
    Args:
        df: Preprocessed grid data DataFrame
        model: Ollama model name
        
    Returns:
        Tuple of (llm, agent)
    """
    print("\n" + "="*60)
    print("INITIALIZING SMART GRID AI OPERATOR")
    print("="*60)
    
    # Initialize LLM
    llm = initialize_llm(model=model, temperature=0.0)
    
    # Create agent
    agent = create_grid_agent(df, llm)
    
    print("\n" + "="*60)
    print("SYSTEM READY")
    print("="*60)
    
    return llm, agent


if __name__ == "__main__":
    print("This module provides LangChain Ollama agent setup.")
    print("Import and use create_smart_grid_agent(df) to initialize the system.")
    print("\nExample usage:")
    print("  from data_loader import load_grid_data")
    print("  from agent_setup import create_smart_grid_agent")
    print("  ")
    print("  df = load_grid_data('smart_city_energy_dataset.csv')")
    print("  llm, agent = create_smart_grid_agent(df)")
