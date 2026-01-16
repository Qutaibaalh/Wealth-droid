from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User
from app.models.currency import ExchangeRate
from app.schemas.common import ExchangeRateResponse
from app.api.deps import get_current_user

router = APIRouter()


@router.get("", response_model=List[ExchangeRateResponse])
def get_exchange_rates(
    base: str = Query(default="KWD"),
    rate_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(ExchangeRate).filter(
        ExchangeRate.from_currency == base,
        ExchangeRate.deleted_at.is_(None)
    )
    
    if rate_date:
        query = query.filter(ExchangeRate.rate_date == rate_date)
    else:
        # Get latest rates
        subquery = db.query(
            ExchangeRate.to_currency,
            db.func.max(ExchangeRate.rate_date).label("max_date")
        ).filter(
            ExchangeRate.from_currency == base
        ).group_by(ExchangeRate.to_currency).subquery()
        
        query = query.join(
            subquery,
            (ExchangeRate.to_currency == subquery.c.to_currency) &
            (ExchangeRate.rate_date == subquery.c.max_date)
        )
    
    rates = query.all()
    
    return [
        ExchangeRateResponse(
            from_currency=r.from_currency,
            to_currency=r.to_currency,
            rate=r.rate / 100000000,  # Convert from stored integer
            rate_date=r.rate_date
        )
        for r in rates
    ]


@router.post("", response_model=ExchangeRateResponse, status_code=status.HTTP_201_CREATED)
def create_exchange_rate(
    from_currency: str,
    to_currency: str,
    rate: float,
    rate_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check if rate already exists
    existing = db.query(ExchangeRate).filter(
        ExchangeRate.from_currency == from_currency,
        ExchangeRate.to_currency == to_currency,
        ExchangeRate.rate_date == rate_date
    ).first()
    
    if existing:
        existing.rate = int(rate * 100000000)
        existing.source = "manual"
        db.commit()
        db.refresh(existing)
        return ExchangeRateResponse(
            from_currency=existing.from_currency,
            to_currency=existing.to_currency,
            rate=rate,
            rate_date=existing.rate_date
        )
    
    exchange_rate = ExchangeRate(
        from_currency=from_currency,
        to_currency=to_currency,
        rate=int(rate * 100000000),
        rate_date=rate_date,
        source="manual"
    )
    db.add(exchange_rate)
    db.commit()
    db.refresh(exchange_rate)
    
    return ExchangeRateResponse(
        from_currency=exchange_rate.from_currency,
        to_currency=exchange_rate.to_currency,
        rate=rate,
        rate_date=exchange_rate.rate_date
    )


@router.get("/convert")
def convert_currency(
    amount: int,
    from_currency: str,
    to_currency: str,
    rate_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if from_currency == to_currency:
        return {"amount": amount, "currency": to_currency}
    
    # Find rate
    query = db.query(ExchangeRate).filter(
        ExchangeRate.from_currency == from_currency,
        ExchangeRate.to_currency == to_currency,
        ExchangeRate.deleted_at.is_(None)
    )
    
    if rate_date:
        query = query.filter(ExchangeRate.rate_date <= rate_date)
    
    rate = query.order_by(ExchangeRate.rate_date.desc()).first()
    
    if not rate:
        # Try reverse
        reverse = db.query(ExchangeRate).filter(
            ExchangeRate.from_currency == to_currency,
            ExchangeRate.to_currency == from_currency,
            ExchangeRate.deleted_at.is_(None)
        ).order_by(ExchangeRate.rate_date.desc()).first()
        
        if not reverse:
            raise HTTPException(
                status_code=404,
                detail=f"Exchange rate not found for {from_currency}/{to_currency}"
            )
        
        converted = int(amount / (reverse.rate / 100000000))
    else:
        converted = int(amount * (rate.rate / 100000000))
    
    return {
        "original_amount": amount,
        "original_currency": from_currency,
        "converted_amount": converted,
        "converted_currency": to_currency
    }
