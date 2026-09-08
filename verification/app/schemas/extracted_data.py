"""
These schemas mirror the AI engine's document-extraction output exactly
(field-for-field), so the Verification Engine can consume its JSON
without any translation layer at the integration boundary.
"""
from typing import Optional
from pydantic import BaseModel


class GSTExtractedData(BaseModel):
    gstin: Optional[str] = None
    legal_name: Optional[str] = None
    trade_name: Optional[str] = None
    registration_date: Optional[str] = None
    business_type: Optional[str] = None
    status: Optional[str] = None
    principal_place_of_business: Optional[str] = None


class PANExtractedData(BaseModel):
    pan_number: Optional[str] = None
    name: Optional[str] = None
    father_name: Optional[str] = None
    date_of_birth: Optional[str] = None


class UdyamExtractedData(BaseModel):
    udyam_number: Optional[str] = None
    enterprise_name: Optional[str] = None
    organisation_type: Optional[str] = None
    major_activity: Optional[str] = None
    social_category: Optional[str] = None
    date_of_incorporation: Optional[str] = None
    date_of_udyam_registration: Optional[str] = None
    enterprise_type: Optional[str] = None


class EPFOExtractedData(BaseModel):
    establishment_id: Optional[str] = None
    establishment_name: Optional[str] = None
    employer_name: Optional[str] = None
    registration_date: Optional[str] = None
    contribution_status: Optional[str] = None
    compliance_period: Optional[str] = None


class ESICExtractedData(BaseModel):
    employer_code: Optional[str] = None
    establishment_name: Optional[str] = None
    employer_name: Optional[str] = None
    registration_date: Optional[str] = None
    contribution_status: Optional[str] = None
    compliance_period: Optional[str] = None


class IncomeTaxExtractedData(BaseModel):
    pan_number: Optional[str] = None
    taxpayer_name: Optional[str] = None
    assessment_year: Optional[str] = None
    filing_status: Optional[str] = None
    return_filing_date: Optional[str] = None
    gross_total_income: Optional[str] = None
    taxable_income: Optional[str] = None


class StartupIndiaExtractedData(BaseModel):
    certificate_number: Optional[str] = None
    startup_name: Optional[str] = None
    recognition_date: Optional[str] = None
    entity_type: Optional[str] = None
    pan_number: Optional[str] = None
    validity_status: Optional[str] = None
