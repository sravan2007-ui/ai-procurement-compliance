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

for t in ['bis_records', 'startup_india_records']:
    cols = [r[0] for r in c.execute(text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{t}'")).fetchall()]
    print(f"Columns for {t}: {cols}")
    rows = [dict(r) for r in c.execute(text(f"SELECT * FROM {t} LIMIT 5")).mappings().fetchall()]
    print(f"Sample from {t}: {json.dumps(rows, default=default_serializer, indent=2)}")

c.close()
