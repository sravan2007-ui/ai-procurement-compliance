from sqlalchemy import Column, String, Boolean, Float, Date, JSON
from app.db.session import Base


class BlacklistRegistry(Base):
    __tablename__ = "registry_blacklist"

    pan_number = Column(String(10), primary_key=True, index=True)
    gstin = Column(String(15), index=True, nullable=True)
    entity_name = Column(String(255), nullable=False)
    blacklisted = Column(Boolean, default=True)
    reason = Column(String, nullable=True)
    valid_until = Column(String(20), nullable=True)


class GSTRegistry(Base):
    __tablename__ = "registry_gst"

    gstin = Column(String(15), primary_key=True, index=True)
    legal_name = Column(String(255), nullable=False)
    trade_name = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)  # ACTIVE / INACTIVE
    registration_date = Column(String(20), nullable=True)
    business_type = Column(String(100), nullable=True)
    return_filing_status = Column(String(50), nullable=True)  # COMPLIANT / NON_COMPLIANT
    principal_place_of_business = Column(String, nullable=True)


class PANRegistry(Base):
    __tablename__ = "registry_pan"

    pan_number = Column(String(10), primary_key=True, index=True)
    legal_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)  # VALID / INVALID


class UdyamRegistry(Base):
    __tablename__ = "registry_udyam"

    udyam_number = Column(String(30), primary_key=True, index=True)
    enterprise_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    classification = Column(String(50), nullable=True)  # MICRO, SMALL, MEDIUM


class EPFORegistry(Base):
    __tablename__ = "registry_epfo"

    establishment_id = Column(String(50), primary_key=True, index=True)
    establishment_name = Column(String(255), nullable=False)
    contribution_status = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    last_compliant_period = Column(String(20), nullable=True)

class ESICRegistry(Base):
    __tablename__ = "registry_esic"
    employer_code = Column(String(50), primary_key=True, index=True)
    establishment_name = Column(String(255), nullable=False)
    employer_name = Column(String(255), nullable=True)
    registration_date = Column(String(20), nullable=True)
    registration_status = Column(String(50), nullable=False)  # REGISTERED / DEREGISTERED
    contribution_status = Column(String(50), nullable=False)  # COMPLIANT / DEFAULTED / EXEMPTED
    last_compliant_period = Column(String(20), nullable=True)


class IncomeTaxRegistry(Base):
    __tablename__ = "registry_income_tax"

    pan_number = Column(String(10), primary_key=True, index=True)
    taxpayer_name = Column(String(255), nullable=False)
    assessment_year = Column(String(20), nullable=False)
    filing_status = Column(String(50), nullable=False)  # FILED_WITHIN_DUE_DATE / FILED_AFTER_DUE_DATE
    return_filing_date = Column(String(20), nullable=True)
    gross_total_income = Column(String(50), nullable=True)
    taxable_income = Column(String(50), nullable=True)


class StartupIndiaRegistry(Base):
    __tablename__ = "registry_startup_india"

    certificate_number = Column(String(50), primary_key=True, index=True)
    startup_name = Column(String(255), nullable=False)
    recognition_date = Column(String(20), nullable=True)
    entity_type = Column(String(100), nullable=True)
    pan_number = Column(String(10), index=True, nullable=False)
    validity_status = Column(String(50), nullable=False)  # VALID / EXPIRED / ACTIVE