# NICAI – TESTING PACKET (FINAL DEMO-SAFE VERSION)

Project: NICAI – Networked Intelligence & Context Analysis Interface
Developer: Ankita Prajapati
Testing Authority: Vinayak Tiwari
Protocol: BHIV Universal Testing Protocol

---

# 1. SYSTEM OVERVIEW

NICAI is a **deterministic intelligence system** that processes real-world datasets and produces structured anomaly intelligence outputs.

NICAI does NOT execute decisions.

It generates:

* anomaly insights
* risk classification
* recommendation signals
* traceable action logs

Pipeline:

Data → Signal Conversion → Validation → Intelligence → Pattern Detection → Dashboard → Action Logging

---

# 2. REAL DATA INGESTION

Datasets used:

data/clean_weather.csv
data/clean_aqi.csv

System reads real-world environmental data and converts into signals.

---

# 3. SIGNAL GENERATION

Handled by:

samachar_input_adapter.py

Example signal:

```json
{
  "signal_id": "W_2",
  "timestamp": "2026-04-14T04:21:32",
  "latitude": 19.0760,
  "longitude": 72.8777,
  "value": 48.7,
  "dataset_id": "weather",
  "feature_type": "temperature"
}
```

---

# 4. TRACEABILITY TEST

Each signal generates deterministic `trace_id`.

Flow:

Signal → Validation → Analysis → Pattern → Dashboard → Action Log

Validation:

* trace_id must remain SAME across all layers
* trace_id must appear in logs

---

# 5. VALIDATION LAYER TESTING

File: validator.py

### Test Cases

| Case            | Input            | Expected     |
| --------------- | ---------------- | ------------ |
| Missing field   | No timestamp     | ERROR        |
| Invalid dataset | Wrong dataset_id | ERROR        |
| Wrong type      | value = string   | ERROR        |
| Valid signal    | Correct input    | VALID / FLAG |

### Expected Output

```json
{
  "status": "ERROR",
  "reason": "Missing field: timestamp",
  "trace_id": "..."
}
```

✔ System must NEVER crash

---

# 6. INTELLIGENCE ENGINE TESTING

File: sanskar_engine.py

### Test Cases

| Condition | Expected Risk |
| --------- | ------------- |
| Normal    | LOW           |
| Elevated  | MEDIUM        |
| Extreme   | HIGH          |

Example:

```json
{
  "risk_level": "HIGH",
  "anomaly_score": 0.9,
  "anomaly_type": "TEMPERATURE_SPIKE",
  "explanation": "Extreme temperature detected",
  "recommendation_signal": "eligible_for_escalation"
}
```

✔ Deterministic output (same input → same output)

---

# 7. PATTERN DETECTION TESTING

Function: analyze_patterns()

### Test Cases

| Scenario           | Expected         |
| ------------------ | ---------------- |
| No anomalies       | NO_PATTERN       |
| Few anomalies      | STABLE           |
| Multiple anomalies | REPEATED_ANOMALY |
| Cluster            | CLUSTER_ANOMALY  |

Example:

```json
{
  "pattern_id": "PATTERN_xxx",
  "anomaly_count": 5,
  "affected_zones": ["North"],
  "pattern_type": "CLUSTER_ANOMALY",
  "severity_trend": "INCREASING"
}
```

---

# 8. API ENDPOINT TESTING (LOCKED)

Allowed endpoints:

/nicai/evaluate
/dashboard
/action

### Test Cases

| Endpoint        | Test          | Expected          |
| --------------- | ------------- | ----------------- |
| /nicai/evaluate | valid signal  | structured output |
| /nicai/evaluate | invalid input | ERROR             |
| /action         | valid request | SUCCESS           |
| /dashboard      | open          | UI loads          |

✔ No unused endpoints should be tested

---

# 9. DASHBOARD TESTING

Open:

http://127.0.0.1:8000/dashboard

### Validate:

* table loads
* risk levels visible
* anomaly type shown
* explanation visible
* recommended step visible
* action button works

### Failure Case:

No data → safe message displayed

✔ Dashboard must NEVER crash

---

# 10. ACTION ROUTING TEST

Endpoint:

POST /action

### Request:

```json
{
  "trace_id": "TEST123",
  "action_type": "ESCALATE",
  "risk_level": "HIGH"
}
```

### Expected Response:

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

# 11. ACTION LOG VALIDATION

File:

logs/action_logs.json

### Verify:

* trace_id present
* action_type present
* timestamp present

✔ Entry must be created after button click

---

# 12. LOGGING SYSTEM TEST

Files:

logs/validation_logs.json
logs/anomaly_logs.json
logs/pattern_logs.json
logs/action_logs.json

### Format:

```json
{
  "trace_id": "...",
  "timestamp": "...",
  "type": "VALIDATION | ANALYSIS | PATTERN | ACTION",
  "data": {}
}
```

✔ Logs must be consistent and readable

---

# 13. FAILURE HANDLING TEST

### Test Cases

| Case           | Expected |
| -------------- | -------- |
| Empty input    | ERROR    |
| Invalid JSON   | ERROR    |
| Missing fields | ERROR    |
| Wrong types    | ERROR    |

✔ System MUST:

* never crash
* always return structured error

---

# 14. INPUT GATE TEST

Before validation:

| Case           | Expected |
| -------------- | -------- |
| Non-dict input | ERROR    |
| Empty input    | ERROR    |
| Missing keys   | ERROR    |

---

# 15. DEMO FLOW VALIDATION

Run:

python run_demo_full.py

### Expected Flow

1. Dataset load
2. Signal conversion
3. Validation
4. Intelligence output
5. Pattern detection
6. Dashboard launch
7. Action click
8. Log verification

✔ Must run WITHOUT interruption

---

# 16. SUCCESS CRITERIA

System passes if:

* No crashes
* All errors structured
* Dashboard stable
* Actions logged
* Patterns detected
* Trace IDs consistent
* Logs properly formatted

---

# 17. FINAL STATUS

NICAI is:

* Deterministic
* Traceable
* Failure-safe
* Demo-ready
* Minimal & controlled

---

# CONCLUSION

NICAI has been validated under:

BHIV Universal Testing Protocol

It is now a:

→ Stable
→ Controlled
→ Demo-safe intelligence system

Ready for final demo and evaluation
