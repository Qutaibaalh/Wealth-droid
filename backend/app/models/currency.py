from sqlalchemy import Column, String, BigInteger, Date, UniqueConstraint
from app.models.base import BaseModel


class ExchangeRate(BaseModel):
    __tablename__ = "exchange_rates"
    __table_args__ = (
        UniqueConstraint('from_currency', 'to_currency', 'rate_date', name='uq_exchange_rate'),
    )
    
    from_currency = Column(String(3), nullable=False, index=True)
    to_currency = Column(String(3), nullable=False, index=True)
    rate_date = Column(Date, nullable=False, index=True)
    
    # Rate stored as integer with 8 decimal places
    # e.g., 1 USD = 0.307 KWD stored as 30700000
    rate = Column(BigInteger, nullable=False)
    
    source = Column(String(100))  # API source or "manual"
