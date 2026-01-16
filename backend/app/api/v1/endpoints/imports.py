from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import csv
import io
from app.core.database import get_db
from app.models.user import User
from app.models.equity import EquityHolding
from app.models.fixed_income import FixedIncomeHolding
from app.models.real_estate import Property
from app.models.private_fund import PrivateFund
from app.api.deps import get_current_user
from pydantic import BaseModel

router = APIRouter()


class ImportError(BaseModel):
    row: int
    message: str


class ImportResult(BaseModel):
    success: bool
    created: int
    errors: List[ImportError]


def parse_int(value: str, default: int = 0) -> int:
    try:
        return int(float(value)) if value else default
    except ValueError:
        return default


def parse_date(value: str) -> str:
    if not value:
        return None
    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y']:
        try:
            return datetime.strptime(value.strip(), fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return value


def parse_csv(content: bytes) -> List[dict]:
    text = content.decode('utf-8-sig')
    reader = csv.DictReader(io.StringIO(text))
    rows = []
    for row in reader:
        cleaned = {k.lower().strip(): v.strip() for k, v in row.items() if k}
        rows.append(cleaned)
    return rows


@router.post("/equities", response_model=ImportResult)
async def import_equities(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ['admin', 'cfo', 'accountant']:
        raise HTTPException(status_code=403, detail="Not authorized to import data")
    
    content = await file.read()
    rows = parse_csv(content)
    
    created = 0
    errors = []
    
    for i, row in enumerate(rows, start=2):
        try:
            if not row.get('ticker'):
                errors.append(ImportError(row=i, message="Missing ticker"))
                continue
            
            holding = EquityHolding(
                ticker=row.get('ticker', '').upper(),
                name=row.get('name', row.get('ticker', '')),
                exchange=row.get('exchange', 'NYSE'),
                sector=row.get('sector'),
                country=row.get('country'),
                quantity=parse_int(row.get('quantity', '0')),
                cost_basis_amount=parse_int(row.get('cost_basis_amount', '0')),
                cost_basis_currency=row.get('cost_basis_currency', 'USD'),
                status='open'
            )
            db.add(holding)
            created += 1
        except Exception as e:
            errors.append(ImportError(row=i, message=str(e)))
    
    if created > 0:
        db.commit()
    
    return ImportResult(
        success=len(errors) == 0,
        created=created,
        errors=errors
    )


@router.post("/fixed-income", response_model=ImportResult)
async def import_fixed_income(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ['admin', 'cfo', 'accountant']:
        raise HTTPException(status_code=403, detail="Not authorized to import data")
    
    content = await file.read()
    rows = parse_csv(content)
    
    created = 0
    errors = []
    
    for i, row in enumerate(rows, start=2):
        try:
            if not row.get('name'):
                errors.append(ImportError(row=i, message="Missing name"))
                continue
            
            holding = FixedIncomeHolding(
                name=row.get('name'),
                isin=row.get('isin'),
                instrument_type=row.get('instrument_type', 'corporate_bond'),
                issuer=row.get('issuer'),
                face_value_amount=parse_int(row.get('face_value_amount', '0')),
                face_value_currency=row.get('face_value_currency', 'USD'),
                purchase_price_amount=parse_int(row.get('purchase_price_amount', '0')),
                purchase_price_currency=row.get('purchase_price_currency', 'USD'),
                purchase_date=parse_date(row.get('purchase_date')),
                coupon_rate=parse_int(row.get('coupon_rate', '0')),
                maturity_date=parse_date(row.get('maturity_date')),
                status='active'
            )
            db.add(holding)
            created += 1
        except Exception as e:
            errors.append(ImportError(row=i, message=str(e)))
    
    if created > 0:
        db.commit()
    
    return ImportResult(
        success=len(errors) == 0,
        created=created,
        errors=errors
    )


@router.post("/real-estate", response_model=ImportResult)
async def import_real_estate(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ['admin', 'cfo', 'accountant']:
        raise HTTPException(status_code=403, detail="Not authorized to import data")
    
    content = await file.read()
    rows = parse_csv(content)
    
    created = 0
    errors = []
    
    for i, row in enumerate(rows, start=2):
        try:
            if not row.get('name'):
                errors.append(ImportError(row=i, message="Missing property name"))
                continue
            
            prop = Property(
                name=row.get('name'),
                property_type=row.get('property_type', 'commercial'),
                address=row.get('address'),
                city=row.get('city'),
                country=row.get('country', 'Kuwait'),
                purchase_price_amount=parse_int(row.get('purchase_price_amount', '0')),
                purchase_price_currency=row.get('purchase_price_currency', 'KWD'),
                purchase_date=parse_date(row.get('purchase_date')),
                ownership_entity=row.get('ownership_entity'),
                ownership_percentage=parse_int(row.get('ownership_percentage', '10000'))
            )
            db.add(prop)
            created += 1
        except Exception as e:
            errors.append(ImportError(row=i, message=str(e)))
    
    if created > 0:
        db.commit()
    
    return ImportResult(
        success=len(errors) == 0,
        created=created,
        errors=errors
    )


@router.post("/private-funds", response_model=ImportResult)
async def import_private_funds(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in ['admin', 'cfo', 'accountant']:
        raise HTTPException(status_code=403, detail="Not authorized to import data")
    
    content = await file.read()
    rows = parse_csv(content)
    
    created = 0
    errors = []
    
    for i, row in enumerate(rows, start=2):
        try:
            if not row.get('name'):
                errors.append(ImportError(row=i, message="Missing fund name"))
                continue
            
            fund = PrivateFund(
                name=row.get('name'),
                fund_type=row.get('fund_type', 'private_equity'),
                fund_manager=row.get('fund_manager'),
                vintage_year=parse_int(row.get('vintage_year', str(datetime.now().year))),
                geography=row.get('geography', 'MENA'),
                sector=row.get('sector'),
                committed_capital_amount=parse_int(row.get('committed_capital_amount', '0')),
                committed_capital_currency=row.get('committed_capital_currency', 'USD'),
                called_capital_amount=0,
                uncalled_capital_amount=parse_int(row.get('committed_capital_amount', '0')),
                status='active'
            )
            db.add(fund)
            created += 1
        except Exception as e:
            errors.append(ImportError(row=i, message=str(e)))
    
    if created > 0:
        db.commit()
    
    return ImportResult(
        success=len(errors) == 0,
        created=created,
        errors=errors
    )
