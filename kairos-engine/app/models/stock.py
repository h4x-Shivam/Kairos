from sqlalchemy import Column, String, Numeric, Boolean, BigInteger
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from app.models.base import Base
import uuid
from datetime import datetime, timezone

class Stock(Base):
    __tablename__ = "STOCKS"

    symbol = Column(String, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    isin = Column(String, unique=True, nullable=False)
    exchange = Column(String, nullable=False)
    sector = Column(String)
    industry = Column(String)
    market_cap_bucket = Column(String)
    market_cap_cr = Column(Numeric)
    beta_1y = Column(Numeric)
    free_float_pct = Column(Numeric)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
