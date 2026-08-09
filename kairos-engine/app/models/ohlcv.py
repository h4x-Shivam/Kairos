from sqlalchemy import Column, String, Numeric, BigInteger
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.models.base import Base

class OhlcvBar(Base):
    __tablename__ = "OHLCV_BARS"

    symbol = Column(String, primary_key=True)
    timeframe = Column(String, primary_key=True)  # e.g., '15m', '1d', '1w'
    bar_time = Column(TIMESTAMP(timezone=True), primary_key=True)
    
    open = Column(Numeric, nullable=False)
    high = Column(Numeric, nullable=False)
    low = Column(Numeric, nullable=False)
    close = Column(Numeric, nullable=False)
    volume = Column(BigInteger, nullable=False)
    delivery_volume = Column(BigInteger)
    delivery_pct = Column(Numeric)
