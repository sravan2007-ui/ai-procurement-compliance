import re


class PANValidator:
    """Validate the basic structural format of a PAN."""

    PAN_PATTERN = re.compile(r"^[A-Z]{5}[0-9]{4}[A-Z]$")

    def validate(self, pan: str | None) -> bool:
        if not pan:
            return False

        normalized_pan = pan.strip().upper()

        return bool(self.PAN_PATTERN.fullmatch(normalized_pan))