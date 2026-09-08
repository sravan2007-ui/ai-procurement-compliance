from typing import Optional, Dict
from app.db.session import SessionLocal
from app.db.models import IncomeTaxRegistry


class IncomeTaxAdapter:
    def get_record(self, pan_number: str) -> Optional[Dict]:
        with SessionLocal() as db:
            row = (
                db.query(IncomeTaxRegistry)
                .filter(IncomeTaxRegistry.pan_number == pan_number)
                .first()
            )
            if not row:
                return None
            return {
                "pan_number": row.pan_number, 
                "taxpayer_name": row.taxpayer_name,
                "assessment_year": row.assessment_year,
                "filing_status": row.filing_status,
                "return_filing_date": row.return_filing_date,
                "gross_total_income": row.gross_total_income,
                "taxable_income": row.taxable_income,
            }


income_tax_adapter = IncomeTaxAdapter()