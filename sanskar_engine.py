import hashlib
from collections import defaultdict

from error_handler import error_response


# -----------------------------
# ZONE DETECTION (STRICT SAFE)
# -----------------------------
def detect_zone(lat, lon):
    try:
        lat = float(lat)

        if lat > 23:
            return "North"
        elif lat > 20:
            return "Central"
        else:
            return "South"

    except:
        return "Unknown"


# =========================================================
# SINGLE SIGNAL ANALYSIS
# =========================================================
def analyze_signal(signal):

    try:
        if not isinstance(signal, dict):
            return error_response("Invalid signal format")

        value = signal.get("value")
        feature = str(signal.get("feature_type", "")).lower()

        if not isinstance(value, (int, float)):
            return error_response("Invalid value type")

        risk_level = "LOW"
        anomaly_score = 0.2
        anomaly_type = "NORMAL"
        explanation = "Normal condition"

        # TEMPERATURE
        if feature == "temperature":
            if value >= 42:
                risk_level = "HIGH"
                anomaly_score = 0.9
                anomaly_type = "TEMPERATURE_SPIKE"
                explanation = "Extreme temperature detected"
            elif value >= 35:
                risk_level = "MEDIUM"
                anomaly_score = 0.6
                anomaly_type = "TEMPERATURE_RISE"
                explanation = "Temperature rising"

        # AQI
        elif feature == "aqi":
            if value >= 250:
                risk_level = "HIGH"
                anomaly_score = 0.95
                anomaly_type = "SEVERE_AIR_POLLUTION"
                explanation = "Hazardous AQI"
            elif value >= 150:
                risk_level = "MEDIUM"
                anomaly_score = 0.7
                anomaly_type = "HIGH_POLLUTION"
                explanation = "Unhealthy AQI"

        # RECOMMENDATION
        if risk_level == "HIGH":
            rec = "eligible_for_escalation"
        elif risk_level == "MEDIUM":
            rec = "requires_review"
        else:
            rec = "monitor"

        return {
            "risk_level": risk_level,
            "anomaly_score": anomaly_score,
            "anomaly_type": anomaly_type,
            "explanation": explanation,
            "recommendation_signal": rec
        }

    except Exception as e:
        return error_response(str(e))


# =========================================================
# MULTI SIGNAL PATTERN ANALYSIS (🔥 FINAL FIX)
# =========================================================
def analyze_patterns(outputs):

    try:
        if not isinstance(outputs, list) or not outputs:
            return {
                "pattern_id": "PATTERN_NONE",
                "anomaly_count": 0,
                "affected_zones": [],
                "pattern_summary": "No data",
                "pattern_type": "NO_PATTERN",
                "severity_trend": "NONE",
                "linked_traces": []
            }

        anomaly_count = 0
        zones = set()
        traces = []

        # ❗ REPLACED defaultdict → normal dict (safer)
        freq = {}

        for o in outputs:

            if not isinstance(o, dict):
                continue

            risk = o.get("risk_level")

            if risk in ["HIGH", "MEDIUM"]:
                anomaly_count += 1

                # TRACE SAFE
                trace = o.get("trace_id")
                if isinstance(trace, str):
                    traces.append(trace)

                # 🔥 HARD LAT/LON VALIDATION
                lat = o.get("latitude")
                lon = o.get("longitude")

                try:
                    lat = float(lat)
                    lon = float(lon)
                except:
                    continue  # skip bad data completely

                zone = detect_zone(lat, lon)

                # 🔥 FINAL SAFETY
                if not isinstance(zone, str):
                    continue

                zones.add(zone)

                # SAFE DICT UPDATE
                if zone not in freq:
                    freq[zone] = 0
                freq[zone] += 1

        dominant = max(freq, key=freq.get) if freq else "Unknown"

        pattern_id = "PATTERN_" + hashlib.sha256(
            f"{dominant}_{anomaly_count}".encode()
        ).hexdigest()[:6]

        return {
            "pattern_id": pattern_id,
            "anomaly_count": anomaly_count,
            "affected_zones": list(zones),
            "pattern_summary": f"Anomalies concentrated in {dominant}",
            "pattern_type": (
                "CLUSTER_ANOMALY" if anomaly_count >= 5
                else "REPEATED_ANOMALY" if anomaly_count >= 2
                else "LOW_ACTIVITY"
            ),
            "severity_trend": (
                "INCREASING" if anomaly_count >= 5
                else "STABLE" if anomaly_count >= 2
                else "LOW"
            ),
            "linked_traces": traces
        }

    except Exception as e:
        return error_response(str(e))
