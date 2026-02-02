"""
Streamlit UI Application
Phase 5: Building Demo Interface
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import sys

# Import our custom modules
from data_loader import load_grid_data, get_anomaly_timestamps
from agent_setup import create_smart_grid_agent
from main_analysis import analyze_grid_event, get_event_context


# Cached functions to prevent re-initialization on every interaction
@st.cache_resource
def load_and_cache_data(csv_path: str):
    """Cache data loading to prevent reloading on every Streamlit rerun."""
    return load_grid_data(csv_path)


@st.cache_resource
def initialize_agent(_df):
    """Cache agent initialization to prevent Ollama reconnection on every interaction.
    Note: _df with underscore prevents Streamlit from hashing the DataFrame."""
    return create_smart_grid_agent(_df)


# Page configuration
st.set_page_config(
    page_title="Smart Grid AI Operator",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)


def init_session_state():
    """Initialize session state variables."""
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'llm' not in st.session_state:
        st.session_state.llm = None
    if 'anomaly_timestamps' not in st.session_state:
        st.session_state.anomaly_timestamps = []


def plot_grid_metrics(context_df: pd.DataFrame, target_timestamp: str):
    """
    Create interactive plotly chart showing Grid Frequency and Solar/Wind Power
    around the target timestamp.
    """
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Grid Frequency (Hz)', 'Renewable Generation (kW)'),
        vertical_spacing=0.12,
        specs=[[{"secondary_y": False}],
               [{"secondary_y": True}]]
    )
    
    # Plot Grid Frequency
    fig.add_trace(
        go.Scatter(
            x=context_df.index,
            y=context_df['Grid Frequency (Hz)'],
            name='Grid Frequency',
            line=dict(color='#FF6B6B', width=2),
            mode='lines+markers'
        ),
        row=1, col=1
    )
    
    # Add threshold line at 49.8 Hz
    fig.add_hline(
        y=49.8,
        line_dash="dash",
        line_color="red",
        annotation_text="Anomaly Threshold (49.8 Hz)",
        row=1, col=1
    )
    
    # Plot Solar PV Output
    fig.add_trace(
        go.Scatter(
            x=context_df.index,
            y=context_df['Solar PV Output (kW)'],
            name='Solar PV Output',
            line=dict(color='#FFD93D', width=2),
            mode='lines+markers'
        ),
        row=2, col=1
    )
    
    # Plot Wind Power Output
    fig.add_trace(
        go.Scatter(
            x=context_df.index,
            y=context_df['Wind Power Output (kW)'],
            name='Wind Power Output',
            line=dict(color='#6BCB77', width=2),
            mode='lines+markers',
            yaxis='y3'
        ),
        row=2, col=1,
        secondary_y=True
    )
    
    # Add vertical line at target timestamp
    target_dt = pd.to_datetime(target_timestamp)
    fig.add_vline(
        x=target_dt,
        line_dash="dash",
        line_color="purple",
        annotation_text="Target Event",
        row='all'
    )
    
    # Update layout
    fig.update_xaxes(title_text="Time", row=2, col=1)
    fig.update_yaxes(title_text="Frequency (Hz)", row=1, col=1)
    fig.update_yaxes(title_text="Solar Output (kW)", row=2, col=1)
    fig.update_yaxes(title_text="Wind Output (kW)", secondary_y=True, row=2, col=1)
    
    fig.update_layout(
        height=700,
        showlegend=True,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def main():
    """Main Streamlit application."""
    init_session_state()
    
    # Header
    st.title("🔋 Smart Grid AI Operator")
    st.markdown("""
    ### Agentic AI System for Microgrid Anomaly Monitoring
    *Powered by LangChain + Ollama (Llama 3.1) + Real-time Data Analysis*
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ System Configuration")
        
        # File upload
        st.subheader("1. Load Dataset")
        uploaded_file = st.file_uploader(
            "Upload Smart City Energy CSV",
            type=['csv'],
            help="Upload the smart_city_energy_dataset.csv file"
        )
        
        # Default file path option
        use_default = st.checkbox("Use default file path", value=True)
        
        if use_default or uploaded_file is not None:
            if st.button("🔄 Load & Initialize System", type="primary"):
                with st.spinner("Loading dataset..."):
                    try:
                        # Load data using cached function
                        if use_default:
                            csv_path = "smart_city_energy_dataset.csv"
                        else:
                            csv_path = uploaded_file
                        
                        st.session_state.df = load_and_cache_data(csv_path)
                        st.session_state.anomaly_timestamps = get_anomaly_timestamps(
                            st.session_state.df
                        )
                        
                        st.success(f"✓ Dataset loaded: {len(st.session_state.df)} rows")
                        st.info(f"📊 Anomalies detected: {len(st.session_state.anomaly_timestamps)}")
                        
                    except Exception as e:
                        st.error(f"Error loading data: {e}")
                        return
                
                with st.spinner("Initializing AI Agent (connecting to Ollama)..."):
                    try:
                        # Use cached agent initialization
                        st.session_state.llm, st.session_state.agent = initialize_agent(
                            st.session_state.df
                        )
                        st.success("✓ AI Agent initialized and ready!")
                    except Exception as e:
                        st.error(f"Error initializing agent: {e}")
                        st.warning("Make sure Ollama is running with llama3.1 model installed.")
                        st.code("ollama run llama3.1", language="bash")
                        return
        
        # System status
        st.markdown("---")
        st.subheader("System Status")
        
        if st.session_state.df is not None:
            st.success("✓ Data Loaded")
            st.metric("Total Records", len(st.session_state.df))
            st.metric("Anomalies", len(st.session_state.anomaly_timestamps))
        else:
            st.warning("⏳ Waiting for data...")
        
        if st.session_state.agent is not None:
            st.success("✓ AI Agent Active")
        else:
            st.warning("⏳ Agent not initialized...")
    
    # Main content area
    if st.session_state.df is None:
        st.info("👈 Please load the dataset from the sidebar to begin.")
        
        # Show instructions
        st.markdown("---")
        st.subheader("📖 Quick Start Guide")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Prerequisites:**
            1. Install Ollama: `https://ollama.ai`
            2. Pull Llama 3.1: `ollama run llama3.1`
            3. Install Python dependencies: `pip install -r requirements.txt`
            """)
        
        with col2:
            st.markdown("""
            **System Features:**
            - 🤖 Local AI agent (no cloud API needed)
            - 📊 Real-time anomaly detection
            - 🔍 Root cause analysis
            - 📈 Interactive visualizations
            """)
        
        return
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 System Overview", "🔍 Anomaly Analysis"])
    
    # Tab 1: System Overview with Time Series
    with tab1:
        st.header("🌐 Grid Status Overview")
        
        # Time range selector
        st.subheader("Time Series Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            # Sample data for visualization (last 7 days or all data if less)
            days_to_show = st.slider("Days to display", 1, 30, 7)
            
        with col2:
            show_anomalies = st.checkbox("Highlight Anomalies", value=True)
        
        # Create time series plot with anomalies marked
        end_time = st.session_state.df.index.max()
        start_time = end_time - timedelta(days=days_to_show)
        
        plot_df = st.session_state.df.loc[start_time:end_time]
        
        # Create figure
        fig_overview = go.Figure()
        
        # Add grid frequency line
        fig_overview.add_trace(go.Scatter(
            x=plot_df.index,
            y=plot_df['Grid Frequency (Hz)'],
            mode='lines',
            name='Grid Frequency',
            line=dict(color='#3498db', width=1.5),
            hovertemplate='<b>Time:</b> %{x}<br><b>Frequency:</b> %{y:.4f} Hz<extra></extra>'
        ))
        
        # Add anomaly points in red
        if show_anomalies:
            anomaly_df = plot_df[plot_df['Is_Anomaly'] == True]
            fig_overview.add_trace(go.Scatter(
                x=anomaly_df.index,
                y=anomaly_df['Grid Frequency (Hz)'],
                mode='markers',
                name='Anomalies',
                marker=dict(color='red', size=6, symbol='x'),
                hovertemplate='<b>ANOMALY</b><br>Time: %{x}<br>Frequency: %{y:.4f} Hz<extra></extra>'
            ))
        
        # Add threshold line
        fig_overview.add_hline(
            y=49.8,
            line_dash="dash",
            line_color="red",
            annotation_text="Anomaly Threshold",
            annotation_position="right"
        )
        
        fig_overview.update_layout(
            title=f"Grid Frequency Time Series (Last {days_to_show} Days)",
            xaxis_title="Time",
            yaxis_title="Grid Frequency (Hz)",
            height=500,
            hovermode='x unified',
            showlegend=True
        )
        
        st.plotly_chart(fig_overview, use_container_width=True)
        
        # Statistics cards
        st.subheader("📈 Key Metrics")
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            avg_freq = plot_df['Grid Frequency (Hz)'].mean()
            st.metric("Avg Frequency", f"{avg_freq:.4f} Hz")
        
        with stat_col2:
            anomaly_count = plot_df['Is_Anomaly'].sum()
            anomaly_rate = (anomaly_count / len(plot_df)) * 100
            st.metric("Anomaly Rate", f"{anomaly_rate:.2f}%", 
                     delta=f"{anomaly_count} events")
        
        with stat_col3:
            avg_solar = plot_df['Solar PV Output (kW)'].mean()
            st.metric("Avg Solar Output", f"{avg_solar:.1f} kW")
        
        with stat_col4:
            avg_wind = plot_df['Wind Power Output (kW)'].mean()
            st.metric("Avg Wind Output", f"{avg_wind:.1f} kW")
    
    # Tab 2: Anomaly Analysis (existing code)
    with tab2:
        st.header("🔍 Detailed Anomaly Analysis")
        
        # Timestamp selection
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if len(st.session_state.anomaly_timestamps) > 0:
                selected_timestamp = st.selectbox(
                    "Select an anomaly timestamp to analyze:",
                    st.session_state.anomaly_timestamps,
                    help="Choose from detected anomaly events where Grid Frequency < 49.8 Hz"
                )
            else:
                st.warning("No anomalies detected in the dataset.")
                selected_timestamp = None
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            analyze_button = st.button("🚀 Run Analysis", type="primary", disabled=(selected_timestamp is None))
        
        # Analysis results
        if analyze_button and selected_timestamp:
            if st.session_state.agent is None:
                st.error("AI Agent not initialized. Please initialize the system first.")
                return
            
            # Show raw data for the selected timestamp
            st.subheader("📋 Raw Data at Selected Timestamp")
            
            target_dt = pd.to_datetime(selected_timestamp)
            row = st.session_state.df.loc[target_dt]
            
            # Display key metrics
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric("Grid Frequency", f"{row['Grid Frequency (Hz)']:.4f} Hz", 
                         delta=f"{row['Grid Frequency (Hz)'] - 50:.4f} Hz")
            
            with metric_col2:
                st.metric("Solar PV Output", f"{row['Solar PV Output (kW)']:.2f} kW")
            
            with metric_col3:
                st.metric("Wind Power Output", f"{row['Wind Power Output (kW)']:.2f} kW")
            
            with metric_col4:
                st.metric("Cloud Cover", f"{row['Cloud Cover (%)']:.1f}%")
            
            # Expandable full data view
            with st.expander("View Complete Data Row"):
                st.dataframe(row.to_frame().T, use_container_width=True)
            
            st.markdown("---")
            
            # Run AI analysis
            st.subheader("🤖 AI Agent Analysis")
            
            with st.spinner("🧠 AI Agent is analyzing the anomaly... (this may take 30-60 seconds)"):
                result = analyze_grid_event(
                    selected_timestamp,
                    st.session_state.df,
                    st.session_state.agent
                )
            
            # Display results
            if result['status'] == 'anomaly':
                st.success("✓ Analysis Complete")
                
                # Show agent's analysis
                st.markdown("### 📊 Agent's Report")
                st.markdown(result['analysis'])
                
            elif result['status'] == 'normal':
                st.info(result['message'])
            else:
                st.error(f"Analysis Error: {result['message']}")
            
            st.markdown("---")
            
            # Visualization
            st.subheader("📈 Time Series Visualization (±2 hours)")
            
            context_df = get_event_context(
                selected_timestamp,
                st.session_state.df,
                hours_before=2,
                hours_after=2
            )
            
            fig = plot_grid_metrics(context_df, selected_timestamp)
            st.plotly_chart(fig, use_container_width=True)
            
            # Additional context
            with st.expander("📊 Statistical Summary (±2 hours)"):
                key_cols = ['Grid Frequency (Hz)', 'Solar PV Output (kW)', 
                           'Wind Power Output (kW)', 'Cloud Cover (%)', 'Wind Speed (m/s)']
                st.dataframe(context_df[key_cols].describe(), use_container_width=True)


if __name__ == "__main__":
    main()
