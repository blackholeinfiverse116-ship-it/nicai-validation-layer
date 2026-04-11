def adapt_input(signal: dict):

    return {
        "signal_id": signal.get("signal_id"),
        "timestamp": signal.get("timestamp"),
        "latitude": signal.get("latitude"),
        "longitude": signal.get("longitude"),
        "feature_type": signal.get("feature_type"),
        "value": signal.get("value"),
        "dataset_id": signal.get("dataset_id")
    }