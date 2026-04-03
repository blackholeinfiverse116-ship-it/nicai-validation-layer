# NICAI Domain Data Integrity Validation Layer

This project implements a **domain-level validation layer** for the NICAI intelligence pipeline.
The system ensures that incoming signals are validated, normalized, and prepared for downstream analytics and simulation systems.

The validation layer processes signals without enforcing decisions or controlling pipeline execution.

---

## Project Purpose

The objective of this project is to create a **clean data integrity boundary** between raw signal ingestion and downstream intelligence systems.

The validation layer:

• validates signal schema
• checks dataset registry status
• assigns validation status (ALLOW / FLAG / REJECT)
• generates trace identifiers for signal tracking
• supports batch-safe signal processing
• produces structured validation outputs for analytics systems

---

## System Architecture

Samachar (Raw Signals)
↓
Validation Layer (This System)
↓
Sanskar (Analytics Layer)
↓
Mitra (Decision Systems)
↓
UI and Simulation Systems

The validation layer ensures that only **clean and trusted signals** reach downstream systems.

---

## Features

• Domain-level signal validation
• Dataset registry verification
• Batch-safe signal processing
• Deterministic validation outputs
• Trace ID generation using UUID
• FastAPI-based validation API
• Structured output schema for analytics systems

---

## Project Structure

```
nicai_validation_layer
│
├── main.py
├── validator.py
├── dataset_registry.py
├── schemas.py
├── utils.py
├── datasets.json
├── sample_signals.json
├── test_validation.py
├── REVIEW_PACKET.md
└── README.md
```

---

## Validation Output Format

Each signal produces a structured validation result:

```
{
 "signal_id": "...",
 "status": "ALLOW / FLAG / REJECT",
 "confidence_score": ...,
 "trace_id": "...",
 "reason": "..."
}
```

This output is designed to be directly consumed by downstream analytics systems.

---

## How to Run the Project

### 1. Install Dependencies

```
pip install fastapi uvicorn
```

---

### 2. Run Validation Test Script

```
python test_validation.py
```

This script runs several validation scenarios including:

• valid signals
• FLAG signals
• REJECT signals
• batch signals
• malformed input

---

### 3. Start the Validation API

```
uvicorn main:app --reload
```

---

### 4. Open API Documentation

Open in browser:

```
http://127.0.0.1:8000/docs
```

You can test the validation endpoint using Swagger UI.

---

## Example Signal Input

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

## Example Validation Output

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

## Failure Handling

The validation system safely handles:

• missing required fields
• malformed input signals
• inactive datasets
• invalid schema structure

The system returns structured **REJECT responses** without stopping batch execution.

---

## Testing

Testing is performed using:

• `test_validation.py` script
• FastAPI `/validate` endpoint

The system was tested with:

• valid signals
• inactive dataset signals
• missing field signals
• batch signals
• malformed inputs

All outputs are deterministic and batch-safe.

---

## Summary

This project implements a **clean domain validation layer** aligned with the NICAI architecture.
It ensures that signals entering the intelligence pipeline are validated, traceable, and ready for analytics systems.

The validation layer maintains clear separation between **data validation**, **analytics**, and **decision systems**.
