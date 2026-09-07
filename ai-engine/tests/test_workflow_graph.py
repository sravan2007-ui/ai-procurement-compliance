from app.models.gst import GSTDocument
from app.models.tender_requirement import (
    TenderRequirement,
    TenderRequirementSet,
)
from app.services.verification.mock_gst import (
    MockGSTVerificationAdapter,
)
from app.services.workflow.graph import build_compliance_graph
from app.models.financial import (
    FinancialDocument,
    FinancialYearTurnover,
)
class FakeRequirementExtractor:
    """Return deterministic requirements without calling Gemini."""

    def extract(self, tender_text: str) -> TenderRequirementSet:
        return TenderRequirementSet(
            requirements=[
                TenderRequirement(
                    rule_id="GST-001",
                    name="Active GST registration",
                    description="Bidder must have active GST registration.",
                    rule_type="GST_STATUS",
                    parameters={"required_status": "ACTIVE"},
                    mandatory=True,
                    source_text=tender_text,
                )
            ]
        )

class FakeRAGService:
    """Return deterministic knowledge without calling the embedding model."""

    def retrieve(self, query: str, limit: int = 5):
        return [
            {
                "id": 17,
                "document_id": 18,
                "content": "A bidder must have a valid GST registration.",
                "chunk_index": 0,
            }
        ]


def test_complete_compliance_graph(monkeypatch):
    """Verify the complete LangGraph workflow."""

    from app.services.workflow.nodes import extract_requirements as module

    monkeypatch.setattr(
        module,
        "TenderRequirementExtractor",
        FakeRequirementExtractor,
    )

    gst_document = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Technologies Private Limited",
        trade_name="ABC Technologies",
        registration_date="2020-01-01",
        status="ACTIVE",
        state="Karnataka",
        raw_text="GST Certificate",
        confidence=0.99,
        warnings=[],
    )

    adapter = MockGSTVerificationAdapter(
        records={
            "29ABCDE1234F1Z5": {
                "legal_name": "ABC Technologies Private Limited",
                "status": "ACTIVE",
            }
        }
    )

    graph = build_compliance_graph(
    verification_adapter=adapter,
    rag_service=FakeRAGService(),
)

    result = graph.invoke(
        {
            "tender_text": "Bidder must have active GST registration.",
            "bidder_data": {
                "GST_STATUS": gst_document,
            },
        }
    )

    assert result["error"] is None

    assert len(result["requirements"]) == 1
    assert result["requirements"][0].rule_type == "GST_STATUS"

    assert len(result["rules"]) == 1
    assert result["rules"][0].rule_type == "GST_STATUS"

    assert len(result["verification_results"]) == 1
    verification = result["verification_results"][
    result["rules"][0].rule_id
]

    assert verification.status.value == "VERIFIED"

    assert len(result["compliance_results"]) == 1
    assert result["compliance_results"][0].status.value == "PASS"

    assessment = result["assessment"]

    assert assessment is not None
    assert assessment.overall_score == 100.0
    assert assessment.pass_count == 1
    assert assessment.fail_count == 0
    assert assessment.conflict_count == 0
    assert assessment.risk_level.value == "LOW"


def test_reference_date_reaches_experience_rule(monkeypatch):
    from datetime import date

    from app.models.experience import (
        ExperienceDocument,
        ExperienceProject,
    )
    from app.services.workflow.nodes import extract_requirements as module

    class ExperienceRequirementExtractor:
        def extract(self, tender_text: str) -> TenderRequirementSet:
            return TenderRequirementSet(
                requirements=[
                    TenderRequirement(
                        rule_id="EXP-001",
                        name="Relevant experience",
                        description="Bidder must have completed an IT project.",
                        rule_type="EXPERIENCE_REQUIREMENT",
                        parameters={
                            "minimum_projects": 1,
                            "project_type": "IT",
                        },
                        mandatory=True,
                        source_text=tender_text,
                    )
                ]
            )

    monkeypatch.setattr(
        module,
        "TenderRequirementExtractor",
        ExperienceRequirementExtractor,
    )

    experience_document = ExperienceDocument(
        company_name="ABC Technologies Private Limited",
        projects=[
            ExperienceProject(
                project_name="Government IT Project",
                client_name="Government Client",
                project_type="IT",
                project_value=10.0,
                completion_date=date(2025, 1, 1),
            )
        ],
        document_type="EXPERIENCE_CERTIFICATE",
        raw_text="Completed government IT project.",
        confidence=0.99,
        warnings=[],
    )

    graph = build_compliance_graph()

    result = graph.invoke(
        {
            "tender_text": "Bidder must have completed an IT project.",
            "bidder_data": {
                "EXPERIENCE_REQUIREMENT": experience_document,
            },
            "reference_date": "2026-09-07",
        }
    )

    assert result["error"] is None

    assert len(result["rules"]) == 1

    rule = result["rules"][0]

    assert rule.rule_type == "EXPERIENCE_REQUIREMENT"
    assert rule.parameters["reference_date"] == "2026-09-07"

    assert len(result["compliance_results"]) == 1
    assert result["compliance_results"][0].status.value == "PASS"

    assessment = result["assessment"]

    assert assessment is not None
    assert assessment.pass_count == 1
    assert assessment.fail_count == 0

