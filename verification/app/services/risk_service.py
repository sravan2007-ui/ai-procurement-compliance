import json
from pathlib import Path
from typing import List
from app.schemas.enums import RiskLevel, VerificationStatus
from app.schemas.verification_result import VerificationResult

CONFIG_PATH = Path(__file__).resolve().parents[2] / "rules-data" / "scoring-config.json"

with open(CONFIG_PATH) as f:
    _CONFIG = json.load(f)

THRESHOLDS = _CONFIG["risk_thresholds"]
MANDATORY_CHECKS = set(_CONFIG.get("mandatory_checks", []))


def calculate_risk(results: List[VerificationResult], score: float) -> RiskLevel:
    # Hard override: failure on a mandatory check (e.g. blacklist) is always CRITICAL,
    # regardless of how high the overall score is.
    for result in results:
        if result.check_type in MANDATORY_CHECKS and result.status == VerificationStatus.FAIL:
            return RiskLevel.CRITICAL

    if score >= THRESHOLDS["LOW"]:
        return RiskLevel.LOW
    if score >= THRESHOLDS["MEDIUM"]:
        return RiskLevel.MEDIUM
    if score >= THRESHOLDS["HIGH"]:
        return RiskLevel.HIGH
    return RiskLevel.CRITICAL
