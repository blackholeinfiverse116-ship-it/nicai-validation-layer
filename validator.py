from schemas import required_fields
from dataset_registry import get_dataset
from utils import generate_trace_id, validate_output_schema


# -------------------------------
# SAFE OPTIONAL IMPORTS
# -------------------------------
try:
    from bucket_emitter import emit_bucket_artifact
    from telemetry_emitter import emit_telemetry
except ImportError:
    def emit_bucket_artifact(x): pass
    def emit_telemetry(a, b): pass


# -------------------------------
# STANDARD ERROR FORMAT
# -------------------------------
def build_error(reason, trace_id=None, signal=None):
    return {
        "signal_id": signal.get("signal_id") if isinstance(signal, dict) else None,
        "status": "ERROR",
        "confidence_score": 0.0,
        "trace_id": trace_id,
        "reason": reason
    }


# -------------------------------
# SAFE TRACE ID
# -------------------------------
def safe_trace_id(signal):
    try:
        return generate_trace_id(signal)
    except:
        return "TRACE_UNKNOWN"


# -------------------------------
# VALIDATE SINGLE SIGNAL
# -------------------------------
def validate_signal(signal):

    try:
        # -------------------------------
        # BASIC CHECK
        # -------------------------------
        if not isinstance(signal, dict):
            return build_error("Invalid signal format")

        trace_id = safe_trace_id(signal)

        # -------------------------------
        # REQUIRED FIELDS CHECK
        # -------------------------------
        for field in required_fields:
            if field not in signal or signal.get(field) in [None, ""]:
                result = build_error(f"Missing field: {field}", trace_id, signal)

                validate_output_schema(result)
                emit_bucket_artifact(result)
                emit_telemetry(signal, result)
                return result

        # -------------------------------
        # SAFE DATASET ID (🔥 FIX)
        # -------------------------------
        dataset_id = signal.get("dataset_id")

        if not isinstance(dataset_id, (str, int)):
            result = build_error("Invalid dataset_id type", trace_id, signal)
            return result

        dataset = get_dataset(dataset_id)

        if not isinstance(dataset, dict):
            result = build_error("Dataset not registered", trace_id, signal)

            validate_output_schema(result)
            emit_bucket_artifact(result)
            emit_telemetry(signal, result)
            return result

        # -------------------------------
        # DATASET STATUS CHECK
        # -------------------------------
        if dataset.get("status") != "active":
            result = {
                "signal_id": signal.get("signal_id"),
                "status": "FLAG",
                "confidence_score": dataset.get("trust_score", 0.5),
                "trace_id": trace_id,
                "reason": "Dataset inactive"
            }

            validate_output_schema(result)
            emit_bucket_artifact(result)
            emit_telemetry(signal, result)
            return result

        # -------------------------------
        # FEATURE VALIDATION
        # -------------------------------
        value = signal.get("value")
        feature = str(signal.get("feature_type", "")).lower()

        if not isinstance(value, (int, float)):
            status = "ERROR"
            confidence = 0.0
            reason = "Invalid value type"

        elif feature == "temperature":
            if value >= 45:
                status = "FLAG"
                confidence = 0.6
                reason = "Extreme temperature"
            elif value >= 38:
                status = "FLAG"
                confidence = 0.7
                reason = "High temperature"
            else:
                status = "VALID"
                confidence = 0.9
                reason = "Normal temperature"

        elif feature == "aqi":
            if value >= 300:
                status = "FLAG"
                confidence = 0.6
                reason = "Hazardous AQI"
            elif value >= 200:
                status = "FLAG"
                confidence = 0.7
                reason = "Unhealthy AQI"
            else:
                status = "VALID"
                confidence = 0.9
                reason = "Normal AQI"

        elif feature == "traffic":
            if value >= 90:
                status = "FLAG"
                confidence = 0.6
                reason = "Severe traffic"
            elif value >= 70:
                status = "FLAG"
                confidence = 0.7
                reason = "Heavy traffic"
            else:
                status = "VALID"
                confidence = 0.9
                reason = "Normal traffic"

        else:
            status = "VALID"
            confidence = 0.8
            reason = "Valid signal"

        # -------------------------------
        # FINAL OUTPUT
        # -------------------------------
        result = {
            "signal_id": signal.get("signal_id"),
            "status": status,
            "confidence_score": confidence,
            "trace_id": trace_id,
            "reason": reason
        }

        validate_output_schema(result)
        emit_bucket_artifact(result)
        emit_telemetry(signal, result)

        return result

    except Exception as e:
        return build_error(str(e), None, signal)


# -------------------------------
# VALIDATE BATCH
# -------------------------------
def validate_batch(signals):

    try:
        if not isinstance(signals, list):
            return {
                "status": "ERROR",
                "reason": "Input must be list",
                "trace_id": None
            }

        safe_signals = [s for s in signals if isinstance(s, dict)]

        safe_signals.sort(key=lambda x: str(x.get("signal_id", "")))

        results = [validate_signal(s) for s in safe_signals]

        return {"results": results}

    except Exception as e:
        return {
            "status": "ERROR",
            "reason": str(e),
            "trace_id": None
        }


# -------------------------------
# FILTER VALID SIGNALS
# -------------------------------
def get_validated_signals(signals):

    try:
        batch = validate_batch(signals)

        if batch.get("status") == "ERROR":
            return batch

        return [
            r for r in batch.get("results", [])
            if isinstance(r, dict) and r.get("status") in ["VALID", "FLAG"]
        ]

    except Exception as e:
        return {
            "status": "ERROR",
            "reason": str(e),
            "trace_id": None
        }
