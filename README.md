## Real Certificate Parsing

The project extracts real X.509 metadata using the cryptography library:

- Certificate validity period
- Remaining lifetime
- RSA key size
- Self-signed detection
- CA flag detection
- Issuer characteristics

These features are used for predictive risk scoring.

openssl req -x509 -nodes -newkey rsa:2048 \
    -keyout test.key \
    -out test_cert.pem \
    -days 365 \
    -subj "/C=SK/ST=Bratislava/O=AI Demo/CN=localhost"
    
