from sqlalchemy import Column, String, BigInteger, Date, ForeignKey, Enum, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class Exchange(str, enum.Enum):
    NYSE = "NYSE"
    NASDAQ = "NASDAQ"
    LSE = "LSE"
    BOURSA_KUWAIT = "BOURSA_KUWAIT"
    TADAWUL = "TADAWUL"
    DFM = "DFM"
    ADX = "ADX"
    QSE = "QSE"
    BAHRAIN = "BAHRAIN"
    MUSCAT = "MUSCAT"
    EGX = "EGX"
    EURONEXT = "EURONEXT"
    HKEX = "HKEX"
    TSE = "TSE"
    OTHER = "OTHER"


class HoldingStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    PARTIAL = "partial"
    
    @classmethod
    def _missing_(cls, value):
        for member in cls:
            if member.value == value:
                return member
        return None


class CorporateActionType(str, enum.Enum):
    BONUS_SHARES = "bonus_shares"
    RIGHTS_ISSUE = "rights_issue"
    STOCK_SPLIT = "stock_split"
    REVERSE_SPLIT = "reverse_split"
    SPINOFF = "spinoff"


class EquityHolding(BaseModel):
    __tablename__ = "equity_holdings"
    
    ticker = Column(String(20), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    exchange = Column(Enum(Exchange, values_callable=lambda x: [e.value for e in x]), nullable=False)
    sector = Column(String(100))
    country = Column(String(100))
    
    quantity = Column(BigInteger, nullable=False, default=0)  # Current quantity
    cost_basis_amount = Column(BigInteger, nullable=False)  # In smallest currency unit
    cost_basis_currency = Column(String(3), nullable=False, default="KWD")
    
    current_price_amount = Column(BigInteger)  # In smallest currency unit
    current_price_currency = Column(String(3), default="USD")
    current_value_kwd = Column(BigInteger)  # Converted to KWD
    
    realized_gain_loss = Column(BigInteger, default=0)  # In KWD fils
    unrealized_gain_loss = Column(BigInteger, default=0)  # In KWD fils
    
    status = Column(Enum(HoldingStatus, values_callable=lambda x: [e.value for e in x]), default=HoldingStatus.OPEN)
    notes = Column(Text)
    
    transactions = relationship("EquityTransaction", back_populates="holding")
    dividends = relationship("Dividend", back_populates="holding")
    corporate_actions = relationship("CorporateAction", back_populates="holding")


class EquityTransaction(BaseModel):
    __tablename__ = "equity_transactions"
    
    holding_id = Column(UUID(as_uuid=True), ForeignKey("equity_holdings.id"), nullable=False)
    transaction_type = Column(String(10), nullable=False)  # BUY or SELL
    quantity = Column(BigInteger, nullable=False)
    price_amount = Column(BigInteger, nullable=False)  # Per share in smallest unit
    price_currency = Column(String(3), nullable=False)
    total_amount = Column(BigInteger, nullable=False)
    total_amount_kwd = Column(BigInteger, nullable=False)
    transaction_date = Column(Date, nullable=False)
    fees_amount = Column(BigInteger, default=0)
    notes = Column(Text)
    
    holding = relationship("EquityHolding", back_populates="transactions")


class Dividend(BaseModel):
    __tablename__ = "dividends"
    
    holding_id = Column(UUID(as_uuid=True), ForeignKey("equity_holdings.id"), nullable=False)
    amount = Column(BigInteger, nullable=False)  # Total dividend
    currency = Column(String(3), nullable=False)
    amount_kwd = Column(BigInteger, nullable=False)
    ex_date = Column(Date, nullable=False)
    payment_date = Column(Date)
    dividend_type = Column(String(50))  # cash, stock, special
    
    holding = relationship("EquityHolding", back_populates="dividends")


class CorporateAction(BaseModel):
    __tablename__ = "corporate_actions"
    
    holding_id = Column(UUID(as_uuid=True), ForeignKey("equity_holdings.id"), nullable=False)
    action_type = Column(Enum(CorporateActionType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    action_date = Column(Date, nullable=False)
    ratio_from = Column(BigInteger)  # For splits: original shares
    ratio_to = Column(BigInteger)  # For splits: new shares
    shares_received = Column(BigInteger)
    notes = Column(Text)
    
    holding = relationship("EquityHolding", back_populates="corporate_actions")
