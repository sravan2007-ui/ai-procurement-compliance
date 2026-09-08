import pymupdf

from app.models.udyam import UdyamDocument
from app.services.document_extractor import DocumentExtractor
from app.services.udyam_extractor import UdyamExtractor


class FakeGeminiClient:
    """Fake Gemini client used for unit testing."""

    def generate_structured(self, prompt, response_model):
        return response_model(
            udyam_number="UDYAM-KA-01-1234567",
            enterprise_name="ABC Technologies Pvt Ltd",
            organisation_type="Private Limited Company",
            major_activity="Manufacturing",
            enterprise_type="Small",
            registration_date="2021-04-12",
            state="Karnataka",
            district="Bengaluru Urban",
            raw_text=None,
            confidence=0.96,
            warnings=[],
        )


def test_udyam_extractor(tmp_path):
    pdf_path = tmp_path / "udyam_certificate.pdf"

    document = pymupdf.open()
    page = document.new_page()

    page.insert_text(
        (72, 72),
        "Udyam Registration Number: UDYAM-KA-01-1234567\n"
        "Enterprise Name: ABC Technologies Pvt Ltd\n"
        "Enterprise Type: Small\n"
        "Major Activity: Manufacturing\n"
        "State: Karnataka",
    )

    document.save(pdf_path)
    document.close()

    extractor = UdyamExtractor(
        document_extractor=DocumentExtractor(),
        gemini_client=FakeGeminiClient(),
    )

    result = extractor.extract(str(pdf_path))

    assert isinstance(result, UdyamDocument)
    assert result.udyam_number == "UDYAM-KA-01-1234567"
    assert result.enterprise_name == "ABC Technologies Pvt Ltd"
    assert result.enterprise_type == "Small"
    assert result.major_activity == "Manufacturing"
    assert result.confidence == 0.96