import sys
sys.path.append('backend')
from app.core.database import engine
from sqlalchemy import text
import json
from decimal import Decimal
from datetime import date, datetime

def default_serializer(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    return str(obj)

c = engine.connect()

print("--- BID 1 ---")
bid = c.execute(text("SELECT * FROM bids WHERE id = 1")).mappings().first()
bid_dict = dict(bid) if bid else None
print(json.dumps(bid_dict, default=default_serializer, indent=2))

if bid:
    print("--- BIDDER ---")
    bidder = c.execute(text(f"SELECT * FROM bidders WHERE id = {bid['bidder_id']}")).mappings().first()
    bidder_dict = dict(bidder) if bidder else None
    print(json.dumps(bidder_dict, default=default_serializer, indent=2))

    print("--- TENDER ---")
    tender = c.execute(text(f"SELECT * FROM tenders WHERE id = {bid['tender_id']}")).mappings().first()
    tender_dict = dict(tender) if tender else None
    print(json.dumps(tender_dict, default=default_serializer, indent=2))

    # Check government registry tables for this bidder
    pan = bidder_dict.get('pan')
    gstin = bidder_dict.get('gstin')
    cin = bidder_dict.get('cin')
    udyam = bidder_dict.get('udyam_number')
    print(f"\nSearching government tables for PAN={pan}, GSTIN={gstin}, CIN={cin}, UDYAM={udyam}...")

    tables = ['pan_records', 'gst_records', 'udyam_records', 'mca_records', 'income_tax_records', 
              'epfo_records', 'esic_records', 'startup_india_records', 'nsic_records', 'bis_records']
    
    for t in tables:
        cols = [r[0] for r in c.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{t}'")).fetchall()]
        # find matching rows
        query = f"SELECT * FROM {t} WHERE "
        conditions = []
        if 'pan' in cols and pan:
            conditions.append(f"pan = '{pan}'")
        if 'gstin' in cols and gstin:
            conditions.append(f"gstin = '{gstin}'")
        if 'cin' in cols and cin:
            conditions.append(f"cin = '{cin}'")
        if 'udyam_number' in cols and udyam:
            conditions.append(f"udyam_number = '{udyam}'")
        if 'company_name' in cols and bidder_dict.get('company_name'):
            conditions.append(f"company_name ILIKE '%{bidder_dict['company_name']}%'")
        if 'legal_name' in cols and bidder_dict.get('legal_name'):
            conditions.append(f"legal_name ILIKE '%{bidder_dict['legal_name']}%'")
            
        if conditions:
            q = f"SELECT * FROM {t} WHERE " + " OR ".join(conditions)
            rows = [dict(r) for r in c.execute(text(q)).mappings().fetchall()]
            print(f"[{t}] matched {len(rows)} rows:")
            for r in rows:
                print("  ", json.dumps(r, default=default_serializer))
        else:
            print(f"[{t}] No matching filter columns (cols: {cols})")

    print("\n--- EXISTING DOCUMENTS FOR BID 1 ---")
    docs = [dict(r) for r in c.execute(text("SELECT * FROM documents WHERE bid_id = 1")).mappings().fetchall()]
    print(f"Found {len(docs)} documents:")
    for d in docs:
        print("  ", json.dumps(d, default=default_serializer))

    print("\n--- EXISTING COMPLIANCE RESULTS FOR BID 1 ---")
    comps = [dict(r) for r in c.execute(text("SELECT * FROM compliance_results WHERE bid_id = 1")).mappings().fetchall()]
    print(f"Found {len(comps)} compliance records:")
    for comp in comps:
        print("  ", json.dumps(comp, default=default_serializer))

c.close()