def test_gst_verification_works_when_gst_is_not_first_rule(monkeypatch):
    """GST verification must map by rule_id, not rule position."""

    from app.models.gst import GSTDocument
    from app.models.tender_requirement import (
        TenderRequirement,
        TenderRequirementSet,
    )
    from app.services.verification.mock_gst import (
        MockGSTVerificationAdapter,
    )
    from app.services.workflow.graph import build_compliance_graph
    import app.services.workflow.nodes.extract_requirements as extract_module

    fake_requirements = TenderRequirementSet(
        requirements=[
            TenderRequirement(
                rule_id="TURNOVER-001",
                name="Minimum Average Turnover",
                description="Bidder must meet the minimum average turnover.",
                rule_type="MIN_AVERAGE_TURNOVER",
                parameters={
    "minimum": 10,
    "years": ["2023-24", "2024-25", "2025-26"],
},
                mandatory=True,
            ),
            TenderRequirement(
                rule_id="GST-001",
                name="GST Status",
                description="GST registration must be active.",
                rule_type="GST_STATUS",
                parameters={"required_status": "ACTIVE"},
                mandatory=True,
            ),
        ]
    )

    class FakeExtractor:
        def extract(self, tender_text):
            return fake_requirements

    monkeypatch.setattr(
        extract_module,
        "TenderRequirementExtractor",
        FakeExtractor,
    )

    gst_document = GSTDocument(
    gstin="29ABCDE1234F1Z5",
    legal_name="ABC Technologies",
    status="ACTIVE",
    confidence=0.99,
)

    financial_document = FinancialDocument(
    company_name="ABC Technologies",
    financial_years=[
        FinancialYearTurnover(
            financial_year="2023-24",
            turnover=12.0,
        ),
        FinancialYearTurnover(
            financial_year="2024-25",
            turnover=15.0,
        ),
        FinancialYearTurnover(
            financial_year="2025-26",
            turnover=18.0,
        ),
    ],
    document_type="FINANCIAL_STATEMENT",
    confidence=0.99,
)

    bidder_data = {
    "MIN_AVERAGE_TURNOVER": financial_document,
    "GST_STATUS": gst_document,
}

    verification_adapter = MockGSTVerificationAdapter(
        records={
            "29ABCDE1234F1Z5": {
                "legal_name": "ABC Technologies",
                "status": "ACTIVE",
            }
        }
    )

    graph = build_compliance_graph(
        verification_adapter=verification_adapter,
    )

    result = graph.invoke(
        {
            "tender_text": "Turnover and GST requirements.",
            "bidder_data": bidder_data,
        }
    )

    assert result["error"] is None

    assert len(result["rules"]) == 2

    assert result["rules"][0].rule_id == "TURNOVER-001"
    assert result["rules"][1].rule_id == "GST-001"

    assert "GST-001" in result["verification_results"]

    verification = result["verification_results"]["GST-001"]

    assert verification.status.value == "VERIFIED"

    gst_result = result["compliance_results"][1]

    assert gst_result.rule_id == "GST-001"
    assert gst_result.status.value == "PASS"

    assert result["assessment"] is not None
    assert len(result["assessment"].evidence) == 2


def test_workflow_graph_compiles():
    graph = build_compliance_graph()
    assert graph is not None


def test_workflow_graph_handles_missing_verification_adapter(monkeypatch):
    import app.services.workflow.nodes.extract_requirements as extract_module
    from app.models.gst import GSTDocument
    from app.models.tender_requirement import (
        TenderRequirement,
        TenderRequirementSet,
    )

    fake_requirements = TenderRequirementSet(
        requirements=[
            TenderRequirement(
                rule_id="GST-001",
                name="GST Status",
                description="GST registration must be active.",
                rule_type="GST_STATUS",
                parameters={"required_status": "ACTIVE"},
                mandatory=True,
            ),
        ]
    )

    class FakeExtractor:
        def extract(self, tender_text):
            return fake_requirements

    monkeypatch.setattr(
        extract_module,
        "TenderRequirementExtractor",
        FakeExtractor,
    )

    graph = build_compliance_graph(verification_adapter=None)
    result = graph.invoke(
        {
            "tender_text": "GST registration must be active.",
            "bidder_data": {
                "GST_STATUS": GSTDocument(
                    gstin="29ABCDE1234F1Z5",
                    legal_name="ABC Technologies",
                    status="ACTIVE",
                    confidence=0.99,
                )
            },
        }
    )

    assert result["error"] is None
    assert result["verification_results"] == {}
    assert len(result["compliance_results"]) == 1
    assert result["compliance_results"][0].status.value == "PASS"
    assert result["assessment"] is not None


