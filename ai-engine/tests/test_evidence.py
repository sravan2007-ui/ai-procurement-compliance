from app.models.evidence import (
    ComplianceEvidence,
    EvidenceItem,
    EvidenceSourceType,
)


def test_evidence_item_creation():
    evidence = EvidenceItem(
        source_type=EvidenceSourceType.DOCUMENT,
        source_name="GST Certificate",
        document_id="DOC-001",
        field="gstin",
        value="29ABCDE1234F1Z5",
        description="GSTIN extracted from the submitted GST certificate.",
    )

    assert evidence.source_type == EvidenceSourceType.DOCUMENT
    assert evidence.source_name == "GST Certificate"
    assert evidence.document_id == "DOC-001"
    assert evidence.field == "gstin"
    assert evidence.value == "29ABCDE1234F1Z5"
    assert evidence.collected_at is not None


def test_compliance_evidence_creation():
    evidence = ComplianceEvidence(
        rule_id="GST_001",
        items=[
            EvidenceItem(
                source_type=EvidenceSourceType.DOCUMENT,
                source_name="GST Certificate",
                field="status",
                value="Active",
                description="Status extracted from submitted document.",
            ),
            EvidenceItem(
                source_type=EvidenceSourceType.VERIFICATION_SOURCE,
                source_name="GST Verification Service",
                field="status",
                value="Active",
                description="Status returned by verification source.",
            ),
        ],
        summary="Submitted document and verification source both show Active GST status.",
    )

    assert evidence.rule_id == "GST_001"
    assert len(evidence.items) == 2
    assert evidence.items[0].value == "Active"
    assert evidence.items[1].source_type == (
        EvidenceSourceType.VERIFICATION_SOURCE
    )


def test_compliance_evidence_defaults_to_empty_items():
    evidence = ComplianceEvidence(
        rule_id="TURNOVER_001",
        summary="Turnover evidence is available.",
    )

    assert evidence.items == []