from app.services.gstin_validator import GSTINValidator


def test_gstin_is_valid():
    validator = GSTINValidator()

    assert validator.validate("29ABCDE1234F1Z5") is True


def test_gstin_is_valid_with_lowercase_input():
    validator = GSTINValidator()

    assert validator.validate("29abcde1234f1z5") is True


def test_gstin_is_invalid_when_length_is_wrong():
    validator = GSTINValidator()

    assert validator.validate("29ABCDE1234F1Z") is False


def test_gstin_is_invalid_when_format_is_wrong():
    validator = GSTINValidator()

    assert validator.validate("INVALID-GSTIN") is False


def test_gstin_is_invalid_when_missing():
    validator = GSTINValidator()

    assert validator.validate(None) is False