def test_workflow_graph_handles_gst_conflict(monkeypatch):
    import app.services.workflow.nodes.extract_requirements as extract_module
    from app.models.gst import GSTDocument
    from app.models.tender_requirement import (
        TenderRequirement,
        TenderRequirementSet,
    )
    from app.services.verification.mock_gst import MockGSTVerificationAdapter

    fake_requirements = TenderRequirementSet(
        requirements=[
            TenderRequirement(
                rule_id="GST-001",
                name="GST Status",
                description="GST registration must be active.",
                rule_type="GST_STATUS",
                parameters={"required_status": "ACTIVE"},
                mandatory=True,
            ),
        ]
    )

    class FakeExtractor:
        def extract(self, tender_text):
            return fake_requirements

    monkeypatch.setattr(
        extract_module,
        "TenderRequirementExtractor",
        FakeExtractor,
    )

    # Submitted legal name does not match authoritative source
    bidder_gst = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="Fake Name Inc",
        status="ACTIVE",
        confidence=0.95,
    )

    verification_adapter = MockGSTVerificationAdapter(
        records={
            "29ABCDE1234F1Z5": {
                "legal_name": "Authentic Registered Enterprise",
                "status": "ACTIVE",
            }
        }
    )

    graph = build_compliance_graph(verification_adapter=verification_adapter)
    result = graph.invoke(
        {
            "tender_text": "GST must be active.",
            "bidder_data": {"GST_STATUS": bidder_gst},
        }
    )

    assert result["error"] is None
    assert result["compliance_results"][0].status.value == "CONFLICT"
    assessment = result["assessment"]
    assert assessment is not None
    assert assessment.conflict_count == 1
    assert assessment.risk_level.value == "HIGH"


def test_workflow_graph_preserves_extraction_error_on_empty_text():
    graph = build_compliance_graph()
    result = graph.invoke(
        {
            "tender_text": "   ",
            "bidder_data": {},
        }
    )

    assert result["error"] == "Tender text is required."
    assert result.get("assessment") is None


def test_workflow_graph_preserves_custom_extraction_error(monkeypatch):
    import app.services.workflow.nodes.extract_requirements as extract_module

    class FailingExtractor:
        def extract(self, tender_text):
            raise ValueError("Extraction syntax failed due to malformed tender.")

    monkeypatch.setattr(
        extract_module,
        "TenderRequirementExtractor",
        FailingExtractor,
    )

    graph = build_compliance_graph()
    result = graph.invoke(
        {
            "tender_text": "Malformed tender document",
            "bidder_data": {},
        }
    )

    # Must retain original error and NOT overwrite with 'No compliance results are available.'
    assert result["error"] == "Extraction syntax failed due to malformed tender."
    assert result.get("assessment") is None


def test_workflow_graph_handles_missing_bidder_documents_defensively(monkeypatch):
    import app.services.workflow.nodes.extract_requirements as extract_module
    from app.models.tender_requirement import (
        TenderRequirement,
        TenderRequirementSet,
    )

    fake_requirements = TenderRequirementSet(
        requirements=[
            TenderRequirement(
                rule_id="TURNOVER-001",
                name="Minimum Average Turnover",
                description="Bidder must meet the minimum average turnover.",
                rule_type="MIN_AVERAGE_TURNOVER",
                parameters={
                    "minimum": 10,
                    "years": ["2023-24", "2024-25", "2025-26"],
                },
                mandatory=True,
            ),
            TenderRequirement(
                rule_id="GST-001",
                name="GST Status",
                description="GST registration must be active.",
                rule_type="GST_STATUS",
                parameters={"required_status": "ACTIVE"},
                mandatory=True,
            ),
        ]
    )

    class FakeExtractor:
        def extract(self, tender_text):
            return fake_requirements

    monkeypatch.setattr(
        extract_module,
        "TenderRequirementExtractor",
        FakeExtractor,
    )

    # Bidder did not submit any documents (empty bidder_data)
    graph = build_compliance_graph()
    result = graph.invoke(
        {
            "tender_text": "Turnover and GST requirements.",
            "bidder_data": {},
        }
    )

    assert result["error"] is None
    assert len(result["compliance_results"]) == 2
    for cr in result["compliance_results"]:
        assert cr.status.value == "REVIEW_REQUIRED"

    assessment = result["assessment"]
    assert assessment is not None
    assert assessment.review_count == 2
    assert len(assessment.evidence) == 2