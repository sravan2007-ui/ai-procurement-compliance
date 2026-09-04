import uuid
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.bid_document import BidDocument
from app.models.tender_bid import TenderBid
from app.schemas.bid_document import (
    BidDocumentResponse,
    DocumentType,
)
from app.services.document_processor import extract_text_from_pdf
from app.schemas.document_processing import DocumentProcessingResponse
from app.services.document_extractor import get_extraction_schema
from app.services.ai_extractor import AIExtractor

router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"],
)


UPLOAD_DIR = Path("uploads/bids")


ALLOWED_MIME_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}


@router.post("/", response_model=BidDocumentResponse)
def upload_document(
    bid_id: int = Form(...),
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 1. Check that the bid exists
    bid = (
        db.query(TenderBid)
        .filter(TenderBid.id == bid_id)
        .first()
    )

    if not bid:
        raise HTTPException(
            status_code=404,
            detail="Bid not found",
        )

    # 2. Validate file type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only PDF, JPEG, and PNG are allowed.",
        )

    # 3. Create bidder-specific upload directory
    bid_upload_dir = UPLOAD_DIR / str(bid_id)
    bid_upload_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    # 4. Save the file
    original_filename = Path(file.filename).name
    file_extension = Path(original_filename).suffix.lower()

    stored_filename = f"{uuid.uuid4().hex}{file_extension}"

    file_path = bid_upload_dir / stored_filename

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

    file_size = 0

    with file_path.open("wb") as buffer:
        while chunk := file.file.read(1024 * 1024):
            file_size += len(chunk)

            if file_size > MAX_FILE_SIZE:
                file_path.unlink(missing_ok=True)

                raise HTTPException(
                    status_code=400,
                    detail="File too large. Maximum file size is 10 MB.",
                )

            buffer.write(chunk)

    # 5. Create database record
    document = BidDocument(
        bid_id=bid_id,
        document_type=document_type.value,
        file_name = original_filename,
        file_path=str(file_path),
        mime_type=file.content_type,
        status="UPLOADED",
    )

    try:
        db.add(document)
        db.commit()
        db.refresh(document)

    except Exception:
        db.rollback()

        # Database failed, so remove the already-saved file
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=500,
            detail="Failed to save document information.",
        )

    return document

@router.get(
    "/bid/{bid_id}",
    response_model=list[BidDocumentResponse],
)
def get_bid_documents(
    bid_id: int,
    db: Session = Depends(get_db),
):
    # Check that the bid exists
    bid = (
        db.query(TenderBid)
        .filter(TenderBid.id == bid_id)
        .first()
    )

    if not bid:
        raise HTTPException(
            status_code=404,
            detail="Bid not found",
        )

    # Get all documents belonging to the bid
    documents = (
        db.query(BidDocument)
        .filter(BidDocument.bid_id == bid_id)
        .order_by(BidDocument.uploaded_at.desc())
        .all()
    )

    return documents

@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    # 1. Find document
    document = (
        db.query(BidDocument)
        .filter(BidDocument.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    # 2. Check that physical file exists
    file_path = Path(document.file_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document file not found",
        )

    # 3. Return the actual file
    return FileResponse(
        path=file_path,
        media_type=document.mime_type,
        filename=document.file_name,
    )

@router.post(
    "/{document_id}/process",
    response_model=DocumentProcessingResponse,
)
def process_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    document = (
        db.query(BidDocument)
        .filter(BidDocument.id == document_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    file_path = Path(document.file_path)

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Document file not found",
        )

    # Step 1: Extract text from PDF
    try:
        extracted_text = extract_text_from_pdf(
            document.file_path
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to process document",
        )

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="No text could be extracted from document",
        )

    # Step 2: Select extraction schema
    schema = get_extraction_schema(
        document.document_type
    )

    # Step 3: Extract structured data using Gemini
    structured_data = None

    if schema is not None:
        try:
            extractor = AIExtractor()

            structured_data = extractor.extract(
                document_text=extracted_text,
                schema=schema,
            )

        except ValueError as exc:
            raise HTTPException(
                status_code=500,
                detail=str(exc),
            )

        except Exception:
            raise HTTPException(
                status_code=500,
                detail="AI document extraction failed",
            )

    return {
        "document_id": document.id,
        "status": "PROCESSED",
        "extracted_text": extracted_text,
        "extracted_data": (
            structured_data.model_dump()
            if structured_data is not None
            else None
    ),
}