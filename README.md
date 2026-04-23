# NICAI – Networked Intelligence & Context Analysis Interface

NICAI is a **deterministic intelligence system** that converts real-world environmental data into **structured, explainable, and traceable intelligence outputs**.

It acts as a **decision-support layer**, not a decision-maker.

---

# 🚀 What NICAI Does

NICAI processes datasets (weather, AQI) to:

* Validate incoming signals
* Detect anomalies using rule-based logic
* Identify multi-signal patterns
* Generate recommendation signals
* Provide a dashboard interface
* Maintain full traceability using `trace_id`

⚠️ NICAI does NOT take decisions
It ONLY prepares **intelligence outputs**

---

# 🧠 Core Capabilities

* Deterministic system (same input → same output)
* Explainable outputs (no black-box AI)
* Multi-signal pattern detection
* Full traceability (`trace_id`)
* Crash-free failure handling
* Dashboard visualization
* Action simulation (no execution)
* Minimal API surface (demo-safe)

---

# 🏗 Final Architecture

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

---

# 📂 Final Project Structure

nicai_system/

main.py
validator.py
sanskar_engine.py
samachar_input_adapter.py
error_handler.py

run_demo_full.py

logs/
data/

README.md
REVIEW_PACKET.md
TESTING_PACKET.md

---

# ▶️ How to Run (Demo Mode)

Run full system:

python run_demo_full.py

This will:

1. Load dataset
2. Convert signals
3. Run validation
4. Run intelligence
5. Detect patterns
6. Start API server

---

Open dashboard:

http://127.0.0.1:8000/dashboard

---

# ⚡ Final API Endpoints (Locked)

/nicai/evaluate → Full pipeline
/dashboard → UI dashboard
/action → Action logging

❌ No extra endpoints (demo-safe)

---

# 📥 Input Signal Format

{
"signal_id": "W_2",
"timestamp": "2026-04-14T04:21:32",
"latitude": 19.07,
"longitude": 72.87,
"value": 48.7,
"dataset_id": "weather",
"feature_type": "temperature"
}

---

# 🔍 Validation Layer

Output:

{
"signal_id": "...",
"status": "VALID | FLAG | ERROR",
"confidence_score": 0.9,
"trace_id": "...",
"reason": "..."
}

Handles:

* missing fields
* invalid dataset
* wrong types
* empty input

---

# ⚙️ Intelligence Engine

Risk mapping:

Normal → LOW
Elevated → MEDIUM
Extreme → HIGH

Output:

{
"risk_level": "HIGH",
"anomaly_type": "TEMPERATURE_SPIKE",
"explanation": "Extreme temperature detected",
"anomaly_score": 0.9,
"recommendation_signal": "eligible_for_escalation"
}

---

# 📈 Pattern Detection

Example:

{
"pattern_id": "PATTERN_xxx",
"anomaly_count": 5,
"affected_zones": ["North"],
"pattern_type": "CLUSTER_ANOMALY",
"severity_trend": "INCREASING"
}

---

# 🧭 TANTRA Compliance

NICAI does NOT execute decisions.

Allowed outputs:

* eligible_for_escalation
* requires_review
* monitor

---

# 🖥 Dashboard

Shows:

* ID
* Risk
* Type
* Explanation
* Recommended Step
* Action button

Fail-safe:

No data → safe fallback

---

# ⚡ Action Layer

POST /action

Output:

{
"status": "SUCCESS",
"action": {
"trace_id": "TRACE_xxx",
"action_type": "ESCALATE",
"target_role": "authority",
"timestamp": "...",
"context": {}
}
}

---

# 📊 Logging System

logs/

validation_logs.json
anomaly_logs.json
pattern_logs.json
action_logs.json

Format:

{
"trace_id": "...",
"timestamp": "...",
"type": "VALIDATION | ANALYSIS | PATTERN | ACTION",
"data": {}
}

---

# 🔗 Traceability

Signal → Validation → Analysis → Pattern → Dashboard → Action Log

---

# 🎯 Demo Flow

1. Run system
2. Show signals
3. Show anomalies
4. Show pattern
5. Open dashboard
6. Click action
7. Show action_logs.json
8. Show trace_id

---

# 🔒 Deterministic Guarantee

Same Input → Same Output

---

# 📌 Final Status

* Crash-free
* Demo-safe
* Deterministic
* Fully traceable
* Minimal endpoints
* Action visibility ready

---

# 👩‍💻 Developer

Ankita Prajapati
NICAI – System Integration & Stabilization

---

# 📌 Final Note

NICAI is not about automation.

It is about:

clean intelligence, clear reasoning, and controlled decisions

