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

for bid_id in [2, 5, 7]:
    bid = dict(c.execute(text(f"SELECT * FROM bids WHERE id = {bid_id}")).mappings().first())
    bidder_id = bid['bidder_id']
    tender_id = bid['tender_id']
    bidder = dict(c.execute(text(f"SELECT * FROM bidders WHERE id = {bidder_id}")).mappings().first())
    tender = dict(c.execute(text(f"SELECT * FROM tenders WHERE id = {tender_id}")).mappings().first())
    
    pan = bidder.get('pan')
    gstin = bidder.get('gstin')
    cin = bidder.get('cin')
    udyam = bidder.get('udyam_number')
    
    # Check compliance result if any
    comp = c.execute(text(f"SELECT * FROM compliance_results WHERE bid_id = {bid_id} ORDER BY id DESC")).mappings().first()
    
    print(f"\n=================== CANDIDATE BID {bid_id} ===================")
    print("Bid:", json.dumps(bid, default=default_serializer, indent=2))
    print("Bidder:", json.dumps(bidder, default=default_serializer, indent=2))
    print("Tender:", json.dumps(tender, default=default_serializer, indent=2))
    print("Compliance result:", json.dumps(dict(comp) if comp else None, default=default_serializer, indent=2))

    # Check government tables for this bidder
    print(f"Checking govt records for PAN={pan}, GSTIN={gstin}, CIN={cin}, UDYAM={udyam}...")
    for t, field, val in [('pan_records', 'pan', pan), 
                          ('gst_records', 'gstin', gstin), 
                          ('mca_records', 'cin', cin), 
                          ('udyam_records', 'udyam_number', udyam),
                          ('income_tax_records', 'pan', pan)]:
        if val:
            row = c.execute(text(f"SELECT * FROM {t} WHERE {field} = '{val}'")).mappings().first()
            print(f"  {t}: {json.dumps(dict(row) if row else None, default=default_serializer)}")

    # Check EPFO, ESIC, BIS, Startup, NSIC
    company_name = bidder['company_name']
    for t in ['epfo_records', 'esic_records', 'bis_records', 'startup_india_records', 'nsic_records']:
        rows = [dict(r) for r in c.execute(text(f"SELECT * FROM {t}")).mappings().fetchall()]
        matched = [r for r in rows if any(company_name.lower() in str(v).lower() for v in r.values())]
        print(f"  {t}: {json.dumps(matched[0] if matched else None, default=default_serializer)}")

c.close()
