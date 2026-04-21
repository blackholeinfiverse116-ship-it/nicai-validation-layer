from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime, timezone
import json
import os
import traceback

from validator import validate_signal
from samachar_input_adapter import load_data, convert_to_signals
from error_handler import error_response
from sanskar_engine import analyze_signal, analyze_patterns

app = FastAPI()
templates = Jinja2Templates(directory="templates")

os.makedirs("logs", exist_ok=True)


# -----------------------------
# SAFE HELPERS
# -----------------------------
def to_str(v):
    try:
        if isinstance(v, dict):
            return json.dumps(v)
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
        log_entry = {
            "trace_id": to_str(data.get("trace_id")),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "type": log_type,
            "data": data
        }

        with open(f"logs/{filename}", "a") as f:
            f.write(json.dumps(log_entry, default=str) + "\n")

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
# MAIN DASHBOARD
# -----------------------------
@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    try:
        weather, aqi = load_data()
        signals = convert_to_signals(weather, aqi)

        if not isinstance(signals, list) or not signals:
            return HTMLResponse("<h3>No data available</h3>")

        rows = ""
        processed_outputs = []

        for signal in signals[:20]:

            # -----------------------------
            # SAFE SIGNAL CHECK
            # -----------------------------
            if not isinstance(signal, dict):
                continue

            # -----------------------------
            # VALIDATION
            # -----------------------------
            validation = validate_signal(signal)

            if not isinstance(validation, dict):
                continue

            if validation.get("status") == "ERROR":
                continue

            # -----------------------------
            # ANALYSIS
            # -----------------------------
            analysis = analyze_signal(signal)

            if not isinstance(analysis, dict):
                continue

            if analysis.get("status") == "ERROR":
                continue

            # -----------------------------
            # SAFE VALUES
            # -----------------------------
            trace_id = to_str(validation.get("trace_id"))
            risk = str(analysis.get("risk_level", "LOW"))
            anomaly_type = to_str(analysis.get("anomaly_type"))
            explanation = to_str(analysis.get("explanation"))

            lat = to_float(signal.get("latitude"))
            lon = to_float(signal.get("longitude"))

            # -----------------------------
            # ACTION UI
            # -----------------------------
            if risk == "HIGH":
                action_label = "Escalate"
                action_type = "ESCALATE"
                row_color = "#ffe6e6"
            elif risk == "MEDIUM":
                action_label = "Review"
                action_type = "REVIEW"
                row_color = "#fff5cc"
            else:
                action_label = "Monitor"
                action_type = "MONITOR"
                row_color = ""

            # -----------------------------
            # SAFE OUTPUT (🔥 CRITICAL FIX)
            # -----------------------------
            processed_outputs.append({
                "signal_id": to_str(signal.get("signal_id")),
                "trace_id": trace_id,
                "risk_level": risk,
                "latitude": lat,
                "longitude": lon,
                "anomaly_score": float(analysis.get("anomaly_score", 0))
            })

            # -----------------------------
            # LOGS
            # -----------------------------
            log_data("validation_logs.json", "VALIDATION", validation)
            log_data("anomaly_logs.json", "ANALYSIS", analysis)

            # -----------------------------
            # TABLE ROW
            # -----------------------------
            rows += f"""
            <tr style="background-color:{row_color};">
                <td>{to_str(signal.get("signal_id"))}</td>
                <td>{risk}</td>
                <td>{anomaly_type}</td>
                <td>{explanation}</td>
                <td>
                    <button onclick="sendAction('{trace_id}','{action_type}','{risk}')">
                        {action_label}
                    </button>
                </td>
            </tr>
            """

        # -----------------------------
        # PATTERN (SAFE)
        # -----------------------------
        try:
            pattern = analyze_patterns(processed_outputs)
        except:
            pattern = {}

        log_data("pattern_logs.json", "PATTERN", pattern)

        # -----------------------------
        # STATS
        # -----------------------------
        total_signals = len(signals)

        total_anomalies = len([
            o for o in processed_outputs
            if isinstance(o, dict) and o.get("risk_level") != "LOW"
        ])

        try:
            with open("logs/action_logs.json") as f:
                action_count = len(f.readlines())
        except:
            action_count = 0

        # -----------------------------
        # HTML
        # -----------------------------
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

        <table border="1" cellpadding="5">
        <tr>
            <th>ID</th>
            <th>Risk</th>
            <th>Type</th>
            <th>Explanation</th>
            <th>Action</th>
        </tr>

        {rows}

        </table>

        </body>
        </html>
        """

        return HTMLResponse(content=html_content)

    except Exception as e:
        traceback.print_exc()   # 🔥 EXACT ERROR LINE
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
            target = "monitor"

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
