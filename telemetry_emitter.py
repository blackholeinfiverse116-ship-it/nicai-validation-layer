import json
from datetime import datetime

METRICS_FILE = "telemetry_metrics.json"

metrics = {
    "total_signals": 0,
    "reject_count": 0,
    "flag_count": 0
}

def emit_telemetry(validation_output, dataset_id):
    metrics["total_signals"] += 1

    if validation_output["status"] == "REJECT":
        metrics["reject_count"] += 1

    if validation_output["status"] == "FLAG":
        metrics["flag_count"] += 1

    telemetry = {
        "trace_id": validation_output["trace_id"],
        "dataset_id": dataset_id,
        "status": validation_output["status"],
        "confidence_score": validation_output["confidence_score"],
        "timestamp": datetime.utcnow().isoformat()
    }

    try:
        with open(METRICS_FILE, "w") as f:
            json.dump(metrics, f, indent=2)
    except Exception as e:
        print("Telemetry emission failed:", e)

    return telemetry