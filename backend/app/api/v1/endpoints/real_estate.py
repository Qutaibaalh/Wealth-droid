from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.models.user import User
from app.models.real_estate import Property, Unit, RentalIncome, PropertyExpense, PropertyValuation, UnitStatus
from app.schemas.real_estate import (
    PropertyCreate, PropertyUpdate, PropertyResponse,
    UnitCreate, UnitUpdate, UnitResponse,
    RentalIncomeCreate, RentalIncomeResponse,
    PropertyExpenseCreate, PropertyExpenseResponse,
    OccupancyReport
)
from app.schemas.common import PaginatedResponse
from app.api.deps import get_current_user

router = APIRouter()


# Properties
@router.get("/properties", response_model=PaginatedResponse[PropertyResponse])
def list_properties(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Property).filter(Property.deleted_at.is_(None))
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.post("/properties", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(
    property_in: PropertyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prop = Property(**property_in.model_dump())
    db.add(prop)
    db.commit()
    db.refresh(prop)
    return prop


@router.get("/properties/{property_id}", response_model=PropertyResponse)
def get_property(
    property_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prop = db.query(Property).filter(
        Property.id == property_id,
        Property.deleted_at.is_(None)
    ).first()
    
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    return prop


@router.put("/properties/{property_id}", response_model=PropertyResponse)
def update_property(
    property_id: UUID,
    property_in: PropertyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prop = db.query(Property).filter(
        Property.id == property_id,
        Property.deleted_at.is_(None)
    ).first()
    
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    for field, value in property_in.model_dump(exclude_unset=True).items():
        setattr(prop, field, value)
    
    db.commit()
    db.refresh(prop)
    return prop


@router.delete("/properties/{property_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_property(
    property_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prop = db.query(Property).filter(
        Property.id == property_id,
        Property.deleted_at.is_(None)
    ).first()
    
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    prop.deleted_at = datetime.utcnow()
    db.commit()


# Units
@router.get("/properties/{property_id}/units", response_model=List[UnitResponse])
def list_units(
    property_id: UUID,
    status: Optional[UnitStatus] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Unit).filter(
        Unit.property_id == property_id,
        Unit.deleted_at.is_(None)
    )
    
    if status:
        query = query.filter(Unit.status == status)
    
    return query.all()


@router.post("/properties/{property_id}/units", response_model=UnitResponse, status_code=status.HTTP_201_CREATED)
def create_unit(
    property_id: UUID,
    unit_in: UnitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prop = db.query(Property).filter(
        Property.id == property_id,
        Property.deleted_at.is_(None)
    ).first()
    
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    unit = Unit(property_id=property_id, **unit_in.model_dump(exclude={"property_id"}))
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


@router.get("/units/{unit_id}", response_model=UnitResponse)
def get_unit(
    unit_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    unit = db.query(Unit).filter(
        Unit.id == unit_id,
        Unit.deleted_at.is_(None)
    ).first()
    
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@router.put("/units/{unit_id}", response_model=UnitResponse)
def update_unit(
    unit_id: UUID,
    unit_in: UnitUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    unit = db.query(Unit).filter(
        Unit.id == unit_id,
        Unit.deleted_at.is_(None)
    ).first()
    
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    
    for field, value in unit_in.model_dump(exclude_unset=True).items():
        setattr(unit, field, value)
    
    db.commit()
    db.refresh(unit)
    return unit


# Occupancy Report
@router.get("/occupancy-report", response_model=List[OccupancyReport])
def get_occupancy_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    properties = db.query(Property).filter(Property.deleted_at.is_(None)).all()
    reports = []
    
    for prop in properties:
        units = db.query(Unit).filter(
            Unit.property_id == prop.id,
            Unit.deleted_at.is_(None)
        ).all()
        
        total_units = len(units)
        occupied = len([u for u in units if u.status == UnitStatus.OCCUPIED])
        vacant = len([u for u in units if u.status == UnitStatus.VACANT])
        
        total_rent = sum(u.monthly_rent_amount or 0 for u in units if u.status == UnitStatus.OCCUPIED)
        total_outstanding = sum(u.outstanding_amount or 0 for u in units)
        
        reports.append(OccupancyReport(
            property_id=prop.id,
            property_name=prop.name,
            total_units=total_units,
            occupied_units=occupied,
            vacant_units=vacant,
            occupancy_rate=round(occupied / total_units * 100, 2) if total_units > 0 else 0,
            total_monthly_rent=total_rent,
            total_collected=total_rent - total_outstanding,
            total_outstanding=total_outstanding,
            currency="KWD"
        ))
    
    return reports


# Rental Income
@router.post("/units/{unit_id}/rental-income", response_model=RentalIncomeResponse, status_code=status.HTTP_201_CREATED)
def create_rental_income(
    unit_id: UUID,
    income_in: RentalIncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    unit = db.query(Unit).filter(
        Unit.id == unit_id,
        Unit.deleted_at.is_(None)
    ).first()
    
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    
    income = RentalIncome(unit_id=unit_id, **income_in.model_dump(exclude={"unit_id"}))
    db.add(income)
    db.commit()
    db.refresh(income)
    return income


# Property Expenses
@router.post("/properties/{property_id}/expenses", response_model=PropertyExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    property_id: UUID,
    expense_in: PropertyExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    prop = db.query(Property).filter(
        Property.id == property_id,
        Property.deleted_at.is_(None)
    ).first()
    
    if not prop:
        raise HTTPException(status_code=404, detail="Property not found")
    
    expense = PropertyExpense(property_id=property_id, **expense_in.model_dump(exclude={"property_id"}))
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense


@router.get("/properties/{property_id}/expenses", response_model=List[PropertyExpenseResponse])
def list_expenses(
    property_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    expenses = db.query(PropertyExpense).filter(
        PropertyExpense.property_id == property_id,
        PropertyExpense.deleted_at.is_(None)
    ).order_by(PropertyExpense.expense_date.desc()).all()
    return expenses
