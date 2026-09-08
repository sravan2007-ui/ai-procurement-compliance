from typing import TypeVar

from google import genai
from pydantic import BaseModel

from app.core.config import settings


T = TypeVar("T", bound=BaseModel)


class GeminiServiceError(RuntimeError):
    """Raised when the Gemini service cannot complete a request."""


class GeminiClient:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def generate(self, prompt: str) -> str:
        try:
            interaction = self.client.interactions.create(
                model=self.model,
                input=prompt,
            )
        except Exception as exc:
            raise GeminiServiceError(
                "Gemini service is currently unavailable."
            ) from exc

        if not interaction.output_text:
            raise GeminiServiceError(
                "Gemini returned an empty response."
            )

        return interaction.output_text

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:
        try:
            interaction = self.client.interactions.create(
                model=self.model,
                input=prompt,
                response_format={
                    "type": "text",
                    "mime_type": "application/json",
                    "schema": response_model.model_json_schema(),
                },
            )
        except Exception as exc:
            raise GeminiServiceError(
                "Gemini service is currently unavailable."
            ) from exc

        if not interaction.output_text:
            raise GeminiServiceError(
                "Gemini returned an empty response."
            )

        try:
            return response_model.model_validate_json(
                interaction.output_text
            )
        except Exception as exc:
            raise GeminiServiceError(
                "Gemini returned an invalid structured response."
            ) from exc