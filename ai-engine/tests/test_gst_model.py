from datetime import date

from app.models.gst import GSTDocument


def test_gst_document():
    gst = GSTDocument(
        gstin="29ABCDE1234F1Z5",
        legal_name="ABC Technologies Pvt Ltd",
        trade_name="ABC Tech",
        registration_date=date(2021, 4, 12),
        status="Active",
        state="Karnataka",
        confidence=0.97,
    )

    assert gst.gstin == "29ABCDE1234F1Z5"
    assert gst.legal_name == "ABC Technologies Pvt Ltd"
    assert gst.status == "Active"
    assert gst.registration_date == date(2021, 4, 12)
    assert gst.confidence == 0.97
    assert gst.warnings == []