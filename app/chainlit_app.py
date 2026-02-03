"""
Chainlit AI Chat Application - Smart Microgrid System
Provides interactive AI agent interface with Chain-of-Thought visualization

Features:
- Real-time agent conversation
- Plotly-based React visualizations
- Step-by-step reasoning display
- Grid status dashboard
"""

import chainlit as cl
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
import asyncio

from app.data_loader import load_data, get_latest_status, get_statistics
from app.agent_setup import create_agent, get_or_create_agent
import os

# Determine data file path
DATA_FILE = os.path.join("data", "smart_city_energy_dataset.csv")
if not os.path.exists(DATA_FILE):
    DATA_FILE = "smart_city_energy_dataset.csv"


def create_status_gauge(frequency: float, title: str = "Grid Frequency (Hz)") -> go.Figure:
    """
    Create a gauge chart for grid frequency status
    
    Args:
        frequency: Current frequency value
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    # Determine color based on frequency
    if frequency < 49.8:
        color = "red"
        status = "ANOMALY"
    elif frequency < 49.9:
        color = "orange"
        status = "WARNING"
    else:
        color = "green"
        status = "NORMAL"
    
    fig = go.Figure(go.Indicator(
        mode="number+gauge+delta",
        value=frequency,
        title={'text': f"{title}<br><span style='font-size:0.8em;color:{color}'>{status}</span>"},
        delta={'reference': 50.0, 'increasing': {'color': 'green'}, 'decreasing': {'color': 'red'}},
        gauge={
            'axis': {'range': [49.0, 51.0], 'tickwidth': 1},
            'bar': {'color': color, 'thickness': 0.75},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [49.0, 49.8], 'color': '#ffcccc'},
                {'range': [49.8, 49.9], 'color': '#ffffcc'},
                {'range': [49.9, 51.0], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 49.8
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig


def create_trend_chart(df: pd.DataFrame, hours: int = 24) -> go.Figure:
    """
    Create a trend chart for the last N hours
    
    Args:
        df: Grid data DataFrame
        hours: Number of hours to display
        
    Returns:
        Plotly figure object
    """
    # Get recent data
    end_time = df.index.max()
    start_time = end_time - timedelta(hours=hours)
    recent_df = df.loc[start_time:end_time]
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Grid Frequency (Hz)', 'Renewable Generation (kW)'),
        vertical_spacing=0.15,
        specs=[[{"secondary_y": False}],
               [{"secondary_y": True}]]
    )
    
    # Frequency plot
    fig.add_trace(
        go.Scatter(
            x=recent_df.index,
            y=recent_df['Grid Frequency (Hz)'],
            name='Frequency',
            line=dict(color='#3498db', width=2),
            mode='lines'
        ),
        row=1, col=1
    )
    
    # Anomaly markers
    anomaly_df = recent_df[recent_df['Is_Anomaly'] == True]
    if len(anomaly_df) > 0:
        fig.add_trace(
            go.Scatter(
                x=anomaly_df.index,
                y=anomaly_df['Grid Frequency (Hz)'],
                name='Anomalies',
                mode='markers',
                marker=dict(color='red', size=8, symbol='x')
            ),
            row=1, col=1
        )
    
    # Threshold line
    fig.add_hline(y=49.8, line_dash="dash", line_color="red", row=1, col=1)
    
    # Solar generation
    fig.add_trace(
        go.Scatter(
            x=recent_df.index,
            y=recent_df['Solar PV Output (kW)'],
            name='Solar',
            line=dict(color='#f39c12', width=2),
            mode='lines'
        ),
        row=2, col=1
    )
    
    # Wind generation
    fig.add_trace(
        go.Scatter(
            x=recent_df.index,
            y=recent_df['Wind Power Output (kW)'],
            name='Wind',
            line=dict(color='#27ae60', width=2),
            mode='lines'
        ),
        row=2, col=1,
        secondary_y=True
    )
    
    # Update layout
    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_yaxes(title_text="Frequency (Hz)", row=1, col=1)
    fig.update_yaxes(title_text="Solar (kW)", row=2, col=1)
    fig.update_yaxes(title_text="Wind (kW)", secondary_y=True, row=2, col=1)
    
    fig.update_layout(
        height=600,
        showlegend=True,
        hovermode='x unified',
        title=f"Last {hours} Hours Overview"
    )
    
    return fig


@cl.on_chat_start
async def on_chat_start():
    """
    Initialize chat session with data loading and welcome message
    """
    # Show loading message
    loading_msg = await cl.Message(content="🔄 Initializing Smart Microgrid AI Operator...").send()
    
    try:
        # 1. Load data
        loading_msg.content = "📊 Loading grid data..."
        await loading_msg.update()
        df = load_data(DATA_FILE)
        
        # 2. Create agent
        loading_msg.content = "🤖 Initializing AI Agent..."
        await loading_msg.update()
        agent = get_or_create_agent(df)
        
        # 3. Store in session
        cl.user_session.set("agent", agent)
        cl.user_session.set("data", df)
        
        # 4. Get statistics
        stats = get_statistics(df)
        latest = get_latest_status(df)
        
        # 5. Update loading message to welcome
        await loading_msg.remove()
        
        # Send welcome message
        welcome_text = f"""# 🔋 Smart Microgrid AI Operator

Welcome to the enterprise-grade AI-powered grid monitoring system!

## 📊 System Status

- **Total Records:** {stats['total_records']:,}
- **Date Range:** {stats['date_range']['start']} to {stats['date_range']['end']}
- **Anomalies Detected:** {stats['anomalies']['count']} ({stats['anomalies']['percentage']:.2f}%)
- **Avg Frequency:** {stats['avg_frequency']:.4f} Hz

