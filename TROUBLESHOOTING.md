# 🔧 Troubleshooting Guide - Smart Grid AI Operator

## Common Issues and Solutions

---

## 🚫 Issue 1: "Cannot connect to Ollama" / "Connection refused"

### Symptoms
```
Error: Could not connect to Ollama
Connection refused at localhost:11434
```

### Solution
**Ollama server is not running.**

```bash
# Start Ollama server in a separate terminal/PowerShell
ollama serve
```

**Keep this terminal open!** The server must run in the background.

### Verification
```bash
# In another terminal, test connection:
ollama list
# Should show available models
```

---

## 🚫 Issue 2: "Model llama3.1 not found"

### Symptoms
```
Error: model 'llama3.1' not found
```

### Solution
**Model not downloaded yet.**

```bash
# Download Llama 3.1 (one-time, ~4GB)
ollama pull llama3.1

# Wait for download to complete
# Then verify:
ollama list
```

### Alternative Models
If Llama 3.1 is too large or slow:

```bash
# Smaller, faster options:
ollama pull mistral        # 4GB, good performance
ollama pull llama2         # 3.8GB, older but stable
ollama pull phi            # 1.6GB, very fast

# Then edit agent_setup.py line 23:
# llm = ChatOllama(model="mistral")
```

---

## 🚫 Issue 3: "ModuleNotFoundError: No module named 'langchain'"

### Symptoms
```
ModuleNotFoundError: No module named 'langchain'
ModuleNotFoundError: No module named 'streamlit'
```

### Solution
**Dependencies not installed.**

```bash
# Install all requirements
pip install -r requirements.txt

# If that fails, install individually:
pip install pandas langchain langchain-experimental langchain-ollama streamlit plotly
```

### Check Installation
```bash
# Verify packages are installed:
pip list | findstr langchain
pip list | findstr streamlit
```

---

## 🚫 Issue 4: CSV File Not Found

### Symptoms
```
FileNotFoundError: [Errno 2] No such file or directory: 'smart_city_energy_dataset.csv'
```

### Solution
**CSV file not in correct location.**

```bash
# Check current directory:
cd c:\Users\kbllm\Desktop\module\ecogridiea

# Verify CSV exists:
dir smart_city_energy_dataset.csv

# If missing, provide full path in code:
df = load_grid_data('c:/Users/kbllm/Desktop/module/ecogridiea/smart_city_energy_dataset.csv')
```

---

## 🚫 Issue 5: "CSV File Too Large to Read in VS Code"

### Symptoms
```
Files above 50MB cannot be synchronized with extensions
```

### Solution
**This is just a VS Code warning - the file still works!**

Your Python scripts can read the 57MB file just fine:
```bash
# Test it:
python data_loader.py
# Should load successfully
```

VS Code limits file display, not file access.

---

## 🚫 Issue 6: Agent Analysis is Very Slow (>2 minutes)

### Symptoms
Agent takes 2-5 minutes to analyze, or times out.

### Solutions

**Option 1: Reduce Agent Iterations**

Edit `agent_setup.py` line 60:
```python
max_iterations=15,  # Change to: max_iterations=8
```

**Option 2: Use Faster Model**
```bash
ollama pull mistral
```

Edit `agent_setup.py`:
```python
llm = ChatOllama(model="mistral", temperature=0.0)
```

**Option 3: Simplify Query**

Edit `main_analysis.py` line 64-100, reduce the query detail.

---

## 🚫 Issue 7: Streamlit Shows "Waiting for data..."

### Symptoms
UI loads but sidebar shows "⏳ Waiting for data..."

### Solution
**Need to click "Load & Initialize System" button.**

1. Open sidebar (left side)
2. Check "Use default file path"
3. Click "🔄 Load & Initialize System"
4. Wait 30-60 seconds for agent initialization

---

## 🚫 Issue 8: "No anomalies detected in the dataset"

### Symptoms
System loads but finds 0 anomalies.

### Causes & Solutions

**Cause 1: Threshold too low**

Edit `data_loader.py` line 31:
```python
# Current threshold:
df['Is_Anomaly'] = df['Grid Frequency (Hz)'] < 49.8

# Try more permissive:
df['Is_Anomaly'] = df['Grid Frequency (Hz)'] < 50.0
```

**Cause 2: Column name mismatch**

Check your CSV column names:
```python
import pandas as pd
df = pd.read_csv('smart_city_energy_dataset.csv')
print(df.columns.tolist())
```

Update `data_loader.py` with correct column name.

---

## 🚫 Issue 9: Timestamp Parsing Error

### Symptoms
```
ValueError: time data '...' does not match format
```

### Solution
**Timestamp format mismatch.**

Edit `data_loader.py` line 20:
```python
# If timestamps like "2021-01-01 00:00:00":
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# If different format, specify:
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M:%S')

# Or let pandas infer:
df['Timestamp'] = pd.to_datetime(df['Timestamp'], infer_datetime_format=True)
```

---

## 🚫 Issue 10: Plotly Charts Not Displaying

### Symptoms
Streamlit shows blank space where charts should be.

### Solution
```bash
# Reinstall plotly
pip install plotly --upgrade

# Restart Streamlit
# Press Ctrl+C in terminal
# Then: streamlit run app.py
```

---

## 🚫 Issue 11: Windows PowerShell Execution Policy Error

