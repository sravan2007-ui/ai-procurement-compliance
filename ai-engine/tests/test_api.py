import app.api.routes as routes
from fastapi.testclient import TestClient

from app.main import app
from app.services.gemini_client import GeminiServiceError


class FailingGraph:
    def invoke(self, state):
        raise GeminiServiceError(
            "Gemini service is currently unavailable."
        )


def test_analyze_returns_503_when_gemini_unavailable(monkeypatch):
    monkeypatch.setattr(
        routes,
        "build_compliance_graph",
        lambda: FailingGraph(),
    )

    client = TestClient(app)

    response = client.post(
        "/api/analyze",
        json={
            "tender_text": "GST registration must be active.",
            "bidder_data": {},
        },
    )

    assert response.status_code == 503

    assert response.json() == {
        "detail": "Gemini service is currently unavailable."
    }


def test_analyze_empty_tender_returns_422():
    client = TestClient(app)

    response = client.post(
        "/api/analyze",
        json={
            "tender_text": "   ",
            "bidder_data": {},
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "Tender text is required."


def test_analyze_happy_path(monkeypatch):
    from app.models.assessment import ComplianceAssessment, RiskLevel
    from app.models.compliance import ComplianceResult, ComplianceStatus
    from app.models.evidence import ComplianceEvidence

    fake_assessment = ComplianceAssessment(
        overall_score=100.0,
        risk_level=RiskLevel.LOW,
        pass_count=1,
        fail_count=0,
        review_count=0,
        conflict_count=0,
        results=[
            ComplianceResult(
                rule_id="GST-001",
                status=ComplianceStatus.PASS,
                message="GST status is ACTIVE.",
                evidence={},
                confidence=1.0,
            )
        ],
        evidence=[
            ComplianceEvidence(
                rule_id="GST-001",
                items=[],
                summary="GST registration active and verified.",
            )
        ],
        recommendation="Recommended for approval.",
    )

    class FakeGraph:
        def invoke(self, state):
            return {
                "assessment": fake_assessment,
                "error": None,
            }

    monkeypatch.setattr(
        routes,
        "build_compliance_graph",
        lambda: FakeGraph(),
    )

    client = TestClient(app)
    response = client.post(
        "/api/analyze",
        json={
            "tender_text": "GST must be active.",
            "bidder_data": {
                "GST_STATUS": {
                    "gstin": "29ABCDE1234F1Z5",
                    "legal_name": "ABC Tech",
                    "status": "ACTIVE",
                    "confidence": 0.99,
                }
            },
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "assessment" in data
    assert data["assessment"]["overall_score"] == 100.0
    assert data["assessment"]["risk_level"] == "LOW"