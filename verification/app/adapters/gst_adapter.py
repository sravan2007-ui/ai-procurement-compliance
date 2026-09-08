from typing import Optional, Dict
from app.db.session import SessionLocal
from app.db.models import GSTRegistry


class GSTAdapter:
    """Wraps access to GST records via PostgreSQL registry table."""

    def get_record(self, gstin: str) -> Optional[Dict]:
        with SessionLocal() as db:
            row = (
                db.query(GSTRegistry)
                .filter(GSTRegistry.gstin == gstin)
                .first()
            )
            if not row:
                return None
            return {
                "gstin": row.gstin,
                "legal_name": row.legal_name,
                "trade_name": row.trade_name,
                "status": row.status,
                "registration_date": row.registration_date,
                "business_type": row.business_type,
                "return_filing_status": row.return_filing_status,
                "principal_place_of_business": row.principal_place_of_business,
            }


gst_adapter = GSTAdapter()