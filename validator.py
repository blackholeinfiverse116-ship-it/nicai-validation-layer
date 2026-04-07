from schemas import required_fields
from dataset_registry import get_dataset
from utils import generate_trace_id, validate_output_schema

from bucket_emitter import emit_bucket_artifact
from telemetry_emitter import emit_telemetry


def process_emissions(result, signal):
    """
    Handles observability emissions (Bucket + Telemetry)
    without modifying validation behavior.
    """

    # Schema contract validation
    try:
        validate_output_schema(result)
    except Exception as e:
        print("Schema validation failed:", e)

    # Bucket emission (memory artifact)
    try:
        emit_bucket_artifact(result)
    except Exception as e:
        print("Bucket emission failed:", e)

    # Telemetry emission (observability metrics)
    try:
        emit_telemetry(result, signal.get("dataset_id"))
    except Exception as e:
        print("Telemetry emission failed:", e)


def validate_signal(signal):

    trace_id = generate_trace_id()

    # Check missing fields
    for field in required_fields:
        if field not in signal:
            result = {
                "signal_id": signal.get("signal_id"),
                "status": "REJECT",
                "confidence_score": 0.0,
                "trace_id": trace_id,
                "reason": f"missing field {field}"
            }

            process_emissions(result, signal)
            return result

    # Dataset check
    dataset = get_dataset(signal["dataset_id"])

    if dataset is None:
        result = {
            "signal_id": signal["signal_id"],
            "status": "REJECT",
            "confidence_score": 0.1,
            "trace_id": trace_id,
            "reason": "dataset not registered"
        }

        process_emissions(result, signal)
        return result

    if dataset["status"] != "active":
        result = {
            "signal_id": signal["signal_id"],
            "status": "FLAG",
            "confidence_score": dataset["trust_score"],
            "trace_id": trace_id,
            "reason": "dataset inactive"
        }

        process_emissions(result, signal)
        return result

    # Valid signal
    result = {
        "signal_id": signal["signal_id"],
        "status": "ALLOW",
        "confidence_score": dataset["trust_score"],
        "trace_id": trace_id,
        "reason": "valid signal"
    }

    process_emissions(result, signal)
    return result


def validate_batch(signals):

    results = []

    for signal in signals:
        result = validate_signal(signal)
        results.append(result)

    return {"results": results}