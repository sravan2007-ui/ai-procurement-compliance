from datetime import date

from app.models.udyam import UdyamDocument


def test_udyam_document():
    udyam = UdyamDocument(
        udyam_number="UDYAM-KA-01-1234567",
        enterprise_name="ABC Technologies Pvt Ltd",
        organisation_type="Private Limited Company",
        major_activity="Manufacturing",
        enterprise_type="Small",
        registration_date=date(2021, 4, 12),
        state="Karnataka",
        district="Bengaluru Urban",
        confidence=0.96,
    )

    assert udyam.udyam_number == "UDYAM-KA-01-1234567"
    assert udyam.enterprise_name == "ABC Technologies Pvt Ltd"
    assert udyam.enterprise_type == "Small"
    assert udyam.registration_date == date(2021, 4, 12)
    assert udyam.confidence == 0.96
    assert udyam.warnings == []