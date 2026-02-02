# 🔋 Smart Grid AI Operator

An intelligent Agentic AI system for monitoring and analyzing microgrid anomalies using LangChain and local Llama 3.1 via Ollama.

## 🎯 Project Overview

This system provides real-time anomaly detection and root cause analysis for smart city energy grids. It uses a local LLM (Llama 3.1) to analyze correlations between grid frequency drops, renewable energy generation changes, and weather conditions.

## 🏗️ Architecture

### Tech Stack
- **Python 3.10+**
- **LangChain** - Agent orchestration framework
- **LangChain-Ollama** - Local LLM inference
- **Pandas** - Data manipulation and analysis
- **Streamlit** - Interactive web interface
- **Plotly** - Interactive visualizations
- **Ollama + Llama 3.1** - Local AI model (no cloud API needed!)

### System Components

```
├── data_loader.py         # Phase 2: Data loading and preprocessing
├── agent_setup.py         # Phase 3: LangChain Ollama agent configuration
├── main_analysis.py       # Phase 4: Main analysis logic and anomaly detection
├── app.py                 # Phase 5: Streamlit UI application
├── requirements.txt       # Python dependencies
└── smart_city_energy_dataset.csv  # Your dataset
```

## 📊 Dataset Structure

The system expects a CSV file with these key columns:
- `Timestamp` - Date/time of measurement
- `Grid Frequency (Hz)` - Main indicator for anomalies (< 49.8 Hz = anomaly)
- `Solar PV Output (kW)` - Solar power generation
- `Wind Power Output (kW)` - Wind power generation
- `Cloud Cover (%)` - Weather condition
- `Wind Speed (m/s)` - Wind condition
- And many more operational metrics...

## 🚀 Quick Start

### Prerequisites

1. **Install Ollama**
   ```bash
   # Visit https://ollama.ai and download for your OS
   # Or on Linux/Mac:
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Pull Llama 3.1 Model**
   ```bash
   ollama run llama3.1
   ```
   This will download the model (~4GB) and start the Ollama server.

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the System

#### Option 1: Streamlit Web UI (Recommended)

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

#### Option 2: Command Line Testing

Test individual components:

```python
# Test data loading
python data_loader.py

# Test the full analysis pipeline
python -c "
from data_loader import load_grid_data
from agent_setup import create_smart_grid_agent
from main_analysis import analyze_grid_event

# Load data
df = load_grid_data('smart_city_energy_dataset.csv')

# Initialize AI agent
llm, agent = create_smart_grid_agent(df)

# Find first anomaly timestamp
anomaly_times = df[df['Is_Anomaly'] == True].index
target = anomaly_times[0].strftime('%Y-%m-%d %H:%M:%S')

# Run analysis
result = analyze_grid_event(target, df, agent)
print(result)
"
```

## 💡 How It Works

### Phase 1: Context Setting
The system is configured as an expert grid operator AI, specialized in analyzing:
- Correlations between grid frequency drops and renewable generation
- Impact of weather conditions on power generation
- Curtailment risks and mitigation strategies

### Phase 2: Data Loading & Preprocessing
```python
from data_loader import load_grid_data

df = load_grid_data('smart_city_energy_dataset.csv')
# - Parses timestamps
# - Creates Is_Anomaly column (Grid Frequency < 49.8 Hz)
# - Sorts by time
```

### Phase 3: Agent Setup
```python
from agent_setup import create_smart_grid_agent

llm, agent = create_smart_grid_agent(df)
# - Initializes local Llama 3.1 (temperature=0 for precision)
# - Creates Pandas DataFrame Agent
# - Configures with grid operator expertise
```

### Phase 4: Anomaly Detection & Analysis
```python
from main_analysis import analyze_grid_event

result = analyze_grid_event(timestamp, df, agent)
# - Checks if anomaly exists
# - If yes, triggers AI agent
# - Agent analyzes 30-min window
# - Calculates % changes
# - Provides root cause + recommendations
```

### Phase 5: Interactive UI
The Streamlit app provides:
- 📊 Real-time anomaly detection dashboard
- 🤖 One-click AI analysis
- 📈 Interactive time-series visualizations
- 📋 Raw data inspection
- 💡 AI-generated recommendations

## 🎓 Use Cases

Perfect for demonstrating to professors:

1. **Real-time Grid Monitoring**: Detect when frequency drops below safe thresholds
2. **Root Cause Analysis**: AI explains WHY anomalies occur (weather, generation drops, etc.)
3. **Predictive Insights**: Correlate weather forecasts with generation patterns
4. **Local AI Privacy**: All analysis runs locally - no data sent to cloud APIs
5. **Educational Tool**: Learn about smart grids, LangChain, and agentic AI

## 🔍 Example Analysis Output

```
ANOMALY DETECTED at 2025-01-15 14:30:00

--- DATA COMPARISON ---
Grid Frequency: 49.73 Hz → 49.65 Hz (-0.08 Hz)
Solar PV Output: 450 kW → 180 kW (-60% drop)
Cloud Cover: 15% → 85% (+70%)

--- ROOT CAUSE ANALYSIS ---
Sudden cloud cover increase caused 60% drop in solar generation.
Wind remained stable. The loss of 270 kW solar capacity triggered
frequency instability as demand exceeded supply.

--- RECOMMENDATION ---
1. Activate battery storage discharge immediately
2. Increase grid import from adjacent regions
3. Weather forecast shows clearing in 45 minutes - temporary event
```

## 🛠️ Troubleshooting

### Ollama Connection Error
```bash
# Make sure Ollama is running
ollama serve

# In another terminal, verify model is available
ollama list
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### CSV File Too Large
If your CSV is >50MB, the system will still work via command line. Just use:
```python
df = load_grid_data('smart_city_energy_dataset.csv')
```

### Agent Taking Too Long
- First run downloads the model (~4GB)
- Subsequent runs should be faster (30-60 seconds)
- Reduce `max_iterations` in `agent_setup.py` if needed

## 📝 Customization

### Change Anomaly Threshold
Edit `data_loader.py`:
```python
df['Is_Anomaly'] = df['Grid Frequency (Hz)'] < 49.8  # Change 49.8 to your threshold
```

### Use Different LLM Model
Edit `agent_setup.py`:
```python
llm = ChatOllama(model="llama3.1")  # Try: mistral, codellama, etc.
```

### Adjust Analysis Window
Edit `main_analysis.py`:
```python
prior_dt = target_dt - timedelta(minutes=30)  # Change minutes window
```

## 📚 Documentation

- **LangChain Docs**: https://python.langchain.com/
- **Ollama Models**: https://ollama.ai/library
- **Streamlit Docs**: https://docs.streamlit.io/
- **Pandas Guide**: https://pandas.pydata.org/docs/

## 🤝 Contributing

This is a demonstration project for academic purposes. Feel free to:
- Add more weather parameters to the analysis
- Implement predictive models
- Add alerting systems
- Export reports to PDF

## 📄 License

MIT License - Free for academic and research use

## 👨‍💻 Author

Built as a Smart Grid Data Analysis demonstration using modern AI agent techniques.

---

**🎉 Ready to impress your professor!**

Start the system with:
```bash
streamlit run app.py
```

And watch the AI analyze grid anomalies in real-time! 🔋⚡
