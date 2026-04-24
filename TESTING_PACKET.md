# NICAI – TESTING PACKET (FINAL – TASK-COMPLIANT & DEMO SAFE)

**Project:** NICAI – Networked Intelligence & Context Analysis Interface
**Developer:** Ankita Prajapati
**Testing Protocol:** BHIV Universal Testing Protocol

---

# 1. SYSTEM EXECUTION TEST (MANDATORY)

Run full system:

```bash
python run_demo_full.py
```

### Expected Output

* ✅ Datasets loaded successfully
* ✅ Signals generated (count displayed)
* ✅ Validation completed (ALLOW / FLAG / REJECT visible)
* ✅ Intelligence processing complete (LOW / MEDIUM / HIGH)
* ✅ Pattern detection output displayed
* ✅ FastAPI server starts

Example:

```
INFO: Uvicorn running on http://127.0.0.1:8000
```

✔ Confirms **end-to-end pipeline stability**

---

# 2. REAL DATA INGESTION TEST

Datasets:

```
data/clean_weather.csv  
data/clean_aqi.csv
```

### Validation

* Data loads without error
* Signals generated successfully
* No null/corrupt entries break pipeline

✔ Confirms **real data → usable signals**

---

# 3. SIGNAL GENERATION TEST

File: `samachar_input_adapter.py`

### Expected

* Output is a **list**
* Each item is a **valid signal dictionary**
* Required fields present:

```json
{
  "signal_id": "...",
  "timestamp": "...",
  "latitude": "...",
  "longitude": "...",
  "value": "...",
  "dataset_id": "...",
  "feature_type": "..."
}
```

✔ Ensures input consistency

---

# 4. VALIDATION LAYER TEST

File: `validator.py`

### Test Cases

| Case            | Input           | Expected     |
| --------------- | --------------- | ------------ |
| Missing field   | No timestamp    | REJECT       |
| Invalid dataset | Unknown dataset | REJECT       |
| Wrong type      | value = string  | REJECT       |
| Empty input     | {}              | REJECT       |
| Valid signal    | Proper input    | ALLOW / FLAG |

### Output Format

```json
{
  "signal_id": "...",
  "status": "ALLOW | FLAG | REJECT",
  "confidence_score": 0.9,
  "trace_id": "...",
  "reason": "..."
}
```

✔ Schema validation
✔ Deterministic output
✔ Trace ID generated

---

# 5. INTELLIGENCE ENGINE TEST

File: `sanskar_engine.py`

### Expected Behavior

| Condition | Risk Level |
| --------- | ---------- |
| Normal    | LOW        |
| Elevated  | MEDIUM     |
| Extreme   | HIGH       |

### Output Format

```json
{
  "trace_id": "...",
  "risk_level": "HIGH",
  "anomaly_type": "...",
  "explanation": "...",
  "anomaly_score": 0.9,
  "confidence": 0.95,
  "recommendation_signal": "eligible_for_escalation"
}
```

✔ Rule-based
✔ No randomness
✔ Explainable

---

# 6. MULTI-SIGNAL PATTERN TEST

Function: `analyze_patterns()`

### Expected

* Detect anomaly clusters
* Count anomalies correctly
* Identify affected zones
* Generate deterministic `pattern_id`

### Output Format

```json
{
  "pattern_id": "PATTERN_xxx",
  "anomaly_count": 15,
  "affected_zones": ["North", "Central", "South"],
  "pattern_type": "CLUSTER_ANOMALY",
  "pattern_summary": "...",
  "severity_trend": "INCREASING"
}
```

✔ Matches dashboard
✔ Based on real processed outputs

---

# 7. MULTI-SIGNAL SCENARIO PROOF (MANDATORY)

System must demonstrate:

| Scenario             | Expected    |
| -------------------- | ----------- |
| Single signal        | LOW risk    |
| Mixed signals        | MEDIUM risk |
| Correlated anomalies | HIGH risk   |

✔ Visible in:

* Dashboard
* Logs
* Explanation

---

# 8. DASHBOARD TEST

Open:

```
http://127.0.0.1:8000/dashboard
```

### Validate

* ✅ Data visible
* ✅ Trace ID shown
* ✅ Validation status visible
* ✅ Risk level displayed
* ✅ Confidence score visible
* ✅ Explanation readable
* ✅ Recommended step visible
* ✅ Action buttons working
* ❌ No crash / blank screen

✔ Confirms UI stability

---

# 9. ACTION ROUTING TEST (API + UI)

## Method 1 — Swagger UI

Open:

```
http://127.0.0.1:8000/docs
```

### Endpoint

```
POST /action
```

### Input

```json
{
  "trace_id": "TEST123",
  "action_type": "eligible_for_escalation",
  "risk_level": "HIGH"
}
```

### Expected Output

```json
{
  "status": "SUCCESS",
  "action": {
    "trace_id": "TEST123",
    "action_type": "eligible_for_escalation",
    "target_role": "authority",
    "timestamp": "...",
    "context": {}
  }
}
```

---

## Method 2 — Dashboard

* Click any action button
* Page reloads
* Action logged

✔ Confirms UI → API connection

---

# 10. LOGGING SYSTEM TEST

Files:

```
logs/validation_logs.json  
logs/anomaly_logs.json  
logs/pattern_logs.json  
logs/action_logs.json  
```

### Each log entry:

```json
{
  "trace_id": "...",
  "timestamp": "...",
  "type": "VALIDATION | ANALYSIS | PATTERN | ACTION",
  "data": {}
}
```

✔ Logs auto-created
✔ No manual file creation needed

---

# 11. TRACEABILITY TEST (CRITICAL)

Pick one signal and verify same `trace_id` exists in:

* validation_logs.json
* anomaly_logs.json
* pattern_logs.json
* action_logs.json

✔ Confirms full pipeline linkage

---

# 12. FAILURE HANDLING TEST

### Test Cases

| Case            | Expected |
| --------------- | -------- |
| Empty input     | ERROR    |
| Invalid JSON    | ERROR    |
| Missing fields  | REJECT   |
| Wrong data type | REJECT   |

### System MUST

* ❌ Never crash
* ✅ Always return structured error
* ✅ Maintain traceability

---

# 13. DEMO FLOW VALIDATION

Run:

```bash
python run_demo_full.py
```

### Expected Flow

1. Dataset loading
2. Signal conversion
3. Validation
4. Intelligence output
5. Pattern detection
6. Dashboard launch
7. Action trigger
8. Log verification

✔ Smooth execution
✔ No manual fixes

---

# 14. FINAL SUCCESS CRITERIA

System passes if:

* ✅ End-to-end execution successful
* ✅ No crashes
* ✅ Dashboard functional
* ✅ Actions logged correctly
* ✅ Patterns detected accurately
* ✅ Trace IDs consistent
* ✅ Errors structured
* ✅ Multi-signal scenarios visible

---

# FINAL STATUS

NICAI is:

* Deterministic
* Fully traceable
* Failure-safe
* Dashboard-enabled
* TANTRA-compliant
* Demo-ready

---

# CONCLUSION

NICAI successfully passes:

* End-to-end execution test
* Validation & intelligence testing
* Multi-signal pattern verification
* Action routing validation (API + UI)
* Logging & traceability checks

---

🚀 **System is fully tested, stable, and ready for final evaluation**
