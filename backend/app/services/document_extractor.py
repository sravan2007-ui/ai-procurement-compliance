from app.schemas.gst import GSTExtractedData
from app.schemas.pan import PANExtractedData
from app.schemas.udyam import UdyamExtractedData
from app.schemas.income_tax import IncomeTaxExtractedData
from app.schemas.epfo import EPFOExtractedData
from app.schemas.esic import ESICExtractedData
from app.schemas.startup_india import StartupIndiaExtractedData

def get_extraction_schema(document_type: str):
    if document_type == "GST_CERTIFICATE":
        return GSTExtractedData

    if document_type == "PAN":
        return PANExtractedData

    if document_type == "UDYAM_CERTIFICATE":
        return UdyamExtractedData

    if document_type == "INCOME_TAX":
        return IncomeTaxExtractedData

    if document_type == "EPFO":
        return EPFOExtractedData

    if document_type == "ESIC":
        return ESICExtractedData

    if document_type == "STARTUP_INDIA":
        return StartupIndiaExtractedData

    return None