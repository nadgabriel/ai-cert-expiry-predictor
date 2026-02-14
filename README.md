# AI Certificate Expiry Predictor with Prometheus Metrics

Machine learning–based certificate risk scoring service with real X.509 parsing and Prometheus monitoring integration.

---

## Overview

This project combines:

- Real TLS certificate parsing (X.509)
- Feature extraction from live certificates
- Machine learning–based expiry risk prediction
- Prometheus metrics export
- Containerized deployment

The service continuously analyzes a certificate and exposes:

- Remaining validity days
- Predicted expiry risk score

---

## Architecture

Certificate → Feature Extraction → ML Model → Risk Score  
                                           ↓  
                                     Prometheus Metrics

Metrics endpoint exposed on:

    http://localhost:8000/metrics

---

## Features

- X.509 parsing using `cryptography`
- Feature engineering from real certificate metadata
- RandomForest-based expiry risk scoring
- Prometheus metrics export
- Dockerized runtime
- CI-ready structure

---

## Extracted Certificate Features

The system extracts the following features from a real certificate:

- validity_days
- days_remaining
- key_size
- self_signed
- is_ca
- issuer_length

These features are passed into a trained ML model to produce a risk score between 0.0 and 1.0.

---

## Installation (Local Python)

Create virtual environment:

    python3 -m venv venv
    source venv/bin/activate

Install dependencies:

    pip install -r requirements.txt

---

## Generate Test Certificate

Example self-signed certificate:

    openssl req -x509 -nodes -newkey rsa:2048 \
        -keyout server.key \
        -out server.crt \
        -days 365 \
        -subj "/C=SK/ST=Bratislava/O=AI Demo/CN=localhost"

Place certificate here:

    certs/server.crt

---

## Train Model

Train model using sample dataset:

    python src/train.py

This creates:

    model.pkl

---

## Run Metrics Server

Start service:

    python src/metrics_server.py

Metrics exposed at:

    http://localhost:8000/metrics

Example output:

    cert_days_remaining 352
    cert_expiry_risk_score 0.18

---

## Docker Deployment

Build image:

    docker build -t ai-cert-monitor .

Run container:

    docker run -p 8000:8000 \
        -v $(pwd)/certs:/app/certs \
        ai-cert-monitor

Metrics endpoint:

    http://localhost:8000/metrics

---

## Configuration

The service expects:

    certs/server.crt
    model.pkl

To monitor a different certificate, modify:

    run_metrics("certs/server.crt")

in:

    src/metrics_server.py

Optional improvement: pass certificate path as environment variable.

Example:

    docker run -p 8000:8000 \
        -e CERT_PATH=certs/custom.crt \
        ai-cert-monitor

---

## Prometheus Integration

Example scrape configuration:

    scrape_configs:
      - job_name: 'cert_ai_monitor'
        static_configs:
          - targets: ['localhost:8000']

---

## Example Alert Rule

    alert: CertificateHighRisk
    expr: cert_expiry_risk_score > 0.7
    for: 5m

---

## CI Integration

Pipeline runs:

- Unit tests
- Model validation
- Build validation

---

## Security Considerations

- No private keys are processed
- Certificate file is read-only
- No secrets stored in repository
- Designed for runtime-only parsing

---

## Use Cases

- Enterprise certificate lifecycle management
- DevSecOps monitoring
- Predictive infrastructure operations
- Kubernetes ingress certificate monitoring
- Internal PKI risk assessment

---

## Future Improvements

- Multi-certificate directory scan
- REST API (FastAPI)
- Grafana dashboard
- Kubernetes deployment (Helm)
- OpenTelemetry export
- Azure Key Vault integration
- Auto retraining pipeline

---

## Author

Gabriel  
DevOps & Network Automation Engineer
