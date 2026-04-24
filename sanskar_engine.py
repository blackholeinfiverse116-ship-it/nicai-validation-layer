import hashlib
from error_handler import error_response


# -----------------------------
# ZONE DETECTION (SAFE)
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
# SINGLE SIGNAL ANALYSIS (FINAL + TRACEABLE + SAFE)
# =========================================================
def analyze_signal(signal, trace_id=None):

    try:
        # -----------------------------
        # INPUT VALIDATION
        # -----------------------------
        if not isinstance(signal, dict):
            return error_response("Invalid signal format")

        value = signal.get("value")
        feature = str(signal.get("feature_type", "")).lower()

        if not isinstance(value, (int, float)):
            return error_response("Invalid value type")

        # -----------------------------
        # DEFAULT VALUES (SAFE BASELINE)
        # -----------------------------
        risk_level = "LOW"
        anomaly_score = 0.2
        anomaly_type = "NORMAL"
        explanation = "Normal condition"
        confidence = 0.9
        temporal_context = "current_window"

        # -----------------------------
        # TEMPERATURE RULES
        # -----------------------------
        if feature == "temperature":

            if value >= 42:
                risk_level = "HIGH"
                anomaly_score = 0.9
                anomaly_type = "TEMPERATURE_SPIKE"
                explanation = "Extreme temperature detected"
                confidence = 0.95

            elif value >= 35:
                risk_level = "MEDIUM"
                anomaly_score = 0.6
                anomaly_type = "TEMPERATURE_RISE"
                explanation = "Temperature rising"
                confidence = 0.85

        # -----------------------------
        # AQI RULES
        # -----------------------------
        elif feature == "aqi":

            if value >= 250:
                risk_level = "HIGH"
                anomaly_score = 0.95
                anomaly_type = "SEVERE_AIR_POLLUTION"
                explanation = "Hazardous AQI"
                confidence = 0.96

            elif value >= 150:
                risk_level = "MEDIUM"
                anomaly_score = 0.7
                anomaly_type = "HIGH_POLLUTION"
                explanation = "Unhealthy AQI"
                confidence = 0.88

        # -----------------------------
        # TANTRA-COMPLIANT RECOMMENDATION
        # -----------------------------
        if risk_level == "HIGH":
            rec = "eligible_for_escalation"
        elif risk_level == "MEDIUM":
            rec = "requires_review"
        else:
            rec = "monitor"

        # -----------------------------
        # FINAL OUTPUT (TRACEABLE)
        # -----------------------------
        return {
            "trace_id": trace_id,  # ✅ CRITICAL for full pipeline traceability
            "risk_level": risk_level,
            "anomaly_score": anomaly_score,
            "anomaly_type": anomaly_type,
            "explanation": explanation,
            "confidence": confidence,
            "temporal_context": temporal_context,
            "recommendation_signal": rec
        }

    except Exception as e:
        return error_response(str(e))


# =========================================================
# MULTI SIGNAL PATTERN ANALYSIS (FINAL + STABLE)
# =========================================================
def analyze_patterns(outputs):

    try:
        # -----------------------------
        # SAFE EMPTY CASE
        # -----------------------------
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
        freq = {}

        # -----------------------------
        # PROCESS EACH OUTPUT
        # -----------------------------
        for o in outputs:

            if not isinstance(o, dict):
                continue

            risk = o.get("risk_level")

            if risk in ["HIGH", "MEDIUM"]:
                anomaly_count += 1

                # TRACE COLLECTION
                trace = o.get("trace_id")
                if isinstance(trace, str):
                    traces.append(trace)

                # SAFE LAT/LON
                try:
                    lat = float(o.get("latitude"))
                    lon = float(o.get("longitude"))
                except:
                    continue

                zone = detect_zone(lat, lon)

                if not isinstance(zone, str):
                    continue

                zones.add(zone)

                freq[zone] = freq.get(zone, 0) + 1

        # -----------------------------
        # DOMINANT ZONE
        # -----------------------------
        dominant = max(freq, key=freq.get) if freq else "Unknown"

        # -----------------------------
        # PATTERN ID (DETERMINISTIC)
        # -----------------------------
        pattern_id = "PATTERN_" + hashlib.sha256(
            f"{dominant}_{anomaly_count}".encode()
        ).hexdigest()[:6]

        # -----------------------------
        # PATTERN TYPE LOGIC
        # -----------------------------
        if anomaly_count >= 5:
            pattern_type = "CLUSTER_ANOMALY"
            trend = "INCREASING"
        elif anomaly_count >= 2:
            pattern_type = "REPEATED_ANOMALY"
            trend = "STABLE"
        else:
            pattern_type = "LOW_ACTIVITY"
            trend = "LOW"

        # -----------------------------
        # FINAL OUTPUT
        # -----------------------------
        return {
            "pattern_id": pattern_id,
            "anomaly_count": anomaly_count,
            "affected_zones": list(zones),
            "pattern_summary": f"Anomalies concentrated in {dominant}",
            "pattern_type": pattern_type,
            "severity_trend": trend,
            "linked_traces": traces
        }

    except Exception as e:
        return error_response(str(e))
