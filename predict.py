import pandas as pd
import joblib
from cert_parser import parse_certificate
from model import predict_risk

model = joblib.load("model.pkl")

features = parse_certificate("certs/server.crt")

df = pd.DataFrame([features])

risk = predict_risk(model, df)

print(f"Predicted expiry risk score: {risk[0]:.2f}")
