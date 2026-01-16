from sqlalchemy import Column, String, BigInteger, Date, ForeignKey, Enum, Text, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.models.base import BaseModel


class PropertyType(str, enum.Enum):
    COMMERCIAL = "commercial"
    RESIDENTIAL = "residential"
    MIXED = "mixed"
    LAND = "land"
    INDUSTRIAL = "industrial"


class UnitStatus(str, enum.Enum):
    OCCUPIED = "occupied"
    VACANT = "vacant"
    UNDER_MAINTENANCE = "under_maintenance"
    RESERVED = "reserved"


class Property(BaseModel):
    __tablename__ = "properties"
    
    name = Column(String(255), nullable=False)
    property_type = Column(Enum(PropertyType, values_callable=lambda x: [e.value for e in x]), nullable=False)
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100), default="Kuwait")
    
    purchase_price_amount = Column(BigInteger, nullable=False)
    purchase_price_currency = Column(String(3), default="KWD")
    purchase_date = Column(Date, nullable=False)
    
    current_value_amount = Column(BigInteger)
    current_value_currency = Column(String(3), default="KWD")
    last_valuation_date = Column(Date)
    
    ownership_entity = Column(String(255))  # SPV or holding company name
    ownership_percentage = Column(Integer, default=10000)  # Basis points (10000 = 100%)
    
    total_area_sqm = Column(BigInteger)  # In square centimeters for precision
    
    irr_bps = Column(Integer)  # IRR in basis points
    
    notes = Column(Text)
    
    units = relationship("Unit", back_populates="property")
    valuations = relationship("PropertyValuation", back_populates="property")
    expenses = relationship("PropertyExpense", back_populates="property")


class Unit(BaseModel):
    __tablename__ = "units"
    
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False)
    unit_number = Column(String(50), nullable=False)
    unit_type = Column(String(50))  # apartment, office, retail, etc.
    floor = Column(Integer)
    area_sqm = Column(BigInteger)  # In square centimeters
    
    status = Column(Enum(UnitStatus, values_callable=lambda x: [e.value for e in x]), default=UnitStatus.VACANT)
    tenant_name = Column(String(255))
    lease_start_date = Column(Date)
    lease_end_date = Column(Date)
    
    monthly_rent_amount = Column(BigInteger)  # In fils
    monthly_rent_currency = Column(String(3), default="KWD")
    budgeted_rent_amount = Column(BigInteger)  # Expected/budgeted rent
    
    deposit_amount = Column(BigInteger, default=0)
    outstanding_amount = Column(BigInteger, default=0)  # Unpaid rent
    
    notes = Column(Text)
    
    property = relationship("Property", back_populates="units")
    rental_income = relationship("RentalIncome", back_populates="unit")


class RentalIncome(BaseModel):
    __tablename__ = "rental_income"
    
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    expected_amount = Column(BigInteger, nullable=False)
    received_amount = Column(BigInteger, default=0)
    currency = Column(String(3), default="KWD")
    
    payment_date = Column(Date)
    is_collected = Column(Boolean, default=False)
    
    notes = Column(Text)
    
    unit = relationship("Unit", back_populates="rental_income")


class PropertyExpense(BaseModel):
    __tablename__ = "property_expenses"
    
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False)
    unit_id = Column(UUID(as_uuid=True), ForeignKey("units.id"), nullable=True)
    
    expense_type = Column(String(100), nullable=False)  # maintenance, utilities, insurance, etc.
    description = Column(Text)
    
    amount = Column(BigInteger, nullable=False)
    currency = Column(String(3), default="KWD")
    expense_date = Column(Date, nullable=False)
    
    vendor_name = Column(String(255))
    invoice_number = Column(String(100))
    
    property = relationship("Property", back_populates="expenses")


class PropertyValuation(BaseModel):
    __tablename__ = "property_valuations"
    
    property_id = Column(UUID(as_uuid=True), ForeignKey("properties.id"), nullable=False)
    valuation_date = Column(Date, nullable=False)
    
    value_amount = Column(BigInteger, nullable=False)
    currency = Column(String(3), default="KWD")
    
    appraiser = Column(String(255))
    valuation_method = Column(String(100))
    notes = Column(Text)
    
    property = relationship("Property", back_populates="valuations")
