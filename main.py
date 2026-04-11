from fastapi import FastAPI
from validator import validate_signal
from analytics_engine import analyze_signal
from decision_engine import make_decision
from samachar_input_adapter import adapt_input
from error_handler import handle_error

app = FastAPI()


@app.post("/nicai/evaluate")
def evaluate_signal(signal: dict):

    try:

        # Step 1 — Adapt Samachar input
        signal = adapt_input(signal)

        # Step 2 — Validation
        validation = validate_signal(signal)

        if validation["status"] == "REJECT":
            return validation

        # Step 3 — Analytics (IMPORTANT FIX)
        analytics = analyze_signal({**validation, **signal})

        # Step 4 — Decision
        decision = make_decision(analytics)

        # Step 5 — Final Contract Output
        return {
            "signal_id": validation["signal_id"],
            "status": validation["status"],
            "confidence_score": validation["confidence_score"],
            "trace_id": validation["trace_id"],
            "reason": validation["reason"],
            "anomaly_score": analytics["anomaly_score"],
            "priority": analytics["priority"],
            "decision": decision["decision"],
            "risk_level": decision["risk_level"],
            "summary_line": f"Signal {decision['decision']} with {analytics['priority']} priority",
            "explanation": decision["reason"]
        }

    except Exception as e:

        return handle_error(str(e))