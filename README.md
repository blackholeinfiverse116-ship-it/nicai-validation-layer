# NICAI Observability & Domain Data Integrity Layer

This project implements the **NICAI Domain Data Integrity and Observability Layer**.  
The system validates incoming signals and ensures they are **clean, traceable, observable, and ready for downstream intelligence systems**.

The validation layer performs **data integrity checks without enforcing decisions or blocking system execution**.

---

# Project Purpose

The purpose of this project is to create a **clean validation boundary inside the NICAI intelligence pipeline**.

The system ensures that:

• incoming signals follow a strict schema  
• datasets are verified through the dataset registry  
• signals are traceable through unique trace identifiers  
• validation artifacts are stored for memory systems  
• telemetry metrics are emitted for system observability  

The validation layer prepares **trusted signals for analytics, agent selection, and contract systems**.

---

# System Architecture

```
SUM-SCRIPT / Samachar (Raw Signals)
        ↓
NICAI Validation Layer (This System)
        ↓
Bucket (Memory Layer)
        ↓
InsightFlow (Observability)
        ↓
Sanskar (Analytics)
        ↓
Chayan (Agent Selection)
        ↓
Sūtradhāra (Contract Builder)
        ↓
RAJYA / SAARTHI Systems
```

This layer acts as a **domain data integrity boundary** in the intelligence pipeline.

---

# Key Features

• domain-level signal validation  
• dataset registry verification  
• batch-safe signal processing  
• trace ID generation using UUID  
• validation artifact emission to Bucket  
• telemetry emission for observability  
• strict validation output contract  
• FastAPI-based validation API  

---

# Validation Data Contract

The system enforces a strict validation schema before forwarding signals to downstream systems.

### Required Fields

• `signal_id`  
• `timestamp`  
• `latitude`  
• `longitude`  
• `feature_type`  
• `value`  
• `dataset_id`

This ensures that analytics systems receive **normalized and structured signals**.

---

# Validation Output Format

Each validated signal produces a structured validation result:

```
{
 "signal_id": "...",
 "status": "ALLOW / FLAG / REJECT",
 "confidence_score": ...,
 "trace_id": "...",
 "reason": "..."
}
```

This output is designed for **analytics, monitoring, and downstream integration**.

---

# Batch Processing

The validation API supports **multiple signals in a single request**.

### Behavior

• each signal is processed independently  
• REJECT signals do not stop batch execution  
• results are returned for all signals  

### Example Response

```
{
 "results": [
   { "signal_id": "SIG100", "status": "ALLOW" },
   { "signal_id": "SIG101", "status": "FLAG" },
   { "signal_id": "SIG102", "status": "REJECT" }
 ]
}
```

---

# Trace Continuity

Each validated signal receives a unique **trace_id**.

Example:

```
trace_id: 428a70e2-bf49-4a70-8f14-cc1c14b8cd24
```

This identifier allows signals to be **tracked across the intelligence pipeline**.

---

# Bucket Artifact Emission

For every validated signal, the system generates a **Bucket artifact** for the memory layer.

Example artifact:

```
{
 "trace_id": "...",
 "signal_id": "...",
 "status": "...",
 "confidence_score": ...,
 "reason": "...",
 "timestamp": "...",
 "layer": "NICAI_VALIDATION"
}
```

Artifacts are stored in:

```
bucket_artifacts.jsonl
```

Purpose:

• traceability  
• system lineage tracking  
• memory layer compatibility

---

# Telemetry & Observability

The system emits telemetry records for **system monitoring and analytics**.

Telemetry format:

```
{
 "trace_id": "...",
 "dataset_id": "...",
 "status": "...",
 "confidence_score": ...,
 "timestamp": "..."
}
```

Telemetry records are stored in:

```
telemetry.log
```

Metrics tracked include:

• total signals processed  
• reject rate  
• flag rate  
• dataset mismatch rate  
• confidence score distribution  

---

# Project Structure

```
nicai_validation_layer
│
├── main.py
├── validator.py
├── dataset_registry.py
├── schemas.py
├── utils.py
├── bucket_emitter.py
├── telemetry_emitter.py
├── schema.json
├── datasets.json
├── sample_signals.json
├── test_validation.py
├── bucket_artifacts.jsonl
├── telemetry.log
├── REVIEW_PACKET.md
└── README.md
```

---

# How to Run the Project

## 1 Install Dependencies

```
pip install fastapi uvicorn
```

---

## 2 Run Validation Tests

```
python test_validation.py
```

This script tests:

• valid signals  
• FLAG signals  
• REJECT signals  
• malformed inputs  
• batch validation

---

## 3 Start the Validation API

```
uvicorn main:app --reload
```

---

## 4 Open API Documentation

Open in browser:

```
http://127.0.0.1:8000/docs
```

Use Swagger UI to test the `/validate` endpoint.

---

# Example Signal Input

```
{
 "signal_id": "SIG500",
 "timestamp": "2026-03-10T10:00:00Z",
 "latitude": 19.07,
 "longitude": 72.87,
 "feature_type": "weather",
 "value": 34,
 "dataset_id": "DS01"
}
```

---

# Example Validation Output

```
{
 "signal_id": "SIG500",
 "status": "ALLOW",
 "confidence_score": 0.92,
 "trace_id": "generated_uuid",
 "reason": "valid signal"
}
```

---

# Failure Handling

The system safely handles:

• missing required fields  
• malformed input signals  
• unregistered datasets  
• inactive datasets  
• emitter failures  

The system returns **structured responses without crashing or stopping batch execution**.

---

# Testing

Testing is performed using:

• `test_validation.py`  
• FastAPI `/validate` endpoint  

Test scenarios include:

• valid signals  
• inactive dataset signals  
• missing field signals  
• malformed inputs  
• mixed batch signals  

All outputs are **deterministic and batch-safe**.

---

# Summary

This project implements a **fully observable domain data integrity layer** for NICAI.

The system guarantees:

• schema-safe validation  
• batch-safe signal processing  
• traceable validation artifacts  
• telemetry-based observability  
• compatibility with downstream intelligence systems  

The validation layer ensures that only **trusted, structured, and traceable signals** enter the intelligence pipeline.
