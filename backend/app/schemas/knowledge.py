from pydantic import BaseModel, Field


class KnowledgeDocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    source: str = Field(min_length=1, max_length=500)
    document_type: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)


class KnowledgeDocumentResponse(BaseModel):
    id: int
    title: str
    source: str
    document_type: str

    model_config = {
        "from_attributes": True,
    }

class KnowledgeChunkCreate(BaseModel):
    content: str = Field(min_length=1)
    chunk_index: int = Field(ge=0)
    embedding: list[float] = Field(min_length=384, max_length=384)

class KnowledgeSearchRequest(BaseModel):
    embedding: list[float] = Field(
        min_length=384,
        max_length=384,
    )
    limit: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class KnowledgeSearchResult(BaseModel):
    id: int
    document_id: int
    content: str
    chunk_index: int
