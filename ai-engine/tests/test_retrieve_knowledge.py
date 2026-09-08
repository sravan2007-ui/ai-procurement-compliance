from app.services.workflow.nodes.retrieve_knowledge import retrieve_knowledge


class FakeRAGService:
    def retrieve(self, query, limit):
        assert query == "GST compliance requirement"
        assert limit == 5

        return [
            {
                "id": 17,
                "document_id": 18,
                "content": "A bidder must have a valid GST registration.",
                "chunk_index": 0,
            }
        ]


def test_retrieve_knowledge():
    state = {
        "tender_text": "GST compliance requirement",
    }

    result = retrieve_knowledge(
        state,
        rag_service=FakeRAGService(),
    )

    assert "error" not in result
    assert len(result["retrieved_knowledge"]) == 1
    assert result["retrieved_knowledge"][0]["id"] == 17
    assert result["retrieved_knowledge"][0]["content"] == (
        "A bidder must have a valid GST registration."
    )


def test_retrieve_knowledge_rejects_empty_tender():
    state = {
        "tender_text": "",
    }

    result = retrieve_knowledge(
        state,
        rag_service=FakeRAGService(),
    )

    assert result["error"] == "Tender text cannot be empty."
