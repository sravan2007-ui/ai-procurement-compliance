from app.services.pan_validator import PANValidator


def test_pan_validator_accepts_valid_pan():
    validator = PANValidator()

    assert validator.validate("ABCDE1234F") is True


def test_pan_validator_accepts_lowercase_pan():
    validator = PANValidator()

    assert validator.validate("abcde1234f") is True


def test_pan_validator_rejects_invalid_pan():
    validator = PANValidator()

    assert validator.validate("ABCDE12345") is False
    assert validator.validate("ABCD1234F") is False
    assert validator.validate("12345ABCDE") is False


def test_pan_validator_rejects_empty_pan():
    validator = PANValidator()

    assert validator.validate(None) is False
    assert validator.validate("") is False
    assert validator.validate("   ") is False