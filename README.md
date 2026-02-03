# 🔋 Smart Microgrid AI System

## 🌟 Enterprise Edition v2.0.0

An intelligent **enterprise-grade** AI system for monitoring and analyzing smart grid anomalies using **FastAPI + Chainlit + LangChain** architecture with local Llama 3.1 via Ollama.

> **✨ New in v2.0:** RESTful API backend, React-based AI chat interface, auto-generated Swagger docs, and Chain-of-Thought visualization!

---

## 🎯 Project Overview

This system provides real-time anomaly detection, root cause analysis, and intelligent decision support for smart city microgrids. It uses a local LLM (Llama 3.1) to analyze correlations between grid frequency drops, renewable energy generation changes, and operational conditions.

### Key Features

- 🚀 **Enterprise Architecture**: FastAPI + Chainlit + React
- 🤖 **AI-Powered Analysis**: LangChain agents with pandas dataframe tools
- 📊 **Real-time Monitoring**: Interactive Plotly dashboards
- 🔗 **RESTful API**: 8+ endpoints with OpenAPI/Swagger documentation
- 💬 **AI Chat Interface**: Chain-of-Thought reasoning visualization
- 🔒 **Privacy-First**: 100% local LLM inference (no cloud API)
- ⚡ **High Performance**: Async I/O, caching, WebSocket streaming

---

## 🏗️ Architecture

### Tech Stack (v2.0)

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend API** | FastAPI 0.109+ | High-performance REST API server |
| **Frontend/Chat** | Chainlit 1.0+ | React-based AI chat interface |
| **AI Framework** | LangChain 0.2+ | Agent orchestration & tool calling |
| **LLM Inference** | Ollama + Llama 3.1 | Local 8B-parameter model |
| **Data Processing** | Pandas 2.2+ | Dataframe manipulation |
| **Visualization** | Plotly 6.5+ | Interactive charts & gauges |
| **Web Server** | Uvicorn 0.27+ | ASGI server with async support |

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│              USER INTERFACE LAYER                   │
│  ┌──────────────┐          ┌──────────────────┐    │
│  │ API Clients  │          │  Chainlit Chat   │    │
│  │ (curl/HTTP)  │          │  (React UI)      │    │
│  └──────┬───────┘          └────────┬─────────┘    │
└─────────│──────────────────────────│───────────────┘
          │                          │
          │ REST API                 │ WebSocket
          │                          │
