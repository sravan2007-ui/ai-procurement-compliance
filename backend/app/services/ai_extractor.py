from typing import TypeVar

from google import genai
from pydantic import BaseModel

from app.core.config import settings


T = TypeVar("T", bound=BaseModel)


class AIExtractor:
    def __init__(self):
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def extract(
        self,
        document_text: str,
        schema: type[T],
    ) -> T:
        prompt = f"""
You are a document data extraction system.

Extract information from the document text below.

Rules:
- Extract only information explicitly present in the document.
- Do not invent or guess values.
- If a field is not present, return null.
- Return data according to the provided schema.

Document text:
{document_text}
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_schema": schema,
            },
        )

        return schema.model_validate_json(
            response.text
        )