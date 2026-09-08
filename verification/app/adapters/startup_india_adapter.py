from typing import Optional, Dict
from app.db.session import SessionLocal
from app.db.models import StartupIndiaRegistry


class StartupIndiaAdapter:
    def get_record(self, certificate_number: str) -> Optional[Dict]:
        with SessionLocal() as db:
            row = (
                db.query(StartupIndiaRegistry)
                .filter(StartupIndiaRegistry.certificate_number == certificate_number)
                .first()
            )
            if not row:
                return None
            return {
                "certificate_number": row.certificate_number,
                "startup_name": row.startup_name,
                "recognition_date": row.recognition_date,
                "entity_type": row.entity_type,
                "pan_number": row.pan_number,
                "validity_status": row.validity_status,
            }


startup_india_adapter = StartupIndiaAdapter()