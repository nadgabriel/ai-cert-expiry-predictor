from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime


def parse_certificate(cert_path: str) -> dict:
    with open(cert_path, "rb") as f:
        cert_data = f.read()

    cert = x509.load_pem_x509_certificate(cert_data, default_backend())

    not_before = cert.not_valid_before
    not_after = cert.not_valid_after
    now = datetime.utcnow()

    validity_days = (not_after - not_before).days
    days_remaining = (not_after - now).days

    public_key = cert.public_key()
    key_size = public_key.key_size if isinstance(public_key, rsa.RSAPublicKey) else 0

    self_signed = int(cert.issuer == cert.subject)

    try:
        basic_constraints = cert.extensions.get_extension_for_class(
            x509.BasicConstraints
        ).value
        is_ca = int(basic_constraints.ca)
    except Exception:
        is_ca = 0

    signature_algo = cert.signature_hash_algorithm.name

    issuer_length = len(cert.issuer.rfc4514_string())

    return {
        "validity_days": validity_days,
        "days_remaining": days_remaining,
        "key_size": key_size,
        "self_signed": self_signed,
        "is_ca": is_ca,
        "issuer_length": issuer_length
    }
