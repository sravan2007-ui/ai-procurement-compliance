from fastapi import APIRouter
from app.schemas.verification_request import VerificationRequest
from app.schemas.verification_result import ComplianceResult
from app.engine import run_verification

router = APIRouter(prefix="/verification", tags=["verification"])


@router.post("/run", response_model=ComplianceResult)
def run(request: VerificationRequest) -> ComplianceResult:
    return run_verification(request)
