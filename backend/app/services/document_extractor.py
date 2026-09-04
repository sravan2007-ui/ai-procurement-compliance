from app.schemas.gst import GSTExtractedData
from app.schemas.pan import PANExtractedData


def get_extraction_schema(document_type: str):
    """
    Return the structured extraction schema
    for the given document type.
    """

    if document_type == "GST_CERTIFICATE":
        return GSTExtractedData

    if document_type == "PAN":
        return PANExtractedData

    return None