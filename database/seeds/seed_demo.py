from pathlib import Path
import sys
from datetime import datetime, timezone

backend_dir = Path(__file__).resolve().parents[2] / "backend"
sys.path.insert(0, str(backend_dir))
import os
os.chdir(backend_dir)

from app.core.database import SessionLocal
from app.models import (
    Bidder,
    BidDocument,
    DocumentExtraction,
    KnowledgeChunk,
    KnowledgeDocument,
    Tender,
    TenderBid,
)
from sentence_transformers import SentenceTransformer


def main() -> None:
    db = SessionLocal()

    try:
        existing_tender = db.query(Tender).filter(
            Tender.title == "Demo Industrial Equipment Procurement"
        ).first()

        existing_bidder = db.query(Bidder).filter(
            Bidder.company_name == "Demo Industrial Solutions Pvt Ltd"
        ).first()

        if existing_tender or existing_bidder:
            print("Demo seed data already exists. Nothing to insert.")
            return

        tender = Tender(
            title="Demo Industrial Equipment Procurement",
            organization="Demo Government Organization",
            description="Synthetic tender data for local development and demonstration.",
            submission_deadline=datetime(2026, 12, 31, tzinfo=timezone.utc),
            status="DRAFT",
        )

        bidder = Bidder(
            company_name="Demo Industrial Solutions Pvt Ltd",
            pan="ABCDE1234F",
            gstin="29ABCDE1234F1Z5",
            udyam_number="UDYAM-KA-00-0000000",
            cin="U00000KA2026PTC000000",
            email="demo@example.com",
            phone="9000000000",
        )

        db.add_all([tender, bidder])
        db.flush()

        bid = TenderBid(
            tender_id=tender.id,
            bidder_id=bidder.id,
            status="SUBMITTED",
        )
        db.add(bid)
        db.flush()

        documents = [
            BidDocument(
                bid_id=bid.id,
                document_type="PAN",
                file_name="demo_pan.pdf",
                file_path="demo/seed/demo_pan.pdf",
                mime_type="application/pdf",
                status="UPLOADED",
            ),
            BidDocument(
                bid_id=bid.id,
                document_type="GST",
                file_name="demo_gst_certificate.pdf",
                file_path="demo/seed/demo_gst_certificate.pdf",
                mime_type="application/pdf",
                status="UPLOADED",
            ),
            BidDocument(
                bid_id=bid.id,
                document_type="UDYAM",
                file_name="demo_udyam_certificate.pdf",
                file_path="demo/seed/demo_udyam_certificate.pdf",
                mime_type="application/pdf",
                status="UPLOADED",
            ),
        ]

        db.add_all(documents)
        db.flush()

        extractions = [
            DocumentExtraction(
                document_id=documents[0].id,
                document_type="PAN",
                extracted_data={
                    "pan_number": bidder.pan,
                    "holder_name": bidder.company_name,
                },
                extraction_status="COMPLETED",
                model_name="demo-seed",
            ),
            DocumentExtraction(
                document_id=documents[1].id,
                document_type="GST",
                extracted_data={
                    "gstin": bidder.gstin,
                    "legal_name": bidder.company_name,
                    "status": "active",
                },
                extraction_status="COMPLETED",
                model_name="demo-seed",
            ),
            DocumentExtraction(
                document_id=documents[2].id,
                document_type="UDYAM",
                extracted_data={
                    "udyam_number": bidder.udyam_number,
                    "enterprise_name": bidder.company_name,
                },
                extraction_status="COMPLETED",
                model_name="demo-seed",
            ),
        ]

        db.add_all(extractions)

        knowledge_content = "A bidder must have a valid GST registration."

        knowledge_document = KnowledgeDocument(
            title="Demo GST Compliance Rule",
            source="Synthetic Prototype Knowledge Base",
            document_type="procurement_rule",
            content=knowledge_content,
        )

        db.add(knowledge_document)
        db.flush()

        embedding = SentenceTransformer('all-MiniLM-L6-v2').encode(knowledge_content, normalize_embeddings=True).tolist()

        knowledge_chunk = KnowledgeChunk(
            document_id=knowledge_document.id,
            content=knowledge_content,
            chunk_index=0,
            embedding=embedding,
        )

        db.add(knowledge_chunk)
        db.commit()

        print(f"Created tender id={tender.id}")
        print(f"Created bidder id={bidder.id}")
        print(f"Created bid id={bid.id}")
        print(f"Created {len(documents)} bid documents")
        print(f"Created {len(extractions)} document extractions")
        print(f"Created knowledge document id={knowledge_document.id}")
        print(f"Created knowledge chunk id={knowledge_chunk.id}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
