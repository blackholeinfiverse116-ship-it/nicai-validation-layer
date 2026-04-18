import json
import hashlib
from datetime import datetime, timezone
from collections import defaultdict

from error_handler import error_response


# -----------------------------
# ZONE DETECTION
# -----------------------------
def detect_zone(lat, lon):
    try:
        if lat is None or lon is None:
            return "Unknown"

        if lat > 23:
            return "North"
        elif lat > 20:
            return "Central"
        else:
            return "South"

    except:
        return "Unknown"


# =========================================================
# 🔹 SINGLE SIGNAL ANALYSIS
# =========================================================
def analyze_signal(signal):

    try:
        # -----------------------------
        # INPUT VALIDATION
        # -----------------------------
        if not isinstance(signal, dict):
            return error_response("Invalid signal input (must be dict)")

        if not signal:
            return error_response("Empty signal received")

        if "value" not in signal:
            return error_response("Missing 'value' field")

        value = signal.get("value")

        if not isinstance(value, (int, float)):
            return error_response("Invalid value type (must be numeric)")

        feature = str(signal.get("feature_type", "")).lower()

        # -----------------------------
        # DEFAULT VALUES
        # -----------------------------
        risk_level = "LOW"
        anomaly_score = 0.2
        anomaly_type = "NORMAL"
        explanation = "Everything normal"

        # -----------------------------
        # TEMPERATURE
        # -----------------------------
        if feature == "temperature":

            if value >= 45:
                risk_level = "HIGH"
                anomaly_score = 0.9
                anomaly_type = "TEMPERATURE_SPIKE"
                explanation = "Extreme temperature detected"

            elif value >= 38:
                risk_level = "MEDIUM"
                anomaly_score = 0.6
                anomaly_type = "TEMPERATURE_RISE"
                explanation = "Temperature rising above safe threshold"

        # -----------------------------
        # AQI
        # -----------------------------
        elif feature == "aqi":

            if value >= 300:
                risk_level = "HIGH"
                anomaly_score = 0.95
                anomaly_type = "SEVERE_AIR_POLLUTION"
                explanation = "Air quality extremely hazardous"

            elif value >= 200:
                risk_level = "MEDIUM"
                anomaly_score = 0.7
                anomaly_type = "HIGH_POLLUTION"
                explanation = "Air quality unhealthy"

        # -----------------------------
        # TRAFFIC
        # -----------------------------
        elif feature == "traffic":

            if value >= 90:
                risk_level = "HIGH"
                anomaly_score = 0.85
                anomaly_type = "TRAFFIC_CONGESTION"
                explanation = "Severe traffic congestion detected"

            elif value >= 70:
                risk_level = "MEDIUM"
                anomaly_score = 0.6
                anomaly_type = "HEAVY_TRAFFIC"
                explanation = "Traffic density increasing"

        # -----------------------------
        # UNKNOWN FEATURE
        # -----------------------------
        else:
            anomaly_type = "UNKNOWN_FEATURE"
            explanation = "Feature type not recognized"
            anomaly_score = 0.1

        # -----------------------------
        # TANTRA COMPLIANT OUTPUT
        # -----------------------------
        if risk_level == "HIGH":
            recommendation = "eligible_for_escalation"
        elif risk_level == "MEDIUM":
            recommendation = "requires_review"
        else:
            recommendation = "monitor"

        output = {
            "risk_level": risk_level,
            "anomaly_score": anomaly_score,
            "anomaly_type": anomaly_type,
            "explanation": explanation,
            "recommendation_signal": recommendation
        }

        # -----------------------------
        # LOGGING (FIXED TIME)
        # -----------------------------
        try:
            log_entry = {
                "trace_id": signal.get("trace_id"),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": "ANALYSIS",
                "data": output
            }

            with open("logs/anomaly_logs.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")

        except:
            pass

        return output

    except Exception as e:
        return error_response(str(e))


# =========================================================
# 🔹 MULTI-SIGNAL ANALYSIS
# =========================================================
def analyze_patterns(outputs):

    try:
        # -----------------------------
        # INPUT VALIDATION
        # -----------------------------
        if not isinstance(outputs, list):
            return error_response("Invalid input (outputs must be list)")

        # ✅ FIX: DO NOT THROW ERROR
        if len(outputs) == 0:
            return {
                "pattern_id": "PATTERN_NONE",
                "anomaly_count": 0,
                "affected_zones": [],
                "pattern_summary": "No data available",
                "pattern_type": "NO_PATTERN",
                "severity_trend": "NONE",
                "linked_traces": []
            }

        anomaly_count = 0
        affected_zones = set()
        linked_traces = []

        zone_frequency = defaultdict(int)

        # -----------------------------
        # PROCESS
        # -----------------------------
        for o in outputs:

            risk = o.get("risk_level")
            trace_id = o.get("trace_id")
            anomaly_score = o.get("anomaly_score", 0)

            if risk == "HIGH" or anomaly_score >= 0.6:

                anomaly_count += 1

                if trace_id:
                    linked_traces.append(trace_id)

                zone = detect_zone(
                    o.get("latitude"),
                    o.get("longitude")
                )

                affected_zones.add(zone)
                zone_frequency[zone] += 1

        dominant_zone = (
            max(zone_frequency, key=zone_frequency.get)
            if zone_frequency else "Unknown"
        )

        trace_string = "".join(sorted(linked_traces))
        base_string = f"{dominant_zone}_{anomaly_count}_{trace_string}"

        pattern_id = "PATTERN_" + hashlib.sha256(
            base_string.encode()
        ).hexdigest()[:6]

        # -----------------------------
        # PATTERN LOGIC
        # -----------------------------
        if anomaly_count >= 5:
            severity_trend = "INCREASING"
            pattern_type = "CLUSTER_ANOMALY"
            summary = f"Clustered anomalies detected in {dominant_zone}"

        elif anomaly_count >= 2:
            severity_trend = "STABLE"
            pattern_type = "REPEATED_ANOMALY"
            summary = f"Moderate anomalies in {dominant_zone}"

        elif anomaly_count == 1:
            severity_trend = "LOW"
            pattern_type = "ISOLATED_EVENT"
            summary = f"Single anomaly in {dominant_zone}"

        else:
            severity_trend = "NONE"
            pattern_type = "NO_PATTERN"
            summary = "No anomalies detected"

        pattern_output = {
            "pattern_id": pattern_id,
            "anomaly_count": anomaly_count,
            "affected_zones": list(affected_zones),
            "pattern_summary": summary,
            "pattern_type": pattern_type,
            "severity_trend": severity_trend,
            "linked_traces": linked_traces
        }

        # -----------------------------
        # LOGGING (FIXED TIME)
        # -----------------------------
        try:
            log_entry = {
                "trace_id": pattern_id,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": "PATTERN",
                "data": pattern_output
            }

            with open("logs/pattern_logs.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")

        except:
            pass

        return pattern_output

    except Exception as e:
        return error_response(str(e))