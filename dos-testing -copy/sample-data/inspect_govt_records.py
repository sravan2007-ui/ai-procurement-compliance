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

queries = {
    'pan_records': f"SELECT * FROM pan_records WHERE pan = '{pan}'",
    'gst_records': f"SELECT * FROM gst_records WHERE gstin = '{gstin}'",
    'mca_records': f"SELECT * FROM mca_records WHERE cin = '{cin}'",
    'udyam_records': f"SELECT * FROM udyam_records WHERE udyam_number = '{udyam}'",
    'income_tax_records': f"SELECT * FROM income_tax_records WHERE pan = '{pan}'",
    'epfo_records': "SELECT * FROM epfo_records LIMIT 3",
    'esic_records': "SELECT * FROM esic_records LIMIT 3",
    'bis_records': "SELECT * FROM bis_records LIMIT 3",
    'startup_india_records': "SELECT * FROM startup_india_records LIMIT 3",
    'nsic_records': "SELECT * FROM nsic_records LIMIT 3",
}

for name, q in queries.items():
    print(f"=== {name} ===")
    rows = [dict(r) for r in c.execute(text(q)).mappings().fetchall()]
    print(json.dumps(rows, default=default_serializer, indent=2))

# Also check column names of epfo, esic, bis, startup, nsic
for t in ['epfo_records', 'esic_records', 'bis_records', 'startup_india_records', 'nsic_records']:
    cols = [r[0] for r in c.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{t}'")).fetchall()]
    print(f"\nColumns of {t}: {cols}")
    # find where company or pan or bidder matches
    rows = [dict(r) for r in c.execute(text(f"SELECT * FROM {t} WHERE 1=1")).mappings().fetchall()]
    # check if any matches ABC Technologies or ABCDE1001F
    matches = [r for r in rows if any('ABC' in str(v) or '1001' in str(v) for v in r.values())]
    print(f"Matches for ABC in {t}: {json.dumps(matches, default=default_serializer, indent=2)}")

c.close()
