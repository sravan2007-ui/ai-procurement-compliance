# Verification Engine

Rule-based, deterministic microservice that verifies bidder compliance
(GST, PAN, Udyam, EPFO, ESIC, Income Tax, Startup India, Blacklist) for
GeM procurement tenders, and produces a compliance score + risk level.
AI/LLMs are NOT used for the pass/fail decision — only for upstream
document extraction (a different service), whose output contract is
defined in `app/schemas/extracted_data.py`.

## Install

    pip install -r requirements.txt --break-system-packages

## Run

    uvicorn app.main:app --reload --port 8001

Then open http://localhost:8001/docs for interactive Swagger UI.

## Test

    pytest tests/ -v

31 tests across every rule module, plus `tests/test_engine.py` for
full end-to-end orchestration, and a regression test in
`tests/test_blacklist.py` for the "Fraudulent Supplies Ltd" bug.

## Example request

    POST /verification/run

    {
      "tender_id": "TND_001",
      "bidder": {
        "bidder_id": "BIDDER_001",
        "company_name": "ABC Technologies Pvt Ltd"
      },
      "extracted_data": {
        "gst": {"gstin": "37ABCDE1234F1Z5", "legal_name": "ABC Technologies Pvt Ltd"},
        "pan": {"pan_number": "ABCDE1234F", "name": "ABC Technologies Pvt Ltd"},
        "udyam": {"udyam_number": "UDYAM-AP-00-0000000", "enterprise_name": "ABC Technologies Pvt Ltd"},
        "epfo": {"establishment_id": "EPFO12345", "establishment_name": "ABC Technologies Pvt Ltd"},
        "esic": {"employer_code": "ESIC12345", "establishment_name": "ABC Technologies Pvt Ltd"},
        "income_tax": {"pan_number": "ABCDE1234F", "taxpayer_name": "ABC Technologies Pvt Ltd"},
        "startup_india": {"certificate_number": "DIPP123456", "pan_number": "ABCDE1234F", "startup_name": "ABC Technologies Pvt Ltd"}
      },
      "requirements": {
        "gst_required": true,
        "pan_required": true,
        "udyam_required": true,
        "epfo_required": true,
        "esic_required": true,
        "income_tax_required": true,
        "startup_india_required": true,
        "blacklist_check_required": true
      }
    }

`extracted_data` fields are all optional — send only the documents that
exist for a given bidder/tender. A missing block for a *required* check
results in FAIL ("document not provided"); a missing block for a
*non-required* check results in NOT_APPLICABLE.

## Blacklist matching (fixed + hardened)

`app/adapters/blacklist_adapter.py` matches in this priority order:
1. Exact PAN match
2. Exact GSTIN match
3. Exact company name match
4. Fuzzy company name match (`difflib.SequenceMatcher`, threshold 0.85) →
   returns `MANUAL_REVIEW`, not a silent PASS, so a near-identical renamed
   entity gets a human's eyes instead of slipping through.

## Next milestones

- `local_content_rules.py`, `document_validator.py`, `expiry_validator.py`
- `cross_verification.py` — a dedicated pass that compares company name
  across every extracted document + bidder declaration in one place,
  instead of pairwise inside each rule
- Remaining checks: MCA, BIS, NSIC, OEM authorization
- Swap adapters from local JSON to real government APIs / PostgreSQL
