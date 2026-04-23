# NICAI – TESTING PACKET (FINAL – DEMO SAFE)

Project: NICAI – Networked Intelligence & Context Analysis Interface  
Developer: Ankita Prajapati  
Testing Authority: Vinayak Tiwari  
Testing Protocol: BHIV Universal Testing Protocol  

---

# 1. SYSTEM EXECUTION TEST (MANDATORY)

Run full system:

```bash
python run_demo_full.py
```

### Expected Output:

- ✅ Datasets loaded successfully  
- ✅ Signals generated (count visible)  
- ✅ Validation + Intelligence processing complete  
- ✅ Risk distribution shown (LOW / MEDIUM / HIGH)  
- ✅ Pattern detection output shown  
- ✅ FastAPI server starts  

Example:

```
INFO: Uvicorn running on http://127.0.0.1:8000
```

👉 Confirms **end-to-end pipeline stability**

---

# 2. REAL DATA INGESTION TEST

Datasets:

```
data/clean_weather.csv  
data/clean_aqi.csv
```

### Validation:

- Data loads without error  
- Signals successfully generated  

---

# 3. SIGNAL GENERATION TEST

File: `samachar_input_adapter.py`

### Expected:

- Output is a list  
- Each item is a valid signal dictionary  

---

# 4. VALIDATION LAYER TEST

File: `validator.py`

### Test Cases

| Case | Input | Expected |
|------|------|---------|
| Missing field | No timestamp | ERROR |
| Invalid dataset | Unknown dataset_id | ERROR |
| Wrong type | value = string | ERROR |
| Empty input | {} | ERROR |
| Valid signal | Proper input | VALID / FLAG |

### Expected Error Format

```json
{
  "status": "ERROR",
  "reason": "...",
  "trace_id": "..."
}
```

---

# 5. INTELLIGENCE ENGINE TEST

File: `sanskar_engine.py`

### Expected Behavior

| Condition | Output |
|----------|--------|
| Normal | LOW |
| Elevated | MEDIUM |
| Extreme | HIGH |

---

# 6. PATTERN DETECTION TEST

Function: `analyze_patterns()`

### Expected:

- Detect anomaly clusters  
- Return structured pattern output  

---

# 7. DASHBOARD TEST

Open:

```
http://127.0.0.1:8000/dashboard
```

### Validate:

- ✅ Data visible  
- ✅ Risk levels shown  
- ✅ Recommended step visible  
- ✅ Action buttons clickable  
- ❌ No crash  

---

# 8. ACTION ROUTING TEST (UPDATED – API + UI)

## Method 1 — Swagger UI (MANDATORY)

### Step 1: Open API Docs

```
http://127.0.0.1:8000/docs
```

### Step 2: Find Endpoint

```
POST /action
```

### Step 3: Click "Try it out"

### Step 4: Paste Input

```json
{
  "trace_id": "TEST123",
  "action_type": "ESCALATE",
  "risk_level": "HIGH"
}
```

### Step 5: Click Execute

### Expected Output

```json
{
  "status": "SUCCESS",
  "action": {
    "trace_id": "TEST123",
    "action_type": "ESCALATE",
    "target_role": "authority",
    "timestamp": "...",
    "context": {}
  }
}
```

---

## Method 2 — Dashboard Action Button

- Click any action button  
- Page reloads  
- Action gets logged  

---

## Verify Action Logs

Open:

```
logs/action_logs.json
```

Check:

- trace_id  
- action_type  
- timestamp  

---

# 9. LOGGING SYSTEM TEST

Files:

```
logs/validation_logs.json  
logs/anomaly_logs.json  
logs/pattern_logs.json  
logs/action_logs.json  
```

### Each log entry must contain:

```json
{
  "trace_id": "...",
  "timestamp": "...",
  "type": "...",
  "data": {}
}
```

---

# 10. FAILURE HANDLING TEST

### Test Cases

| Case | Expected |
|------|---------|
| Empty input | ERROR |
| Invalid JSON | ERROR |
| Missing fields | ERROR |
| Wrong data type | ERROR |

### System MUST:

- ❌ Never crash  
- ✅ Always return structured error  

---

# 11. TRACEABILITY TEST

Pick one signal and verify same `trace_id` exists in:

- validation_logs.json  
- anomaly_logs.json  
- pattern_logs.json  
- action_logs.json  

---

# 12. DEMO FLOW VALIDATION

Run:

```bash
python run_demo_full.py
```

### Expected Flow:

1. Dataset load  
2. Signal conversion  
3. Validation  
4. Intelligence output  
5. Pattern detection  
6. Dashboard launch  
7. Action trigger  
8. Log verification  

---

# 13. FINAL SUCCESS CRITERIA

System passes if:

- ✅ End-to-end run successful  
- ✅ No crashes  
- ✅ Dashboard working  
- ✅ Actions logged  
- ✅ Patterns detected  
- ✅ Trace IDs consistent  
- ✅ Errors structured  

---

# FINAL STATUS

NICAI is:

- Deterministic  
- Traceable  
- Failure-safe  
- Demo-ready  
- TANTRA-aligned  

---

# CONCLUSION

NICAI successfully passes:

- End-to-end execution test  
- Failure handling validation  
- Action routing verification (API + UI)  
- Dashboard stability test  

System is now **fully demo-safe and ready for evaluation**.
