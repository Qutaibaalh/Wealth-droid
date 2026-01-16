from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.core.database import get_db
from app.models.user import User
from app.models.fixed_income import FixedIncomeHolding, FixedIncomeType
from app.schemas.fixed_income import FixedIncomeCreate, FixedIncomeUpdate, FixedIncomeResponse
from app.schemas.common import PaginatedResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("", response_model=PaginatedResponse[FixedIncomeResponse])
def list_fixed_income(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    instrument_type: Optional[FixedIncomeType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(FixedIncomeHolding).filter(FixedIncomeHolding.deleted_at.is_(None))
    
    if instrument_type:
        query = query.filter(FixedIncomeHolding.instrument_type == instrument_type)
    
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )


@router.post("", response_model=FixedIncomeResponse, status_code=status.HTTP_201_CREATED)
def create_fixed_income(
    holding_in: FixedIncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = FixedIncomeHolding(**holding_in.model_dump())
    db.add(holding)
    db.commit()
    db.refresh(holding)
    return holding


@router.get("/{holding_id}", response_model=FixedIncomeResponse)
def get_fixed_income(
    holding_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = db.query(FixedIncomeHolding).filter(
        FixedIncomeHolding.id == holding_id,
        FixedIncomeHolding.deleted_at.is_(None)
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    return holding


@router.put("/{holding_id}", response_model=FixedIncomeResponse)
def update_fixed_income(
    holding_id: UUID,
    holding_in: FixedIncomeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = db.query(FixedIncomeHolding).filter(
        FixedIncomeHolding.id == holding_id,
        FixedIncomeHolding.deleted_at.is_(None)
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    for field, value in holding_in.model_dump(exclude_unset=True).items():
        setattr(holding, field, value)
    
    db.commit()
    db.refresh(holding)
    return holding


@router.delete("/{holding_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fixed_income(
    holding_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    holding = db.query(FixedIncomeHolding).filter(
        FixedIncomeHolding.id == holding_id,
        FixedIncomeHolding.deleted_at.is_(None)
    ).first()
    
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    
    holding.deleted_at = datetime.utcnow()
    db.commit()