┌─────────▼──────────────────────────▼────────────────┐
│          FASTAPI SERVER (Port 8000)                 │
│  ┌──────────────────────────────────────────────┐  │
│  │  API Endpoints (/api/*)                      │  │
│  │  - /docs (Swagger UI)                        │  │
│  │  - /api/health, /api/grid/statistics         │  │
│  │  - /api/grid/status, /api/grid/anomalies     │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Chainlit Application (/chat)                │  │
│  │  - AI conversation with CoT visualization    │  │
│  │  - Plotly React components                   │  │
│  └──────────────────────────────────────────────┘  │
└───────────────────┬──────────────────────────────┘
                    │
        ┌───────────┴──────────┐
        │                      │
┌───────▼────────┐   ┌─────────▼─────────┐
│  Data Module   │   │  Agent Module     │
│  (app/         │   │  (app/            │
│   data_loader) │   │   agent_setup)    │
└───────┬────────┘   └─────────┬─────────┘
        │                      │
┌───────▼──────────────────────▼─────────┐
│  Data & Model Layer                    │
│  - CSV Dataset (72,960 records)        │
│  - Ollama (llama3:8b-instruct-q4_K_M)  │
└────────────────────────────────────────┘
```

### Project Structure

```
ecogridiea/
├── app/                          # ⭐ Enterprise application
│   ├── __init__.py              #    Package initialization
│   ├── server.py                #    FastAPI main server (Entry Point)
│   ├── chainlit_app.py          #    Chainlit AI chat interface
│   ├── data_loader.py           #    Data loading with caching
│   └── agent_setup.py           #    LangChain agent factory
│
├── data/
│   └── smart_city_energy_dataset.csv  # Dataset (72,960 rows)
│
├── .chainlit/
│   └── config.toml              #    Chainlit configuration
│
├── requirements.txt             #    Python dependencies
├── start_enterprise.bat         #    Windows launcher script
├── test_enterprise.py           #    Component validation tests
├── test_api.py                  #    API endpoint tests
│
├── ENTERPRISE_ARCHITECTURE.md   # 📚 Architecture documentation
├── DEPLOYMENT_REPORT.md         # ✅ Deployment verification report
├── README.md                    # 📖 This file
│
└── [Legacy Files]               # 📦 Streamlit version (v1.0)
    ├── app.py                   #    Streamlit UI (still works)
    ├── data_loader.py           #    Old data loader
    ├── agent_setup.py           #    Old agent setup
    └── main_analysis.py         #    Analysis logic
```

---

## 📊 Dataset Structure

The system expects a CSV file with these key columns:
- `Timestamp` - Date/time of measurement
- `Grid Frequency (Hz)` - Main indicator for anomalies (< 49.8 Hz = anomaly)
- `Solar PV Output (kW)` - Solar power generation
- `Wind Power Output (kW)` - Wind power generation
- `Cloud Cover (%)` - Weather condition
- `Wind Speed (m/s)` - Wind condition
- `Z_Score` - Anomaly score (auto-calculated)
- And 50+ more operational metrics...

**Current Dataset:**
- **Total Records:** 72,960
- **Time Span:** 2021-01-01 to 2025-02-28 (4+ years)
- **Anomalies Detected:** 11,628 (15.94%)
- **Columns:** 61

---

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
   ollama pull llama3:8b-instruct-q4_K_M
   # OR simply run:
   ollama run llama3:8b-instruct-q4_K_M
   ```
   This will download the 4-bit quantized 8B model (~4.7GB) and start the Ollama server.

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Enterprise System (v2.0)

#### ⭐ Option 1: Windows Launcher Script (Recommended)

```bash
# Automatically checks Ollama, activates venv, starts server
start_enterprise.bat
```

#### Option 2: Manual Start (Cross-platform)

```bash
# Set PYTHONPATH for module imports
export PYTHONPATH=$PWD  # Linux/Mac
$env:PYTHONPATH = $PWD  # Windows PowerShell

# Start the FastAPI + Chainlit server
uvicorn app.server:app --host 0.0.0.0 --port 8000
```

#### Option 3: Development Mode (Auto-reload)

```bash
$env:PYTHONPATH = $PWD  # Windows
uvicorn app.server:app --host 0.0.0.0 --port 8000 --reload
```

### Access Points

Once the server is running, you can access:

- **🌐 Root Info**: http://localhost:8000/
- **📚 API Documentation**: http://localhost:8000/docs (Swagger UI)
- **💬 AI Chat Interface**: http://localhost:8000/chat (Chainlit UI)
- **🔧 Health Check**: http://localhost:8000/api/health

---

## 🔌 API Endpoints

### Core Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | System information |
| GET | `/docs` | Swagger UI documentation |
| GET | `/redoc` | ReDoc documentation |
| GET | `/api/health` | Health check status |
| GET | `/api/grid/statistics` | Overall grid statistics |
| GET | `/api/grid/status` | Latest grid status |
| GET | `/api/grid/status/{timestamp}` | Historical data at timestamp |
| GET | `/api/grid/anomalies` | List anomalies (paginated) |
| GET | `/api/grid/range` | Query time range |

### API Examples

```bash
# Health check
curl http://localhost:8000/api/health

# Get overall statistics
curl http://localhost:8000/api/grid/statistics

# Get latest grid status
curl http://localhost:8000/api/grid/status

# Get first 5 anomalies
curl "http://localhost:8000/api/grid/anomalies?limit=5&offset=0"

# Query specific timestamp
curl "http://localhost:8000/api/grid/status/2021-01-01%2001:30:00"

# Time range query
curl "http://localhost:8000/api/grid/range?start=2021-01-01&end=2021-01-02"
```

See [ENTERPRISE_ARCHITECTURE.md](ENTERPRISE_ARCHITECTURE.md) for detailed API documentation.

---

## 💬 AI Chat Interface

Access the Chainlit interface at http://localhost:8000/chat

### Features

1. **Real-time AI Conversation**
   - Natural language queries about grid anomalies
   - Contextual understanding of timestamps and patterns
   - Automatic data retrieval and analysis

2. **Chain-of-Thought Visualization**
   - See the AI's reasoning process step-by-step
   - Transparent decision making with intermediate steps
   - Tool usage logging

3. **Interactive Visualizations**
   - Real-time frequency gauge (Green/Yellow/Red status)
   - 24-hour trend charts with anomaly markers
   - Event-specific analysis charts

4. **Example Queries**
   ```
   - "What's the current grid status?"
   - "Analyze the anomaly at 2021-01-01 01:30:00"
   - "Show me recent frequency drops"
   - "Why did the grid become unstable at midnight?"
   - "What's the correlation between solar output and anomalies?"
   ```

---

## 🧪 Testing

### Run Component Tests

```bash
python test_enterprise.py
```

Expected output:
```
[1/4] Testing Data Loader...    ✅ PASS
[2/4] Testing Agent Setup...    ✅ PASS
[3/4] Testing FastAPI Server... ✅ PASS
[4/4] Testing Chainlit App...   ✅ PASS

ALL TESTS PASSED! 🚀
```

### Test API Endpoints

```bash
python test_api.py
```

---

## 🎓 Legacy Streamlit Version

The original Streamlit interface (v1.0) is still available:

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
