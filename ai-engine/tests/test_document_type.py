from app.models.document_type import DocumentType, DocumentTypeResult


def test_document_type_result():
    result = DocumentTypeResult(
        document_type=DocumentType.GST_CERTIFICATE,
        confidence=0.98,
        reasoning="The document contains a GSTIN and GST registration details.",
    )

    assert result.document_type == DocumentType.GST_CERTIFICATE
    assert result.confidence == 0.98
    assert "GSTIN" in result.reasoning