from fastapi import APIRouter, HTTPException

from app.api.schemas import (
    ComplianceAnalysisRequest,
    ComplianceAnalysisResponse,
)
from app.models.experience import ExperienceDocument
from app.models.financial import FinancialDocument
from app.models.gst import GSTDocument
from app.models.udyam import UdyamDocument
from app.services.gemini_client import GeminiServiceError
from app.services.workflow.graph import build_compliance_graph

router = APIRouter(
    prefix="/api",
    tags=["AI Analysis"],
)


@router.post("/analyze", response_model=ComplianceAnalysisResponse)
def analyze_compliance(
    request: ComplianceAnalysisRequest,
) -> ComplianceAnalysisResponse:
    bidder_data = dict(request.bidder_data)

    if "GST_STATUS" in bidder_data:
        bidder_data["GST_STATUS"] = GSTDocument.model_validate(
            bidder_data["GST_STATUS"]
        )

    if "UDYAM_ELIGIBILITY" in bidder_data:
        bidder_data["UDYAM_ELIGIBILITY"] = UdyamDocument.model_validate(
            bidder_data["UDYAM_ELIGIBILITY"]
        )

    if "MIN_AVERAGE_TURNOVER" in bidder_data:
        bidder_data["MIN_AVERAGE_TURNOVER"] = (
            FinancialDocument.model_validate(
                bidder_data["MIN_AVERAGE_TURNOVER"]
            )
        )

    if "EXPERIENCE_REQUIREMENT" in bidder_data:
        bidder_data["EXPERIENCE_REQUIREMENT"] = (
            ExperienceDocument.model_validate(
                bidder_data["EXPERIENCE_REQUIREMENT"]
            )
        )

    graph = build_compliance_graph()

    try:
        result = graph.invoke(
            {
                "tender_text": request.tender_text,
                "bidder_data": bidder_data,
                "reference_date": (
                    request.reference_date.isoformat()
                    if request.reference_date is not None
                    else None
                ),
            }
        )
    except GeminiServiceError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    if result.get("error"):
        error_msg = result["error"]
        if (
            "503" in error_msg
            or "Gemini service" in error_msg
            or "unavailable" in error_msg.lower()
        ):
            raise HTTPException(
                status_code=503,
                detail=error_msg,
            )
        raise HTTPException(
            status_code=422,
            detail=error_msg,
        )

    assessment = result.get("assessment")

    if assessment is None:
        raise HTTPException(
            status_code=422,
            detail="Compliance assessment could not be generated.",
        )

    return ComplianceAnalysisResponse(
        assessment=assessment,
    )