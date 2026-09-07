import re


class GSTINValidator:
    """Validate the basic structural format of a GSTIN."""

    GSTIN_PATTERN = re.compile(
        r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"
    )

    def validate(self, gstin: str | None) -> bool:
        if not gstin:
            return False

        normalized_gstin = gstin.strip().upper()

        return bool(self.GSTIN_PATTERN.fullmatch(normalized_gstin))