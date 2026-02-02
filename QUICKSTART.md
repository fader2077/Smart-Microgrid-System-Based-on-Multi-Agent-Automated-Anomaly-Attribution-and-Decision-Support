# 🚀 Quick Start Guide - Smart Grid AI Operator

## 📋 Prerequisites Checklist

- [ ] Python 3.10 or higher installed
- [ ] Ollama installed (https://ollama.ai)
- [ ] Llama 3.1 model downloaded
- [ ] CSV dataset in project folder

---

## ⚡ Installation (5 minutes)

### Step 1: Install Ollama

**Windows:**
1. Download from https://ollama.ai
2. Run installer
3. Open PowerShell/Command Prompt

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Download Llama 3.1 Model

```bash
ollama pull llama3.1
```

This downloads ~4GB. First time only!

### Step 3: Install Python Dependencies

```bash
# Option 1: Use the setup script (Windows)
setup.bat

# Option 2: Manual installation
pip install -r requirements.txt
```

---

## 🎮 How to Run

### Option 1: Web UI (Best for Demos) ⭐

```bash
streamlit run app.py
```

Open browser to: http://localhost:8501

**Features:**
- 📊 Interactive dashboard
- 🎯 Point-and-click analysis
- 📈 Beautiful visualizations
- 💾 Upload CSV files
- 🖥️ Perfect for presentations!

### Option 2: Command Line Demo

```bash
python demo.py
```

**Features:**
- 🖥️ Terminal interface
- 📝 Text-based interaction
- ⚡ Quick testing
- 🔍 Browse all anomalies

### Option 3: System Test

```bash
python test_system.py
```

Runs automated tests to verify everything works.

---

## 📖 Usage Examples

### Example 1: Analyze First Anomaly

```python
from data_loader import load_grid_data
from agent_setup import create_smart_grid_agent
from main_analysis import analyze_grid_event, get_anomaly_timestamps

# Load data
df = load_grid_data('smart_city_energy_dataset.csv')

# Initialize AI
llm, agent = create_smart_grid_agent(df)

# Get first anomaly
anomalies = get_anomaly_timestamps(df)
target = anomalies[0]

# Analyze
result = analyze_grid_event(target, df, agent)
print(result['analysis'])
```

### Example 2: Check Specific Timestamp

```python
# Analyze a specific time
result = analyze_grid_event('2021-01-15 14:30:00', df, agent)

if result['status'] == 'anomaly':
    print(f"⚠️ Anomaly detected!")
    print(result['analysis'])
else:
    print("✓ System normal")
```

### Example 3: Get Event Context

```python
from main_analysis import get_event_context

# Get ±2 hours of data around event
context = get_event_context('2021-01-15 14:30:00', df, hours_before=2, hours_after=2)

# Show frequency trend
print(context['Grid Frequency (Hz)'])
```

---

## 🔧 Troubleshooting

### "Connection refused" / "Cannot connect to Ollama"

**Solution:**
```bash
# Start Ollama server in a separate terminal
ollama serve
```

Keep this terminal running!

### "Model llama3.1 not found"

**Solution:**
```bash
ollama pull llama3.1
```

Wait for download to complete (~4GB).

### "CSV file too large"

Your dataset is >50MB. This is fine! Just use command line:
```bash
python demo.py
```

### Agent is slow

First run is always slower (model loading). Subsequent runs are faster.

To speed up:
1. Reduce `max_iterations` in `agent_setup.py` (line 60)
2. Use a smaller model: `ollama pull mistral`

### Import errors

```bash
pip install -r requirements.txt --upgrade
```

---

## 🎯 What to Show Your Professor

### 1. The Problem (30 seconds)
"Smart grids need real-time anomaly detection. Traditional rule-based systems can't explain WHY anomalies occur."

### 2. The Solution (30 seconds)  
"I built an Agentic AI system using LangChain + local Llama 3.1. It detects frequency drops AND explains root causes by analyzing weather and generation data."

### 3. Live Demo (2 minutes)

**Run Streamlit:**
```bash
streamlit run app.py
```

**Show:**
1. ✅ Load dataset → Shows anomaly count
2. ✅ Select an anomaly timestamp
3. ✅ Click "Run Analysis"
4. ✅ AI explains causation in natural language
5. ✅ Charts show correlation

### 4. Technical Deep Dive (if asked)

**Architecture:**
- Pandas for data preprocessing
- LangChain experimental agents
- Zero-shot ReAct reasoning
- Local inference (no API costs!)
- Prompt engineering for domain expertise

**Key Code:**
- `data_loader.py` - ETL pipeline
- `agent_setup.py` - LangChain configuration
- `main_analysis.py` - Business logic
- `app.py` - User interface

---

## 📊 System Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│                  Smart Grid Dataset                 │
│              (CSV with 40+ columns)                 │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
         ┌─────────────────────┐
         │   data_loader.py    │
         │  • Parse timestamps │
         │  • Detect anomalies │
         │  • Clean & sort     │
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │   agent_setup.py    │
         │  • Init Ollama LLM  │
         │  • Create DF Agent  │
         │  • Set expertise    │
         └──────────┬──────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  main_analysis.py   │
         │  • Check anomaly    │
         │  • Query agent      │
         │  • Format results   │
         └──────────┬──────────┘
                    │
            ┌───────┴───────┐
            ▼               ▼
    ┌──────────────┐  ┌──────────────┐
    │    app.py    │  │   demo.py    │
    │  (Streamlit) │  │ (CLI mode)   │
    │   Web UI     │  │   Terminal   │
    └──────────────┘  └──────────────┘
```

---

## 💡 Extension Ideas (For Extra Credit)

1. **Email Alerts**: Send notifications when anomalies detected
2. **Predictive Mode**: Use weather forecasts to predict future drops
3. **Multi-model Ensemble**: Compare Llama vs Mistral analyses
4. **Database Integration**: Store analysis results in SQLite
5. **Export Reports**: Generate PDF summaries

---

## 📚 Key Technologies Explained

| Technology | Purpose | Why It Matters |
|------------|---------|----------------|
| **LangChain** | Agent orchestration | Industry-standard AI framework |
| **Ollama** | Local LLM inference | No API costs, data privacy |
| **Pandas** | Data manipulation | Standard for data science |
| **Streamlit** | Web UI | Rapid prototyping, impressive demos |
| **Llama 3.1** | AI model | State-of-the-art open-source LLM |

---

## ✅ Final Checklist Before Demo

- [ ] Ollama is running (`ollama serve`)
- [ ] Model is downloaded (`ollama list` shows llama3.1)
- [ ] Dataset CSV is in project folder
- [ ] Dependencies installed (`pip list` shows langchain)
- [ ] Test run completed (`python test_system.py`)
- [ ] Browser open to `http://localhost:8501`

---

## 🏆 Success Criteria

Your system works if:
1. ✅ Data loads without errors
2. ✅ Agent connects to Ollama
3. ✅ Anomalies are detected (Is_Anomaly = True)
4. ✅ AI provides natural language analysis
5. ✅ Charts display correctly

---

## 📞 Quick Commands Reference

```bash
# Start system (web)
streamlit run app.py

# Start system (CLI)
python demo.py

# Run tests
python test_system.py

# Check Ollama status
ollama list

# Start Ollama server
ollama serve

# Pull new model
ollama pull mistral

# Install packages
pip install -r requirements.txt
```

---

**Ready to impress? 🚀**

Start with: `streamlit run app.py`

Good luck with your presentation! 🎓
