from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.extracted_data import (
    GSTExtractedData,
    PANExtractedData,
    UdyamExtractedData,
    EPFOExtractedData,
    ESICExtractedData,
    IncomeTaxExtractedData,
    StartupIndiaExtractedData,
)


class TenderRequirements(BaseModel):
    gst_required: bool = False
    pan_required: bool = False
    udyam_required: bool = False
    epfo_required: bool = False
    esic_required: bool = False
    income_tax_required: bool = False
    startup_india_required: bool = False
    blacklist_check_required: bool = True
    minimum_local_content_percentage: Optional[float] = None


class ExtractedData(BaseModel):
    """Bundle of per-document data as produced by the AI extraction engine.
    Each field is optional because a bidder won't upload every document for
    every tender — the corresponding rule treats a missing block as
    'document not provided' rather than crashing."""

    gst: Optional[GSTExtractedData] = None
    pan: Optional[PANExtractedData] = None
    udyam: Optional[UdyamExtractedData] = None
    epfo: Optional[EPFOExtractedData] = None
    esic: Optional[ESICExtractedData] = None
    income_tax: Optional[IncomeTaxExtractedData] = None
    startup_india: Optional[StartupIndiaExtractedData] = None


class BidderData(BaseModel):
    """The bidder's own declared identity (from their GeM profile / bid
    submission), used to cross-check against whatever the uploaded
    documents actually say."""

    bidder_id: str
    company_name: str
    local_content_percentage: Optional[float] = None


class VerificationRequest(BaseModel):
    tender_id: str
    bidder: BidderData
    extracted_data: ExtractedData = Field(default_factory=ExtractedData)
    requirements: TenderRequirements = Field(default_factory=TenderRequirements)
