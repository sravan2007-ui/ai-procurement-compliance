import json
from pathlib import Path
from app.db.session import engine, Base, SessionLocal
from app.db.models import (
    BlacklistRegistry,
    GSTRegistry,
    PANRegistry,
    UdyamRegistry,
    EPFORegistry,
    ESICRegistry,
    IncomeTaxRegistry,
    StartupIndiaRegistry,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "rules-data" / "government-data"


def seed_all():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Blacklist (List format)
        bl_path = DATA_DIR / "blacklist.json"
        if bl_path.exists():
            with open(bl_path) as f:
                for item in json.load(f):
                    if not db.query(BlacklistRegistry).filter_by(pan_number=item.get("pan_number")).first():
                        db.add(BlacklistRegistry(**item))

        # 2. GST (Dictionary format)
        gst_path = DATA_DIR / "gst.json"
        if gst_path.exists():
            with open(gst_path) as f:
                for key, val in json.load(f).items():
                    if not db.query(GSTRegistry).filter_by(gstin=key).first():
                        db.add(GSTRegistry(**val))

        # 3. PAN (Dictionary format)
        pan_path = DATA_DIR / "pan.json"
        if pan_path.exists():
            with open(pan_path) as f:
                for key, val in json.load(f).items():
                    if not db.query(PANRegistry).filter_by(pan_number=key).first():
                        db.add(PANRegistry(**val))

        # 4. Udyam (Dictionary format)
        udyam_path = DATA_DIR / "udyam.json"
        if udyam_path.exists():
            with open(udyam_path) as f:
                for key, val in json.load(f).items():
                    if not db.query(UdyamRegistry).filter_by(udyam_number=key).first():
                        db.add(UdyamRegistry(**val))

        # 5. EPFO (Dictionary format)
        epfo_path = DATA_DIR / "epfo.json"
        if epfo_path.exists():
            with open(epfo_path) as f:
                for key, val in json.load(f).items():
                    if not db.query(EPFORegistry).filter_by(establishment_id=key).first():
                        db.add(EPFORegistry(**val))

        # 6. ESIC (Dictionary format)
        esic_path = DATA_DIR / "esic.json"
        if esic_path.exists():
            with open(esic_path) as f:
                for key, val in json.load(f).items():
                    if not db.query(ESICRegistry).filter_by(employer_code=key).first():
                        db.add(ESICRegistry(**val))

        # 7. Income Tax (Dictionary format)
        it_path = DATA_DIR / "income_tax.json"
        if it_path.exists():
            with open(it_path) as f:
                for key, val in json.load(f).items():
                    if not db.query(IncomeTaxRegistry).filter_by(pan_number=key).first():
                        db.add(IncomeTaxRegistry(**val))

        # 8. Startup India (Dictionary format)
        si_path = DATA_DIR / "startup_india.json"
        if si_path.exists():
            with open(si_path) as f:
                for key, val in json.load(f).items():
                    if not db.query(StartupIndiaRegistry).filter_by(certificate_number=key).first():
                        db.add(StartupIndiaRegistry(**val))

        db.commit()
        print("Data loaded into PostgreSQL tables successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_all()