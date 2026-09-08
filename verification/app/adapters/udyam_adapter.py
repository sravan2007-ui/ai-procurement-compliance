from typing import Optional, Dict
from app.db.session import SessionLocal
from app.db.models import UdyamRegistry


class UdyamAdapter:
    def get_record(self, udyam_number: str) -> Optional[Dict]:
        with SessionLocal() as db:
            row = (
                db.query(UdyamRegistry)
                .filter(UdyamRegistry.udyam_number == udyam_number)
                .first()
            )
            if not row:
                return None
            return {
                "udyam_number": row.udyam_number,
                "enterprise_name": row.enterprise_name,
                "status": row.status,
                "classification": row.classification,
            }


udyam_adapter = UdyamAdapter()