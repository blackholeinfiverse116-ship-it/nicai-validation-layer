import hashlib
from collections import defaultdict


def generate_pattern_id(linked_traces):
    """
    Deterministic pattern id based on traces
    """
    base = "".join(sorted(linked_traces))
    return "PATTERN_" + hashlib.sha256(base.encode()).hexdigest()[:6]


def analyze_patterns(outputs):

    anomaly_count = 0
    affected_zones = set()
    linked_traces = []
    zone_frequency = defaultdict(int)

    for o in outputs:

        # --- SAFETY: ensure dict ---
        if not isinstance(o, dict):
            continue

        risk = o.get("risk_level")
        trace_id = o.get("trace_id")

        if risk == "HIGH" or o.get("anomaly_score", 0) >= 0.6:

            anomaly_count += 1

            # trace tracking
            if trace_id:
                linked_traces.append(str(trace_id))

            # --- SAFE ZONE EXTRACTION ---
            lat = o.get("latitude")
            lon = o.get("longitude")

            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                zone = f"{lat}_{lon}"
            else:
                zone = o.get("zone", "Unknown")

            # 🚨 FINAL SAFETY (fix unhashable issue)
            if isinstance(zone, dict):
                zone = str(zone)

            zone = str(zone)

            affected_zones.add(zone)
            zone_frequency[zone] += 1

    # --- DETERMINISTIC PATTERN ID ---
    pattern_id = generate_pattern_id(linked_traces)

    # --- severity trend ---
    if anomaly_count >= 5:
        severity_trend = "INCREASING"
    elif anomaly_count >= 2:
        severity_trend = "STABLE"
    else:
        severity_trend = "LOW"

    # --- pattern type ---
    if anomaly_count >= 5:
        pattern_type = "CLUSTER_ANOMALY"
    elif anomaly_count >= 2:
        pattern_type = "REPEATED_ANOMALY"
    else:
        pattern_type = "ISOLATED_EVENT"

    # --- summary ---
    if anomaly_count >= 5:
        summary = "Clustered high-risk anomalies detected in nearby region"
    elif anomaly_count > 0:
        summary = "Some anomalies detected"
    else:
        summary = "No major anomalies"

    return {
        "pattern_id": pattern_id,
        "anomaly_count": anomaly_count,
        "affected_zones": sorted(list(affected_zones)),  # deterministic order
        "pattern_summary": summary,
        "pattern_type": pattern_type,
        "severity_trend": severity_trend,
        "linked_traces": sorted(linked_traces)  # deterministic
    }


# wrapper
def analyze_multi_signals(outputs):
    return analyze_patterns(outputs)
