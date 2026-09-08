from typing import Optional, Dict
from app.db.session import SessionLocal
from app.db.models import EPFORegistry


class EPFOAdapter:
    def get_record(self, establishment_id: str) -> Optional[Dict]:
        with SessionLocal() as db:
            row = (
                db.query(EPFORegistry)
                .filter(EPFORegistry.establishment_id == establishment_id)
                .first()
            )
            if not row:
                return None
            return {
                "establishment_id": row.establishment_id,
                "establishment_name": row.establishment_name,
                "contribution_status": row.contribution_status,
                "status": row.status,
            }


epfo_adapter = EPFOAdapter()