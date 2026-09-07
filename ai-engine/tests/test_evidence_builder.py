from app.models.compliance import ComplianceResult, ComplianceStatus
from app.models.gst import GSTDocument
from app.models.evidence import EvidenceSourceType
from app.services.evidence_builder import EvidenceBuilder
from app.models.verification import (
    VerificationResult,
    VerificationStatus,
)

def test_evidence_builder_creates_document_and_rule_evidence():
    result = ComplianceResult(
        rule_id="GST_001",
        status=ComplianceStatus.PASS,
        message="GST status is active.",
        evidence={
            "gstin": "29ABCDE1234F1Z5",
            "actual_status": "Active",
        },
        confidence=1.0,
    )

    document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Private Limited",
        status="Active",
        confidence=1.0,
    )

    evidence = EvidenceBuilder().build(
        result,
        document,
    )

    assert evidence.rule_id == "GST_001"
    assert len(evidence.items) == 7

    document_items = [
        item
        for item in evidence.items
        if item.source_type == EvidenceSourceType.DOCUMENT
    ]

    rule_items = [
        item
        for item in evidence.items
        if item.source_type == EvidenceSourceType.RULE_ENGINE
    ]

    assert len(document_items) == 6
    assert len(rule_items) == 1
    assert rule_items[0].value == "PASS"


def test_evidence_builder_handles_missing_data():
    result = ComplianceResult(
        rule_id="GST_001",
        status=ComplianceStatus.REVIEW_REQUIRED,
        message="GST verification requires review.",
        confidence=0.5,
    )

    evidence = EvidenceBuilder().build(result)

    assert evidence.rule_id == "GST_001"
    assert len(evidence.items) == 1
    assert evidence.items[0].source_type == (
        EvidenceSourceType.RULE_ENGINE
    )
    assert evidence.items[0].value == "REVIEW_REQUIRED"


def test_evidence_builder_skips_raw_text_and_warnings():
    result = ComplianceResult(
        rule_id="GST_001",
        status=ComplianceStatus.PASS,
        message="GST status is active.",
        confidence=1.0,
    )

    document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Private Limited",
        status="Active",
        raw_text="Large source document text...",
        warnings=["Low OCR quality"],
        confidence=0.9,
    )

    evidence = EvidenceBuilder().build(
        result,
        document,
    )

    fields = {
        item.field
        for item in evidence.items
        if item.source_type == EvidenceSourceType.DOCUMENT
    }

    assert "raw_text" not in fields
    assert "warnings" not in fields
    assert "confidence" not in fields
    assert "gstin" in fields
    assert "legal_name" in fields
    assert "status" in fields


def test_evidence_builder_includes_verified_source():
    result = ComplianceResult(
        rule_id="GST_001",
        status=ComplianceStatus.PASS,
        message="GST status is active.",
        confidence=1.0,
    )

    verification = VerificationResult(
        status=VerificationStatus.VERIFIED,
        source="Mock GST Verification Service",
        message="GST record verified successfully.",
        verified_data={
            "gstin": "29ABCDE1234F1Z5",
            "legal_name": "ABC Private Limited",
            "status": "Active",
        },
        confidence=1.0,
    )

    evidence = EvidenceBuilder().build(
        result,
        verification=verification,
    )

    verification_items = [
        item
        for item in evidence.items
        if item.source_type
        == EvidenceSourceType.VERIFICATION_SOURCE
    ]

    assert len(verification_items) == 4
    assert verification_items[0].source_name == (
        "Mock GST Verification Service"
    )
    assert verification_items[0].value == "29ABCDE1234F1Z5"
    assert verification_items[-1].field == "verification_status"
    assert verification_items[-1].value == "VERIFIED"


def test_evidence_builder_includes_conflicting_source():
    result = ComplianceResult(
        rule_id="GST_001",
        status=ComplianceStatus.CONFLICT,
        message="GST status conflicts with verified source.",
        confidence=1.0,
    )

    verification = VerificationResult(
        status=VerificationStatus.CONFLICT,
        source="Mock GST Verification Service",
        message="Document and verified GST status do not match.",
        verified_data={
            "gstin": "29ABCDE1234F1Z5",
            "status": "Cancelled",
            "conflicting_fields": "status",
        },
        confidence=1.0,
    )

    evidence = EvidenceBuilder().build(
        result,
        verification=verification,
    )

    verification_items = [
        item
        for item in evidence.items
        if item.source_type
        == EvidenceSourceType.VERIFICATION_SOURCE
    ]

    assert len(verification_items) == 4
    assert any(
        item.field == "status" and item.value == "Cancelled"
        for item in verification_items
    )
    assert any(
        item.field == "verification_status"
        and item.value == "CONFLICT"
        for item in verification_items
    )