### Symptoms
```
cannot be loaded because running scripts is disabled on this system
```

### Solution
```powershell
# Allow scripts for current user:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run Python directly:
python -m streamlit run app.py
```

---

## 🚫 Issue 12: "Agent parsing error" in Terminal Output

### Symptoms
Agent shows errors but eventually produces output anyway.

### Solution
**This is normal!** LangChain agents sometimes make parsing mistakes and self-correct.

If you want cleaner output, edit `agent_setup.py` line 56:
```python
verbose=True,  # Change to: verbose=False
```

This hides intermediate reasoning steps.

---

## 🚫 Issue 13: Memory Error with Large Dataset

### Symptoms
```
MemoryError: Unable to allocate array
```

### Solution

**Option 1: Sample Data**

Edit `data_loader.py`, add after line 16:
```python
# Load only first 10,000 rows for testing:
df = pd.read_csv(csv_path, nrows=10000)
```

**Option 2: Filter Date Range**

```python
# Load and filter to specific month:
df = pd.read_csv(csv_path)
df = df[df['Timestamp'].str.startswith('2021-01')]
```

---

## 🚫 Issue 14: Ollama Not Found (Windows)

### Symptoms
```
'ollama' is not recognized as an internal or external command
```

### Solution
**Ollama not installed or not in PATH.**

1. Download from https://ollama.ai
2. Run the installer
3. Restart PowerShell/Command Prompt
4. Test: `ollama --version`

If still not working:
```powershell
# Find Ollama manually:
Get-ChildItem -Path "C:\Users\$env:USERNAME\AppData\Local\Programs" -Filter "ollama.exe" -Recurse

# Add to PATH or use full path:
& "C:\Users\...\ollama.exe" serve
```

---

## 🚫 Issue 15: Port 8501 Already in Use (Streamlit)

### Symptoms
```
OSError: [Errno 98] Address already in use
```

### Solution
**Another Streamlit instance is running.**

```bash
# Option 1: Kill the process
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID_NUMBER> /F

# Option 2: Use different port
streamlit run app.py --server.port 8502
```

---

## 🔍 General Debugging Tips

### 1. Check Python Version
```bash
python --version
# Should be 3.10 or higher
```

### 2. Test Components Individually

```python
# Test 1: Data loading only
python data_loader.py

# Test 2: Agent setup (requires Ollama)
python -c "from agent_setup import initialize_llm; llm = initialize_llm(); print('✓ LLM works')"

# Test 3: Full system
python test_system.py
```

### 3. Enable Verbose Mode

Edit your scripts to add debug prints:
```python
print(f"Debug: df shape = {df.shape}")
print(f"Debug: columns = {df.columns.tolist()}")
```

### 4. Check Logs

```bash
# Ollama logs:
ollama serve  # Watch output for errors

# Streamlit logs:
# Already shown in terminal

# Python errors:
python app.py 2> errors.log
```

---

## 📞 Quick Diagnostic Commands

Run these to check system health:

```powershell
# Check Python
python --version

# Check pip packages
pip list | findstr -i "langchain streamlit pandas"

# Check Ollama
ollama list
ollama ps  # Shows running models

# Check file
Test-Path "smart_city_energy_dataset.csv"

# Check ports
netstat -ano | findstr "8501 11434"
```

---

## ✅ System Health Checklist

Before running the system:

- [ ] Python 3.10+ installed (`python --version`)
- [ ] All packages installed (`pip list`)
- [ ] Ollama installed (`ollama --version`)
- [ ] Ollama server running (`ollama ps`)
- [ ] Llama 3.1 downloaded (`ollama list`)
- [ ] CSV file exists (`Test-Path "smart_city_energy_dataset.csv"`)
- [ ] No port conflicts (8501, 11434)
- [ ] Sufficient disk space (~5GB for model)
- [ ] Sufficient RAM (4GB+ recommended)

---

## 🆘 Still Not Working?

### Last Resort Solutions

1. **Complete Reinstall**
```bash
# Uninstall everything
pip uninstall langchain langchain-experimental langchain-ollama streamlit pandas plotly -y

# Clean install
pip install -r requirements.txt --no-cache-dir

# Restart Ollama
taskkill /IM ollama.exe /F
ollama serve
```

2. **Try Command Line Demo**
```bash
# Bypass Streamlit
python demo.py
```

3. **Manual Test**
```python
# Minimal test script
import pandas as pd
from langchain_ollama import ChatOllama

# Test 1: Pandas
df = pd.read_csv('smart_city_energy_dataset.csv', nrows=100)
print(f"✓ Loaded {len(df)} rows")

# Test 2: Ollama
llm = ChatOllama(model="llama3.1")
response = llm.invoke("Say 'test successful'")
print(f"✓ LLM responded: {response}")
```

---

## 📧 Getting Help

If all else fails:

1. **Check Python environment**: `pip list > installed_packages.txt`
2. **Check Ollama status**: `ollama list`
3. **Run test script**: `python test_system.py`
4. **Copy error messages** (full traceback)
5. **Check system requirements**: Windows 10+, 4GB RAM, 10GB disk

---

**Most issues are due to:**
1. Ollama not running (50%)
2. Missing packages (30%)
3. File path issues (10%)
4. Other (10%)

**Start with the basics: Is Ollama running? Are packages installed?**

Good luck! 🚀
