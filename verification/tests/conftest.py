import pytest
from app.schemas.verification_request import BidderData, TenderRequirements, ExtractedData
from app.schemas.extracted_data import (
    GSTExtractedData, PANExtractedData, UdyamExtractedData,
    EPFOExtractedData, ESICExtractedData, IncomeTaxExtractedData, StartupIndiaExtractedData,
)


@pytest.fixture
def clean_bidder():
    return BidderData(
        bidder_id="BIDDER_001",
        company_name="ABC Technologies Pvt Ltd",
        local_content_percentage=60.0,
    )


@pytest.fixture
def blacklisted_bidder():
    return BidderData(bidder_id="BIDDER_002", company_name="XYZ Enterprises")


@pytest.fixture
def fully_compliant_extracted_data():
    return ExtractedData(
        gst=GSTExtractedData(gstin="37ABCDE1234F1Z5", legal_name="ABC Technologies Pvt Ltd"),
        pan=PANExtractedData(pan_number="ABCDE1234F", name="ABC Technologies Pvt Ltd"),
        udyam=UdyamExtractedData(udyam_number="UDYAM-AP-00-0000000", enterprise_name="ABC Technologies Pvt Ltd"),
        epfo=EPFOExtractedData(establishment_id="EPFO12345", establishment_name="ABC Technologies Pvt Ltd"),
        esic=ESICExtractedData(employer_code="ESIC12345", establishment_name="ABC Technologies Pvt Ltd"),
        income_tax=IncomeTaxExtractedData(pan_number="ABCDE1234F", taxpayer_name="ABC Technologies Pvt Ltd"),
        startup_india=StartupIndiaExtractedData(certificate_number="DIPP123456", pan_number="ABCDE1234F",
                                                 startup_name="ABC Technologies Pvt Ltd"),
    )


@pytest.fixture
def all_required():
    return TenderRequirements(
        gst_required=True, pan_required=True, udyam_required=True,
        epfo_required=True, esic_required=True, income_tax_required=True,
        startup_india_required=True, blacklist_check_required=True,
        minimum_local_content_percentage=50.0,
    )
