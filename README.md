# NICAI – Networked Intelligence & Context Analysis Interface

NICAI is a **deterministic intelligence system** that converts real-world environmental data into **structured, explainable, and traceable intelligence outputs**.

It functions as a **decision-support layer**, not a decision-maker.

---

# 🚀 What NICAI Does

NICAI processes datasets (Weather, AQI) to:

* Validate incoming signals
* Detect anomalies using rule-based logic
* Identify multi-signal patterns
* Generate recommendation signals
* Provide a dashboard interface
* Maintain full traceability using `trace_id`

⚠️ NICAI does **NOT execute decisions**
It only generates **intelligence outputs**

---

# 🧠 Core Capabilities

* Deterministic system (Same Input → Same Output)
* Explainable outputs (No black-box AI)
* Multi-signal pattern detection
* Full traceability (`trace_id`)
* Crash-safe error handling
* Real-time dashboard visualization
* Action simulation (no real execution)
* Minimal API surface (demo-safe)

---

# 🏗️ System Architecture

```
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
Pattern Detection
   ↓
FastAPI Layer
   ↓
Dashboard
   ↓
Action Router (Simulation)
   ↓
Logging System
```

---

# 📂 Project Structure

```
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

---

# ▶️ How to Run (Demo Mode)

Run full system:

```
python run_demo_full.py
```

This will:

1. Load datasets
2. Convert into signals
3. Validate signals
4. Run intelligence engine
5. Detect patterns
6. Start API server

---

# 🌐 Open Dashboard

```
http://127.0.0.1:8000/dashboard
```

---

# ⚡ API Endpoints

| Endpoint          | Method     | Description   |
| ----------------- | ---------- | ------------- |
| `/dashboard`      | GET        | UI Dashboard  |
| `/action`         | POST       | Log action    |
| `/nicai/evaluate` | (Optional) | Full pipeline |

❌ No unnecessary endpoints (Demo-safe)

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

Output:

```json
{
  "signal_id": "...",
  "status": "ALLOW | FLAG | REJECT",
  "confidence_score": 0.9,
  "trace_id": "...",
  "reason": "..."
}
```

Handles:

* Missing fields
* Invalid dataset
* Wrong data types
* Empty inputs

---

# ⚙️ Intelligence Engine

Risk Mapping:

* Normal → LOW
* Elevated → MEDIUM
* Extreme → HIGH

Output:

```json
{
  "risk_level": "HIGH",
  "anomaly_type": "TEMPERATURE_SPIKE",
  "explanation": "Extreme temperature detected",
  "anomaly_score": 0.9,
  "confidence": 0.95,
  "recommendation_signal": "eligible_for_escalation"
}
```

---

# 📈 Pattern Detection

Example:

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

---

# 🧭 TANTRA Compliance

NICAI does NOT take actions.

Allowed outputs:

* `eligible_for_escalation`
* `requires_review`
* `monitor`

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
* Recommended Action
* Action Button

✔ Full traceability visible
✔ Clean UI for demo

---

# ⚡ Action Layer

**POST /action**

Output:

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

---

# 📊 Logging System

```
logs/
│── validation_logs.json
│── anomaly_logs.json
│── pattern_logs.json
│── action_logs.json
```

Format:

```json
{
  "trace_id": "...",
  "timestamp": "...",
  "type": "VALIDATION | ANALYSIS | PATTERN | ACTION",
  "data": {}
}
```

---

# 🔗 Traceability Flow

```
Signal → Validation → Analysis → Pattern → Dashboard → Action Log
```

---

# 🎯 Demo Flow

1. Run system
2. Observe signals
3. Detect anomalies
4. View pattern summary
5. Open dashboard
6. Trigger action
7. Check logs
8. Track via trace_id

---

# 🔒 Deterministic Guarantee

Same Input → Same Output

---

# 📌 Final Status

* ✅ Fully Functional
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
