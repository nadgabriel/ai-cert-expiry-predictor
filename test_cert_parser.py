from cert_parser import parse_certificate

def test_parse_certificate():
    features = parse_certificate("tests/test_cert.pem")

    assert "validity_days" in features
    assert "key_size" in features
    assert features["validity_days"] > 0
