from typing import Optional, Dict
from app.db.session import SessionLocal
from app.db.models import ESICRegistry


class ESICAdapter:
    def get_record(self, employer_code: str) -> Optional[Dict]:
        with SessionLocal() as db:
            row = (
                db.query(ESICRegistry)
                .filter(ESICRegistry.employer_code == employer_code)
                .first()
            )
            if not row:
                return None
            status = "ACTIVE" if row.registration_status == "REGISTERED" else row.registration_status
            return {
                "employer_code": row.employer_code,
                "establishment_name": row.establishment_name,
                "employer_name": row.employer_name,
                "registration_date": row.registration_date,
                "registration_status": row.registration_status,
                "status": status,
                "contribution_status": row.contribution_status,
                "last_compliant_period": row.last_compliant_period,
                "compliance_period": row.last_compliant_period,
            }


esic_adapter = ESICAdapter()