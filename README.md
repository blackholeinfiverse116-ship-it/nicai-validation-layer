# NICAI – Networked Intelligence & Context Analysis Interface

NICAI is a **deterministic intelligence system** that converts real-world environmental data into **structured, explainable, and traceable intelligence outputs**.

It acts as a **decision-support layer**, not a decision-maker.

---

# 🚀 What NICAI Does

NICAI processes real datasets (Weather, AQI) to:

* Validate incoming signals
* Detect anomalies using rule-based logic
* Identify multi-signal patterns
* Generate recommendation signals
* Provide a dashboard interface
* Maintain full traceability using `trace_id`

⚠️ NICAI does **NOT execute decisions**
It only produces **intelligence outputs**

---

# 🧠 Core Capabilities

* Deterministic system (**Same Input → Same Output**)
* Explainable outputs (**No black-box AI**)
* Multi-signal pattern detection
* End-to-end traceability (`trace_id`)
* Crash-safe failure handling
* Real-time dashboard visualization
* Action simulation (no execution)
* Minimal API surface (demo-safe)

---

# 🏗️ Final System Architecture (LOCKED)

```text
Dataset
   ↓
Samachar Input Adapter
   ↓
Signal Conversion
   ↓
Validation Layer
   ↓
Sanskar Intelligence Engine
   ↓
Multi-Signal Pattern Analysis
   ↓
FastAPI Layer
   ↓
Dashboard
   ↓
Action Router (Simulation)
   ↓
Logging System
```

✔ No shortcuts
✔ No bypass
✔ Fully deterministic pipeline

---

# 📂 Project Structure

```text
nicai_system/

│── main.py
│── validator.py
│── sanskar_engine.py
│── samachar_input_adapter.py
│── dataset_registry.py
│── utils.py
│── error_handler.py

│── run_demo_full.py

│── logs/
│── data/

│── README.md
│── REVIEW_PACKET.md
│── TESTING_PACKET.md
```

✔ Clean, unified, demo-safe structure

---

# ▶️ How to Run (Demo Mode)

Run full system:

```bash
python run_demo_full.py
```

### This will:

1. Load datasets
2. Convert into signals
3. Validate signals
4. Run intelligence engine
5. Detect patterns
6. Start FastAPI server

---

# 🌐 Open Dashboard

```bash
http://127.0.0.1:8000/dashboard
```

---

# ⚡ API Endpoints

| Endpoint          | Method | Description         |
| ----------------- | ------ | ------------------- |
| `/dashboard`      | GET    | UI Dashboard        |
| `/action`         | POST   | Action logging      |
| `/nicai/evaluate` | POST   | (Optional) Pipeline |

✔ Minimal endpoints → lower demo risk

---

# 📥 Input Signal Format

```json
{
  "signal_id": "W_2",
  "timestamp": "2026-04-14T04:21:32",
  "latitude": 19.07,
  "longitude": 72.87,
  "value": 48.7,
  "dataset_id": "weather",
  "feature_type": "temperature"
}
```

---

# 🔍 Validation Layer

### Output:

```json
{
  "signal_id": "...",
  "status": "ALLOW | FLAG | REJECT",
  "confidence_score": 0.9,
  "trace_id": "...",
  "reason": "..."
}
```

### Handles:

* Missing fields
* Invalid dataset
* Wrong data types
* Empty input

✔ Deterministic
✔ Crash-free

---

# ⚙️ Intelligence Engine (Sanskar Engine)

### Risk Mapping:

* Normal → LOW
* Elevated → MEDIUM
* Extreme → HIGH

### Output:

```json
{
  "trace_id": "...",
  "risk_level": "HIGH",
  "anomaly_type": "TEMPERATURE_SPIKE",
  "explanation": "Extreme temperature detected",
  "anomaly_score": 0.9,
  "confidence": 0.95,
  "recommendation_signal": "eligible_for_escalation"
}
```

✔ Explainable
✔ Rule-based
✔ Deterministic

---

# 📈 Multi-Signal Pattern Detection

### Example Output:

```json
{
  "pattern_id": "PATTERN_xxx",
  "anomaly_count": 15,
  "affected_zones": ["North", "Central", "South"],
  "pattern_type": "CLUSTER_ANOMALY",
  "severity_trend": "INCREASING",
  "pattern_summary": "Anomalies concentrated in North"
}
```

✔ Uses real processed signals
✔ Detects clusters & trends

---

# 🧭 TANTRA Compliance

NICAI does NOT take actions.

### Allowed Outputs:

* `eligible_for_escalation`
* `requires_review`
* `monitor`

❌ No direct execution
❌ No automation

---

# 🖥️ Dashboard Features

Displays:

* Signal ID
* Trace ID
* Validation Status
* Risk Level
* Confidence Score
* Anomaly Type
* Explanation
* Recommended Step
* Action Button

✔ Fully traceable
✔ Clean & readable UI
✔ Demo-safe

---

# ⚡ Action Layer (Simulation)

**Endpoint:** `POST /action`

### Output:

```json
{
  "status": "SUCCESS",
  "action": {
    "trace_id": "TRACE_xxx",
    "action_type": "eligible_for_escalation",
    "target_role": "authority",
    "timestamp": "...",
    "context": {}
  }
}
```

✔ Logged
✔ Traceable
✔ Non-executable

---

# 📊 Logging System

```text
logs/

│── validation_logs.json
│── anomaly_logs.json
│── pattern_logs.json
│── action_logs.json
```

### Format:

```json
{
  "trace_id": "...",
  "timestamp": "...",
  "type": "VALIDATION | ANALYSIS | PATTERN | ACTION",
  "data": {}
}
```

✔ Auto-generated
✔ No manual setup required

---

# 🔗 Traceability Flow

```text
Signal → Validation → Analysis → Pattern → Dashboard → Action Log
```

✔ Same `trace_id` across all layers
✔ Full auditability

---

# 🎯 Demo Flow

1. Run system (`run_demo_full.py`)
2. Show dataset ingestion
3. Show signal generation
4. Show validation + intelligence
5. Show pattern detection
6. Open dashboard
7. Trigger action
8. Show logs
9. Verify trace_id

✔ Stable & repeatable demo

---

# 🔒 Deterministic Guarantee

```text
Same Input → Same Output
```

✔ No randomness
✔ Fixed rules
✔ Consistent outputs

---

# 📌 Final Status

* ✅ Fully Integrated
* ✅ Crash-Free
* ✅ Deterministic
* ✅ Traceable
* ✅ Minimal & Clean
* ✅ Demo-Ready

---

# 👩‍💻 Developer

**Ankita Prajapati**
NICAI – System Integration & Stabilization

---

# 📌 Final Note

NICAI is not about automation.

It is about:

> **Clean intelligence, clear reasoning, and controlled decision support.**
