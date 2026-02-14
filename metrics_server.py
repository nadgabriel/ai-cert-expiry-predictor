from prometheus_client import start_http_server, Gauge
import time
import pandas as pd
import joblib
from cert_parser import parse_certificate
from model import predict_risk

# Prometheus metrics
CERT_DAYS_REMAINING = Gauge(
    "cert_days_remaining",
    "Days remaining until certificate expiry"
)

CERT_EXPIRY_RISK = Gauge(
    "cert_expiry_risk_score",
    "Predicted certificate expiry risk score"
)

def run_metrics(cert_path: str):
    model = joblib.load("model.pkl")

    while True:
        features = parse_certificate(cert_path)
        df = pd.DataFrame([features])

        risk = predict_risk(model, df)[0]

        CERT_DAYS_REMAINING.set(features["days_remaining"])
        CERT_EXPIRY_RISK.set(risk)

        time.sleep(60)


if __name__ == "__main__":
    start_http_server(8000)
    print("Prometheus metrics exposed on :8000/metrics")

    run_metrics("certs/server.crt")
