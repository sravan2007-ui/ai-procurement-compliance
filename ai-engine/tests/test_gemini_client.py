import pytest

from app.services.gemini_client import (
    GeminiClient,
    GeminiServiceError,
)


class FakeInteractions:
    def create(self, **kwargs):
        raise RuntimeError("simulated Gemini 429 error")


class FakeClient:
    def __init__(self):
        self.interactions = FakeInteractions()


def test_gemini_client_converts_provider_error_to_service_error():
    client = GeminiClient.__new__(GeminiClient)
    client.client = FakeClient()
    client.model = "gemini-3.6-flash"

    with pytest.raises(GeminiServiceError) as exc_info:
        client.generate("test prompt")

    assert str(exc_info.value) == (
        "Gemini service is currently unavailable."
    )


def test_gemini_client_structured_converts_provider_error_to_service_error():
    client = GeminiClient.__new__(GeminiClient)
    client.client = FakeClient()
    client.model = "gemini-3.6-flash"

    with pytest.raises(GeminiServiceError) as exc_info:
        client.generate_structured(
            "test prompt",
            dict,
        )

    assert str(exc_info.value) == (
        "Gemini service is currently unavailable."
    )