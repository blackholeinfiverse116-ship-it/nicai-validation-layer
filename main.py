from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from datetime import datetime, timezone
import json
import os
import traceback

from validator import validate_signal
from samachar_input_adapter import load_data, convert_to_signals
from sanskar_engine import analyze_signal, analyze_patterns
from error_handler import error_response

app = FastAPI()
os.makedirs("logs", exist_ok=True)


# -----------------------------
# SAFE HELPERS
# -----------------------------
def to_str(v):
    try:
        return str(v)
    except:
        return "N/A"


def to_float(v):
    try:
        return float(v)
    except:
        return 0.0


# -----------------------------
# LOGGING
# -----------------------------
def log_data(filename, log_type, data):
    try:
        with open(f"logs/{filename}", "a") as f:
            f.write(json.dumps({
                "trace_id": to_str(data.get("trace_id")),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "type": log_type,
                "data": data
            }, default=str) + "\n")
    except:
        pass


# -----------------------------
# ROOT
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body>
            <h2>NICAI Running ✅</h2>
            <a href="/dashboard">Open Dashboard</a>
        </body>
    </html>
    """


# -----------------------------
# 🔥 MAIN PIPELINE API (REQUIRED)
# -----------------------------
@app.post("/nicai/evaluate")
def evaluate(signals: list):

    try:
        if not isinstance(signals, list):
            return error_response("Input must be list")

        results = []
        processed = []

        for signal in signals:

            validation = validate_signal(signal)

            if validation.get("status") == "REJECT":
                results.append(validation)
                continue

            trace_id = validation.get("trace_id")

            analysis = analyze_signal(signal, trace_id)

            combined = {
                "signal_id": signal.get("signal_id"),
                "trace_id": trace_id,
                "validation": validation,
                "analysis": analysis
            }

            results.append(combined)

            processed.append({
                "trace_id": trace_id,
                "risk_level": analysis.get("risk_level"),
                "latitude": signal.get("latitude"),
                "longitude": signal.get("longitude")
            })

        pattern = analyze_patterns(processed)

        return {
            "status": "SUCCESS",
            "results": results,
            "pattern": pattern
        }

    except Exception as e:
        return error_response(str(e))


# -----------------------------
# DASHBOARD
# -----------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    try:
        weather, aqi = load_data()

        if weather is None or aqi is None:
            return HTMLResponse("<h3>Error: Dataset not loaded</h3>")

        signals = convert_to_signals(weather, aqi)

        if not isinstance(signals, list) or not signals:
            return HTMLResponse("<h3>No data available</h3>")

        rows = ""
        processed_outputs = []

        for signal in signals[:20]:

            if not isinstance(signal, dict):
                continue

            # VALIDATION
            validation = validate_signal(signal)

            if not isinstance(validation, dict):
                continue

            if validation.get("status") == "REJECT":
                continue

            validation_status = validation.get("status")
            trace_id = to_str(validation.get("trace_id"))

            # 🔥 FIXED: PASS TRACE_ID
            analysis = analyze_signal(signal, trace_id)

            if not isinstance(analysis, dict):
                continue

            risk = str(analysis.get("risk_level", "LOW"))
            confidence = analysis.get("confidence", 0)

            # ACTION
            if risk == "HIGH":
                step = "Escalation recommended"
                action_label = "Escalate"
                action_type = "eligible_for_escalation"
                row_color = "#ffe6e6"

            elif risk == "MEDIUM":
                step = "Needs review"
                action_label = "Review"
                action_type = "requires_review"
                row_color = "#fff5cc"

            else:
                step = "Monitor"
                action_label = "Monitor"
                action_type = "monitor"
                row_color = ""

            processed_outputs.append({
                "signal_id": to_str(signal.get("signal_id")),
                "trace_id": trace_id,
                "risk_level": risk,
                "latitude": to_float(signal.get("latitude")),
                "longitude": to_float(signal.get("longitude")),
                "anomaly_score": float(analysis.get("anomaly_score", 0))
            })

            # LOGGING
            log_data("validation_logs.json", "VALIDATION", validation)
            log_data("anomaly_logs.json", "ANALYSIS", analysis)

            # TABLE
            rows += f"""
            <tr style="background-color:{row_color};">
                <td>{to_str(signal.get("signal_id"))}</td>
                <td>{trace_id}</td>
                <td>{validation_status}</td>
                <td>{risk}</td>
                <td>{confidence}</td>
                <td>{to_str(analysis.get("anomaly_type"))}</td>
                <td>{to_str(analysis.get("explanation"))}</td>
                <td>{step}</td>
                <td>
                    <button onclick="sendAction('{trace_id}','{action_type}','{risk}')">
                        {action_label}
                    </button>
                </td>
            </tr>
            """

        # PATTERN
        pattern = analyze_patterns(processed_outputs)
        log_data("pattern_logs.json", "PATTERN", pattern)

        total_signals = len(signals)
        total_anomalies = len([o for o in processed_outputs if o.get("risk_level") != "LOW"])

        try:
            with open("logs/action_logs.json") as f:
                action_count = len(f.readlines())
        except:
            action_count = 0

        html_content = f"""
        <html>
        <head>
            <title>NICAI Dashboard</title>

            <script>
            async function sendAction(trace_id, action_type, risk) {{
                await fetch("/action", {{
                    method: "POST",
                    headers: {{"Content-Type": "application/json"}},
                    body: JSON.stringify({{
                        trace_id: trace_id,
                        action_type: action_type,
                        risk_level: risk
                    }})
                }});
                alert("Action logged");
                location.reload();
            }}
            </script>
        </head>

        <body>

        <h2>NICAI Dashboard</h2>

        <p>Total Signals: {total_signals}</p>
        <p>Total Anomalies: {total_anomalies}</p>
        <p>Actions Logged: {action_count}</p>

        <h3>Pattern Summary</h3>
        <p><b>Pattern ID:</b> {pattern.get("pattern_id")}</p>
        <p><b>Anomaly Count:</b> {pattern.get("anomaly_count")}</p>
        <p><b>Zones:</b> {pattern.get("affected_zones")}</p>
        <p><b>Pattern Type:</b> {pattern.get("pattern_type")}</p>
        <p><b>Trend:</b> {pattern.get("severity_trend")}</p>
        <p><b>Summary:</b> {pattern.get("pattern_summary")}</p>

        <table border="1" cellpadding="5">
        <tr>
            <th>ID</th>
            <th>Trace ID</th>
            <th>Validation</th>
            <th>Risk</th>
            <th>Confidence</th>
            <th>Type</th>
            <th>Explanation</th>
            <th>Recommended Step</th>
            <th>Action</th>
        </tr>

        {rows}

        </table>

        </body>
        </html>
        """

        return HTMLResponse(content=html_content)

    except Exception as e:
        traceback.print_exc()
        return HTMLResponse(f"<h3>Error: {str(e)}</h3>")


# -----------------------------
# ACTION ROUTER
# -----------------------------
@app.post("/action")
def trigger_action(data: dict):

    try:
        if not isinstance(data, dict):
            return error_response("Invalid input")

        risk = data.get("risk_level", "LOW")

        if risk == "HIGH":
            target = "authority"
        elif risk == "MEDIUM":
            target = "operator"
        else:
            target = "system"

        action_payload = {
            "trace_id": to_str(data.get("trace_id")),
            "action_type": data.get("action_type"),
            "target_role": target,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "context": {}
        }

        log_data("action_logs.json", "ACTION", action_payload)

        return {
            "status": "SUCCESS",
            "action": action_payload
        }

    except Exception as e:
        return error_response(str(e))
