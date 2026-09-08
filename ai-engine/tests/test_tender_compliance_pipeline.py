from app.models.tender_requirement import TenderRequirementSet
from app.services.tender_compliance_pipeline import (
    TenderCompliancePipeline,
)
from app.models.gst import GSTDocument
from app.models.udyam import UdyamDocument
from app.services.verification.mock_gst import MockGSTVerificationAdapter

class FakeRequirementExtractor:
    def __init__(self, requirements: TenderRequirementSet) -> None:
        self.requirements = requirements
        self.received_text = None

    def extract(self, tender_text: str) -> TenderRequirementSet:
        self.received_text = tender_text
        return self.requirements


def test_pipeline_evaluates_gst_requirement():
    requirements = TenderRequirementSet(
        requirements=[
            {
                "rule_id": "GST_001",
                "name": "GST Status",
                "description": "GST registration must be active.",
                "rule_type": "GST_STATUS",
                "parameters": {
                    "required_status": "Active",
                },
                "mandatory": True,
            }
        ]
    )

    extractor = FakeRequirementExtractor(requirements)

    pipeline = TenderCompliancePipeline(
        requirement_extractor=extractor,
    )

    assessment = pipeline.process(
        tender_text="GST registration must be active.",
        bidder_data={
    "GST_STATUS": GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Private Limited",
        status="Active",
        confidence=1.0,
    )
},
    )

    assert extractor.received_text == (
        "GST registration must be active."
    )
    assert len(assessment.results) == 1
    assert assessment.pass_count == 1
    assert assessment.fail_count == 0
    assert assessment.review_count == 0
    assert assessment.conflict_count == 0
    assert assessment.overall_score == 100.0
    assert "passed" in assessment.recommendation


def test_pipeline_detects_failed_gst_requirement():
    requirements = TenderRequirementSet(
        requirements=[
            {
                "rule_id": "GST_001",
                "name": "GST Status",
                "description": "GST registration must be active.",
                "rule_type": "GST_STATUS",
                "parameters": {
                    "required_status": "Active",
                },
                "mandatory": True,
            }
        ]
    )

    pipeline = TenderCompliancePipeline(
        requirement_extractor=FakeRequirementExtractor(
            requirements
        ),
    )

    assessment = pipeline.process(
        tender_text="GST registration must be active.",
        bidder_data={
    "GST_STATUS": GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Private Limited",
        status="Cancelled",
        confidence=1.0,
    )
},
    )

    assert len(assessment.results) == 1
    assert assessment.pass_count == 0
    assert assessment.fail_count == 1
    assert assessment.risk_level.value == "HIGH"
    assert "failed" in assessment.recommendation


def test_pipeline_handles_multiple_requirements():
    requirements = TenderRequirementSet(
        requirements=[
            {
                "rule_id": "GST_001",
                "name": "GST Status",
                "description": "GST must be active.",
                "rule_type": "GST_STATUS",
                "parameters": {
                    "required_status": "Active",
                },
            },
            {
                "rule_id": "UDYAM_001",
                "name": "Udyam Eligibility",
                "description": "Bidder must have eligible Udyam classification.",
                "rule_type": "UDYAM_ELIGIBILITY",
                "parameters": {
                    "allowed_types": ["Micro", "Small", "Medium"],
                },
            },
        ]
    )

    pipeline = TenderCompliancePipeline(
        requirement_extractor=FakeRequirementExtractor(
            requirements
        ),
    )

    assessment = pipeline.process(
        tender_text="GST and Udyam requirements.",
        bidder_data={
    "GST_STATUS": GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Private Limited",
        status="Active",
        confidence=1.0,
    ),
    "UDYAM_ELIGIBILITY": UdyamDocument(
        udyam_number="UDYAM-AP-01-0000001",
        enterprise_name="ABC Private Limited",
        enterprise_type="Small",
        confidence=1.0,
    ),
},
    )

    assert len(assessment.results) == 2
    assert assessment.pass_count == 2
    assert assessment.fail_count == 0
    assert assessment.review_count == 0
    assert assessment.conflict_count == 0
    assert assessment.overall_score == 100.0

def test_pipeline_builds_evidence_for_each_requirement():
    requirements = TenderRequirementSet(
        requirements=[
            {
                "rule_id": "GST_001",
                "name": "GST Status",
                "description": "GST must be active.",
                "rule_type": "GST_STATUS",
                "parameters": {
                    "required_status": "Active",
                },
            },
        ]
    )

    pipeline = TenderCompliancePipeline(
        requirement_extractor=FakeRequirementExtractor(
            requirements
        ),
    )

    assessment = pipeline.process(
        tender_text="GST must be active.",
        bidder_data={
            "GST_STATUS": GSTDocument(
                gstin="29ABCDE1234F1Z5",
                legal_name="ABC Private Limited",
                status="Active",
                confidence=1.0,
            ),
        },
    )

    assert len(assessment.results) == 1
    assert len(assessment.evidence) == 1
    assert assessment.evidence[0].rule_id == "GST_001"
    assert len(assessment.evidence[0].items) > 0

