import pytest
import requests
from app.services.rag.rag_client import RAGClient, RAGClientError


class FakeResponse:
    def raise_for_status(self):
        pass

    def json(self):
        return [
            {
                "id": 1,
                "document_id": 10,
                "content": "GST registration must be valid.",
                "chunk_index": 0,
            }
        ]


def test_rag_client_search(monkeypatch):
    def fake_post(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "app.services.rag.rag_client.requests.post",
        fake_post,
    )

    client = RAGClient(base_url="http://test-server")

    results = client.search(
        embedding=[1.0] + [0.0] * 383,
        limit=5,
    )

    assert len(results) == 1
    assert results[0]["id"] == 1
    assert results[0]["document_id"] == 10
    assert results[0]["content"] == "GST registration must be valid."


def test_rag_client_raises_error_when_backend_unavailable(monkeypatch):
    def fake_post(*args, **kwargs):
        raise requests.RequestException("Backend unavailable")

    monkeypatch.setattr(
        "app.services.rag.rag_client.requests.post",
        fake_post,
    )

    client = RAGClient(base_url="http://test-server")

    with pytest.raises(RAGClientError):
        client.search(
            embedding=[1.0] + [0.0] * 383,
        )
