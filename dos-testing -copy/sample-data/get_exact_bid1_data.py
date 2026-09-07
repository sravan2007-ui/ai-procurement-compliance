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

pan = 'ABCDE1001F'
gstin = '29ABCDE1001F1Z7'
cin = 'U00001IN2020PTC000001'
udyam = 'UDYAM-IN-12-0000001'

print("--- PAN RECORD ---")
r = c.execute(text(f"SELECT * FROM pan_records WHERE pan = '{pan}'")).mappings().first()
print(json.dumps(dict(r) if r else None, default=default_serializer, indent=2))

print("--- GST RECORD ---")
r = c.execute(text(f"SELECT * FROM gst_records WHERE gstin = '{gstin}'")).mappings().first()
print(json.dumps(dict(r) if r else None, default=default_serializer, indent=2))

print("--- MCA RECORD ---")
r = c.execute(text(f"SELECT * FROM mca_records WHERE cin = '{cin}'")).mappings().first()
print(json.dumps(dict(r) if r else None, default=default_serializer, indent=2))

print("--- UDYAM RECORD ---")
r = c.execute(text(f"SELECT * FROM udyam_records WHERE udyam_number = '{udyam}'")).mappings().first()
print(json.dumps(dict(r) if r else None, default=default_serializer, indent=2))

print("--- INCOME TAX RECORD ---")
r = c.execute(text(f"SELECT * FROM income_tax_records WHERE pan = '{pan}'")).mappings().first()
print(json.dumps(dict(r) if r else None, default=default_serializer, indent=2))

print("--- EPFO RECORD ---")
r = c.execute(text("SELECT * FROM epfo_records WHERE employer_name ILIKE '%ABC Technologies%' OR establishment_id ILIKE '%10001%' OR legal_name ILIKE '%ABC Technologies%'")).mappings().first()
print(json.dumps(dict(r) if r else None, default=default_serializer, indent=2))

print("--- ESIC RECORD ---")
r = c.execute(text("SELECT * FROM esic_records WHERE employer_name ILIKE '%ABC Technologies%' OR esic_number ILIKE '%10001%' OR legal_name ILIKE '%ABC Technologies%'")).mappings().first()
print(json.dumps(dict(r) if r else None, default=default_serializer, indent=2))

print("--- BIS RECORD ---")
r = c.execute(text("SELECT * FROM bis_records WHERE licensee_name ILIKE '%ABC Technologies%' OR legal_name ILIKE '%ABC Technologies%' OR company_name ILIKE '%ABC Technologies%'")).mappings().first()
print(json.dumps(dict(r) if r else None, default=default_serializer, indent=2))

print("--- STARTUP INDIA RECORD ---")
r = c.execute(text("SELECT * FROM startup_india_records WHERE entity_name ILIKE '%ABC Technologies%' OR legal_name ILIKE '%ABC Technologies%'")).mappings().first()
print(json.dumps(dict(r) if r else None, default=default_serializer, indent=2))

print("--- NSIC RECORD ---")
r = c.execute(text("SELECT * FROM nsic_records WHERE enterprise_name ILIKE '%ABC Technologies%' OR legal_name ILIKE '%ABC Technologies%'")).mappings().first()
print(json.dumps(dict(r) if r else None, default=default_serializer, indent=2))

c.close()
