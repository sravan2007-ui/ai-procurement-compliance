from app.schemas.enums import VerificationStatus
from app.schemas.verification_result import VerificationResult


def verify_local_content(extracted, bidder, requirements) -> VerificationResult:
    # Check if tender requires a minimum local content percentage
    min_required = getattr(requirements, "minimum_local_content_percentage", 0) or 0
    if min_required <= 0:
        return VerificationResult(
            check_type="LOCAL_CONTENT",
            status=VerificationStatus.NOT_APPLICABLE,
            message="Local content (Make in India) verification not required for this tender.",
            score=0,
            evidence={},
        )

    declared_percentage = getattr(bidder, "local_content_percentage", None)

    # If not declared or negative
    if declared_percentage is None or declared_percentage < 0:
        return VerificationResult(
            check_type="LOCAL_CONTENT",
            status=VerificationStatus.FAIL,
            message="Missing or invalid Make in India local content self-declaration.",
            score=0,
            evidence={"declared_percentage": declared_percentage, "required_percentage": min_required},
        )

    # Class-I vs Class-II / Threshold checks
    if declared_percentage >= min_required:
        supplier_class = "Class-I Local Supplier" if declared_percentage >= 50 else "Class-II Local Supplier"
        return VerificationResult(
            check_type="LOCAL_CONTENT",
            status=VerificationStatus.PASS,
            message=f"Bidder complies with Make in India policy as a {supplier_class} ({declared_percentage}% >= {min_required}% required).",
            score=100,
            evidence={
                "declared_percentage": declared_percentage,
                "required_percentage": min_required,
                "supplier_class": supplier_class,
            },
        )

    # Fails required threshold
    return VerificationResult(
        check_type="LOCAL_CONTENT",
        status=VerificationStatus.FAIL,
        message=(
            f"Non-compliant local content: Declared {declared_percentage}% falls below the "
            f"minimum required {min_required}% threshold."
        ),
        score=0,
        evidence={
            "declared_percentage": declared_percentage,
            "required_percentage": min_required,
        },
    )