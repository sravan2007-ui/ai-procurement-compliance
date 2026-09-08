from app.models.consistency import (
    ConsistencyCheckResult,
    ConsistencyStatus,
)


def test_consistency_check_result():
    result = ConsistencyCheckResult(
        status=ConsistencyStatus.CONSISTENT,
        field="company_name",
        message="Company names match across submitted documents.",
        evidence={
            "gst_name": "ABC Pvt Ltd",
            "udyam_name": "ABC Pvt Ltd",
        },
        confidence=0.98,
    )

    assert result.status == ConsistencyStatus.CONSISTENT
    assert result.field == "company_name"
    assert result.evidence["gst_name"] == "ABC Pvt Ltd"