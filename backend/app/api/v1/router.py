from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, portfolio, equities, fixed_income, real_estate, private_funds, exchange_rates, reports, imports

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["Portfolio"])
api_router.include_router(equities.router, prefix="/holdings/equities", tags=["Equities"])
api_router.include_router(fixed_income.router, prefix="/holdings/fixed-income", tags=["Fixed Income"])
api_router.include_router(real_estate.router, prefix="/real-estate", tags=["Real Estate"])
api_router.include_router(private_funds.router, prefix="/private-funds", tags=["Private Funds"])
api_router.include_router(exchange_rates.router, prefix="/exchange-rates", tags=["Exchange Rates"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(imports.router, prefix="/import", tags=["Import"])
