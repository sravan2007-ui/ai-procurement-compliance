from pydantic import BaseModel


class StartupIndiaExtractedData(BaseModel):
    certificate_number: str | None = None
    startup_name: str | None = None
    recognition_date: str | None = None
    entity_type: str | None = None
    pan_number: str | None = None
    validity_status: str | None = None