from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class DocumentType(str, Enum):
    GST_CERTIFICATE = "GST_CERTIFICATE"
    PAN = "PAN"
    UDYAM_CERTIFICATE = "UDYAM_CERTIFICATE"
    INCOME_TAX = "INCOME_TAX"
    EPFO = "EPFO"
    ESIC = "ESIC"
    STARTUP_INDIA = "STARTUP_INDIA"
    NSIC = "NSIC"
    OEM_AUTHORIZATION = "OEM_AUTHORIZATION"
    MAKE_IN_INDIA = "MAKE_IN_INDIA"
    EXPERIENCE_CERTIFICATE = "EXPERIENCE_CERTIFICATE"
    OTHER = "OTHER"


class BidDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    bid_id: int
    document_type: DocumentType
    file_name: str
    file_path: str
    mime_type: str
    status: str
    uploaded_at: datetime