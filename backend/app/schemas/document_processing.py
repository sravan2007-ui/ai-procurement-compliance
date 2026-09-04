from typing import Any

from pydantic import BaseModel


class DocumentProcessingResponse(BaseModel):
    document_id: int
    status: str
    extracted_text: str
    extracted_data: dict[str, Any] | None = None