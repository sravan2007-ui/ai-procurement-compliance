from pydantic import BaseModel


class PANExtractedData(BaseModel):
    pan_number: str | None = None
    name: str | None = None
    father_name: str | None = None
    date_of_birth: str | None = None