def test_pipeline_detects_gst_verification_conflict():
    requirements = TenderRequirementSet(
        requirements=[
            {
                "rule_id": "GST_001",
                "name": "GST Status",
                "description": "GST must be active.",
                "rule_type": "GST_STATUS",
                "parameters": {
                    "required_status": "Active",
                },
            }
        ]
    )

    verification_adapter = MockGSTVerificationAdapter(
        records={
            "29ABCDE1234F1Z5": {
                "gstin": "29ABCDE1234F1Z5",
                "legal_name": "ABC Private Limited",
                "status": "Cancelled",
            }
        }
    )

    pipeline = TenderCompliancePipeline(
        requirement_extractor=FakeRequirementExtractor(
            requirements
        ),
        verification_adapter=verification_adapter,
    )

    assessment = pipeline.process(
        tender_text="GST must be active.",
        bidder_data={
            "GST_STATUS": GSTDocument(
                gstin="29ABCDE1234F1Z5",
                legal_name="ABC Private Limited",
                status="Active",
                confidence=1.0,
            ),
        },
    )

    assert len(assessment.results) == 1
    assert assessment.results[0].status.value == "CONFLICT"

    assert assessment.conflict_count == 1
    assert assessment.risk_level.value == "HIGH"

    assert len(assessment.evidence) == 1

    verification_items = [
        item
        for item in assessment.evidence[0].items
        if item.source_type.value == "VERIFICATION_SOURCE"
    ]

    assert len(verification_items) > 0

    assert any(
        item.field == "status"
        and item.value == "Cancelled"
        for item in verification_items
    )

    assert any(
        item.field == "verification_status"
        and item.value == "CONFLICT"
        for item in verification_items
    )

    assert "review required" in assessment.recommendation


def test_pipeline_evaluates_required_document_requirement():
    requirements = TenderRequirementSet(
        requirements=[
            {
                "rule_id": "DOC_GST_001",
                "name": "GST Certificate Required",
                "description": "Bidder must submit a GST certificate.",
                "rule_type": "REQUIRED_DOCUMENT",
                "parameters": {
                    "document_type": "GST_CERTIFICATE",
                },
                "mandatory": True,
            }
        ]
    )

    pipeline = TenderCompliancePipeline(
        requirement_extractor=FakeRequirementExtractor(
            requirements
        ),
    )

    assessment = pipeline.process(
        tender_text="Bidder must submit a GST certificate.",
        bidder_data={
            "REQUIRED_DOCUMENT": [
                {
                    "document_type": "GST_CERTIFICATE",
                },
                {
                    "document_type": "FINANCIAL_STATEMENT",
                },
            ],
        },
    )

    assert len(assessment.results) == 1
    assert assessment.results[0].rule_id == "DOC_GST_001"
    assert assessment.results[0].status.value == "PASS"

    assert assessment.pass_count == 1
    assert assessment.fail_count == 0
    assert assessment.review_count == 0
    assert assessment.conflict_count == 0
    assert assessment.overall_score == 100.0

def test_pipeline_evaluates_experience_requirement():
    requirements = TenderRequirementSet(
        requirements=[
            {
                "rule_id": "EXP_001",
                "name": "Relevant Experience",
                "description": "Bidder must have qualifying refinery projects.",
                "rule_type": "EXPERIENCE_REQUIREMENT",
                "parameters": {
                    "minimum_projects": 2,
                    "minimum_project_value": 5,
                    "project_type": "Refinery",
                },
                "mandatory": True,
            }
        ]
    )

    from app.models.experience import (
        ExperienceDocument,
        ExperienceProject,
    )

    pipeline = TenderCompliancePipeline(
        requirement_extractor=FakeRequirementExtractor(
            requirements
        ),
    )

    assessment = pipeline.process(
        tender_text="Bidder must have relevant refinery experience.",
        bidder_data={
            "EXPERIENCE_REQUIREMENT": ExperienceDocument(
                company_name="ABC Pvt Ltd",
                projects=[
                    ExperienceProject(
                        project_name="Refinery Upgrade",
                        client_name="Client A",
                        project_type="Refinery",
                        project_value=7.5,
                        completion_date="2025-03-31",
                    ),
                    ExperienceProject(
                        project_name="Refinery Expansion",
                        client_name="Client B",
                        project_type="Refinery",
                        project_value=6.0,
                        completion_date="2025-06-30",
                    ),
                ],
                document_type="EXPERIENCE_CERTIFICATE",
                confidence=0.95,
            ),
        },
    )

    assert len(assessment.results) == 1
    assert assessment.results[0].rule_id == "EXP_001"
    assert assessment.results[0].status.value == "PASS"

    assert assessment.pass_count == 1
    assert assessment.fail_count == 0
    assert assessment.review_count == 0
    assert assessment.conflict_count == 0
    assert assessment.overall_score == 100.0