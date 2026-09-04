from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class DocumentExtractionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    document_id: int
    document_type: str
    extracted_data: dict[str, Any] | None
    extraction_status: str
    model_name: str | None
    created_at: datetime