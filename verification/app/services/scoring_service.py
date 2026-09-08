import json
from pathlib import Path
from typing import List
from app.schemas.enums import VerificationStatus
from app.schemas.verification_result import VerificationResult

CONFIG_PATH = Path(__file__).resolve().parents[2] / "rules-data" / "scoring-config.json"

with open(CONFIG_PATH) as f:
    _CONFIG = json.load(f)

WEIGHTS = _CONFIG["weights"]


def calculate_score(results: List[VerificationResult]) -> float:
    """
    Weighted average score. NOT_APPLICABLE checks are excluded from both
    the numerator and denominator so they don't unfairly drag the score down.
    A rule's own `.score` (0-100) is scaled by its weight.
    """
    # If blacklisted, wipe out the entire score
    if any(r.check_type == "BLACKLIST" and r.status == VerificationStatus.FAIL for r in results):
        return 0.0
    total_weight = 0.0
    earned = 0.0

    for result in results:
        weight = WEIGHTS.get(result.check_type, 0)
        if result.status == VerificationStatus.NOT_APPLICABLE or weight == 0:
            continue
        total_weight += weight
        earned += (result.score / 100.0) * weight

    if total_weight == 0:
        return 0.0

    return round((earned / total_weight) * 100, 2)
