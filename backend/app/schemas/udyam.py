from pydantic import BaseModel


class UdyamExtractedData(BaseModel):
    udyam_number: str | None = None
    enterprise_name: str | None = None
    organisation_type: str | None = None
    major_activity: str | None = None
    social_category: str | None = None
    date_of_incorporation: str | None = None
    date_of_udyam_registration: str | None = None
    enterprise_type: str | None = None