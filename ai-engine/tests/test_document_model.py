from app.models.document import DocumentExtraction


def test_document_extraction():
    result = DocumentExtraction(
        document_type="GST_CERTIFICATE",
        confidence=0.97,
        extracted_text="GSTIN: 29ABCDE1234F1Z5",
        fields={
            "gstin": "29ABCDE1234F1Z5",
            "status": "Active",
        },
    )

    assert result.document_type == "GST_CERTIFICATE"
    assert result.confidence == 0.97
    assert result.fields["gstin"] == "29ABCDE1234F1Z5"
    assert result.warnings == []