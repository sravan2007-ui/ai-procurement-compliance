from typing import Optional, Dict
from app.db.session import SessionLocal
from app.db.models import PANRegistry


class PANAdapter:
    def get_record(self, pan_number: str) -> Optional[Dict]:
        with SessionLocal() as db:
            row = (
                db.query(PANRegistry)
                .filter(PANRegistry.pan_number == pan_number)
                .first()
            )
            if not row:
                return None
            return {
                "pan_number": row.pan_number,
                "legal_name": row.legal_name,
                "status": row.status,
            }


pan_adapter = PANAdapter()