## 🎯 What I Can Do

1. **Analyze Anomalies** - "Analyze the anomaly at 2021-01-01 01:30:00"
2. **Generate Reports** - "Show me a summary of recent anomalies"
3. **Explain Patterns** - "Why did the frequency drop?"
4. **Provide Recommendations** - "What should operators do?"

**Try asking:** "What's the current grid status?" or "Analyze the first anomaly"
"""
        
        await cl.Message(content=welcome_text).send()
        
        # Send real-time dashboard
        freq_gauge = create_status_gauge(
            latest['grid_frequency'],
            "Current Grid Frequency"
        )
        
        trend_chart = create_trend_chart(df, hours=24)
        
        elements = [
            cl.Plotly(name="frequency_gauge", figure=freq_gauge, display="inline"),
            cl.Plotly(name="trend_chart", figure=trend_chart, display="inline")
        ]
        
        await cl.Message(
            content="## 📈 Live Dashboard",
            elements=elements
        ).send()
        
    except Exception as e:
        loading_msg.content = f"❌ **Initialization Error**\n\n```\n{str(e)}\n```\n\nPlease check:\n1. Ollama is running: `ollama serve`\n2. Model is available: `ollama list`\n3. Data file exists: {DATA_FILE}"
        await loading_msg.update()


@cl.on_message
async def on_message(message: cl.Message):
    """
    Handle incoming messages with Chain-of-Thought visualization
    """
    agent = cl.user_session.get("agent")
    df = cl.user_session.get("data")
    
    if agent is None:
        await cl.Message(content="❌ Agent not initialized. Please refresh the page.").send()
        return
    
    # Create a parent step for the entire reasoning process
    async with cl.Step(name="🤖 AI Agent Processing", type="llm") as main_step:
        main_step.input = message.content
        
        try:
            # Show thinking animation
            async with cl.Step(name="🧠 Analyzing Query", type="tool", parent_id=main_step.id) as thinking_step:
                thinking_step.input = message.content
                
                # Parse query for timestamp
                import re
                timestamp_match = re.search(r'\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}', message.content)
                
                if timestamp_match:
                    ts = timestamp_match.group(0)
                    thinking_step.output = f"Detected timestamp: {ts}"
                else:
                    thinking_step.output = "General query - will analyze overall patterns"
            
            # Invoke agent (synchronous call wrapped in async)
            async with cl.Step(name="⚙️ Agent Execution", type="run", parent_id=main_step.id) as execution_step:
                # Run synchronous agent in thread pool
                response = await cl.make_async(agent.invoke)({"input": message.content})
                execution_step.output = "Agent completed analysis"
            
            # Extract output
            if isinstance(response, dict):
                agent_output = response.get('output', str(response))
            else:
                agent_output = str(response)
            
            main_step.output = agent_output
            
            # Check if analysis mentions specific timestamp
            if timestamp_match:
                try:
                    ts = pd.to_datetime(timestamp_match.group(0))
                    
                    if ts in df.index:
                        # Create visualization for the analyzed timestamp
                        context_start = ts - timedelta(hours=2)
                        context_end = ts + timedelta(hours=2)
                        context_df = df.loc[context_start:context_end]
                        
                        # Create chart
                        fig = make_subplots(
                            rows=2, cols=1,
                            subplot_titles=('Grid Frequency', 'Renewable Generation'),
                            vertical_spacing=0.15
                        )
                        
                        # Frequency
                        fig.add_trace(
                            go.Scatter(x=context_df.index, y=context_df['Grid Frequency (Hz)'],
                                     name='Frequency', line=dict(color='blue')),
                            row=1, col=1
                        )
                        fig.add_vline(x=ts, line_dash="dash", line_color="red", row=1, col=1)
                        fig.add_hline(y=49.8, line_dash="dash", line_color="red", row=1, col=1)
                        
                        # Generation
                        fig.add_trace(
                            go.Scatter(x=context_df.index, y=context_df['Solar PV Output (kW)'],
                                     name='Solar', line=dict(color='orange')),
                            row=2, col=1
                        )
                        fig.add_trace(
                            go.Scatter(x=context_df.index, y=context_df['Wind Power Output (kW)'],
                                     name='Wind', line=dict(color='green')),
                            row=2, col=1
                        )
                        fig.add_vline(x=ts, line_dash="dash", line_color="red", row=2, col=1)
                        
                        fig.update_layout(height=600, showlegend=True)
                        
                        elements = [cl.Plotly(name="analysis_chart", figure=fig, display="inline")]
                        
                        await cl.Message(
                            content="## 📊 Detailed Visualization\n\n" + agent_output,
                            elements=elements
                        ).send()
                        return
                        
                except Exception as viz_error:
                    print(f"Visualization error: {viz_error}")
            
            # Send text response
            await cl.Message(content=agent_output).send()
            
        except Exception as e:
            main_step.output = f"Error: {str(e)}"
            await cl.Message(
                content=f"❌ **Error during analysis:**\n\n```\n{str(e)}\n```"
            ).send()


@cl.on_chat_end
async def on_chat_end():
    """Handle chat session end"""
    print("[CHAINLIT] Chat session ended")


# Custom settings
@cl.set_chat_profiles
async def chat_profile():
    """Define chat profiles for different modes"""
    return [
        cl.ChatProfile(
            name="Standard",
            markdown_description="Standard AI agent mode",
            icon="🤖"
        ),
        cl.ChatProfile(
            name="Expert",
            markdown_description="Detailed technical analysis mode",
            icon="🔬"
        )
    ]
