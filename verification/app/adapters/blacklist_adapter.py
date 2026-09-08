from difflib import SequenceMatcher
from typing import Optional, Tuple, Dict
from sqlalchemy import func
from app.db.session import SessionLocal
from app.db.models import BlacklistRegistry

# Ratio (0-1) above which a company name is considered "close enough" to a
# blacklisted entity's name to warrant a human look, even without an exact
# identifier (PAN/GSTIN) match.
NAME_SIMILARITY_THRESHOLD = 0.85


class BlacklistAdapter:
    def find_match(
        self, pan_number: Optional[str], gstin: Optional[str], company_name: str
    ) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Queries PostgreSQL  table.
        Returns (matched_record, match_type) or (None, None) if clean.

        match_type is one of:
          "EXACT_PAN"    - identifier match, highest confidence
          "EXACT_GSTIN"  - identifier match, highest confidence
          "EXACT_NAME"   - exact (case-insensitive) name match
          "FUZZY_NAME"   - name is suspiciously similar but not identical;
                            routes to manual review
        """
        with SessionLocal() as db:
            # 1. Exact identifier matches first (indexed lookups)
            if pan_number:
                record = db.query(BlacklistRegistry).filter(BlacklistRegistry.pan_number == pan_number).first()
                if record:
                    return self._to_dict(record), "EXACT_PAN"

            if gstin:
                record = db.query(BlacklistRegistry).filter(BlacklistRegistry.gstin == gstin).first()
                if record:
                    return self._to_dict(record), "EXACT_GSTIN"

            normalized_company = company_name.strip().lower()

            # 2. Exact name match (case-insensitive)
            record = (
                db.query(BlacklistRegistry)
                .filter(func.lower(func.trim(BlacklistRegistry.entity_name)) == normalized_company)
                .first()
            )
            if record:
                return self._to_dict(record), "EXACT_NAME"

            # 3. Fuzzy name match against all records
            all_records = db.query(BlacklistRegistry).all()
            best_entry, best_ratio = None, 0.0

            for entry in all_records:
                target_name = (entry.entity_name or "").strip().lower()
                ratio = SequenceMatcher(None, normalized_company, target_name).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_entry = entry

            if best_entry and best_ratio >= NAME_SIMILARITY_THRESHOLD:
                return self._to_dict(best_entry), "FUZZY_NAME"

            return None, None

    @staticmethod
    def _to_dict(record: BlacklistRegistry) -> Dict:
        return {
            "pan_number": record.pan_number,
            "gstin": record.gstin,
            "entity_name": record.entity_name,
            "blacklisted": record.blacklisted,
            "reason": record.reason,
            "valid_until": record.valid_until,
        }


blacklist_adapter = BlacklistAdapter()