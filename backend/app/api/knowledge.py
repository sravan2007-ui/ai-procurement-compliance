from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.knowledge import (
    KnowledgeDocumentCreate,
    KnowledgeDocumentResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResult,
    KnowledgeChunkCreate
)
from app.services.rag.knowledge_repository import KnowledgeRepository

router = APIRouter(
    prefix="/api/knowledge",
    tags=["Knowledge Base"],
)


@router.get("/health")
def knowledge_health(
    db: Session = Depends(get_db),
) -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/documents",
    response_model=KnowledgeDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_knowledge_document(
    request: KnowledgeDocumentCreate,
    db: Session = Depends(get_db),
) -> KnowledgeDocumentResponse:
    repository = KnowledgeRepository(db)

    document = repository.create_document(
        title=request.title,
        source=request.source,
        document_type=request.document_type,
        content=request.content,
    )

    db.commit()
    db.refresh(document)

    return document

@router.post(
    "/documents/{document_id}/chunks",
    status_code=status.HTTP_201_CREATED,
)
def create_knowledge_chunk(
    document_id: int,
    request: KnowledgeChunkCreate,
    db: Session = Depends(get_db),
) -> dict[str, int]:
    repository = KnowledgeRepository(db)

    chunk = repository.add_chunk(
        document_id=document_id,
        content=request.content,
        chunk_index=request.chunk_index,
        embedding=request.embedding,
    )

    db.commit()
    db.refresh(chunk)

    return {"id": chunk.id}

@router.post(
    "/search",
    response_model=list[KnowledgeSearchResult],
)
def search_knowledge(
    request: KnowledgeSearchRequest,
    db: Session = Depends(get_db),
) -> list[KnowledgeSearchResult]:
    repository = KnowledgeRepository(db)

    chunks = repository.search_similar(
        embedding=request.embedding,
        limit=request.limit,
    )

    return [
        KnowledgeSearchResult(
            id=chunk.id,
            document_id=chunk.document_id,
            content=chunk.content,
            chunk_index=chunk.chunk_index,
        )
        for chunk in chunks
    ]
