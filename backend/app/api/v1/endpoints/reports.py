from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from app.core.database import get_db
from app.models.user import User
from app.models.equity import EquityHolding
from app.models.fixed_income import FixedIncomeHolding
from app.models.real_estate import Property, Unit
from app.models.private_fund import PrivateFund
from app.api.deps import get_current_user

router = APIRouter()


def format_money(amount: int, currency: str = "KWD") -> str:
    """Format money amount from smallest unit to display format."""
    if currency == "KWD":
        return f"{amount / 1000:,.3f} KWD"
    return f"{amount / 100:,.2f} {currency}"


@router.get("/pdf")
def generate_pdf_report(
    report_type: str = Query(default="summary"),
    period: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#1a365d')
    )
    
    # Title
    elements.append(Paragraph("ALrashid Family Office", title_style))
    elements.append(Paragraph(f"Portfolio Report - {date.today().strftime('%B %d, %Y')}", styles['Heading2']))
    elements.append(Spacer(1, 20))
    
    if report_type == "summary":
        # Portfolio Summary
        equities = db.query(EquityHolding).filter(EquityHolding.deleted_at.is_(None)).all()
        fixed_income = db.query(FixedIncomeHolding).filter(FixedIncomeHolding.deleted_at.is_(None)).all()
        properties = db.query(Property).filter(Property.deleted_at.is_(None)).all()
        funds = db.query(PrivateFund).filter(PrivateFund.deleted_at.is_(None)).all()
        
        equities_value = sum(e.current_value_kwd or 0 for e in equities)
        fi_value = sum(f.current_value_kwd or f.purchase_price_amount or 0 for f in fixed_income)
        re_value = sum(p.current_value_amount or p.purchase_price_amount or 0 for p in properties)
        pf_value = sum(f.current_nav_kwd or f.called_capital_amount or 0 for f in funds)
        total_value = equities_value + fi_value + re_value + pf_value
        
        summary_data = [
            ['Asset Class', 'Value (KWD)', 'Holdings', '% of Portfolio'],
            ['Public Equities', format_money(equities_value), str(len(equities)), f"{equities_value/total_value*100:.1f}%" if total_value else "0%"],
            ['Fixed Income', format_money(fi_value), str(len(fixed_income)), f"{fi_value/total_value*100:.1f}%" if total_value else "0%"],
            ['Real Estate', format_money(re_value), str(len(properties)), f"{re_value/total_value*100:.1f}%" if total_value else "0%"],
            ['Private Funds', format_money(pf_value), str(len(funds)), f"{pf_value/total_value*100:.1f}%" if total_value else "0%"],
            ['Total Portfolio', format_money(total_value), '', '100%'],
        ]
        
        table = Table(summary_data, colWidths=[2.5*inch, 2*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e2e8f0')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f7fafc')]),
        ]))
        elements.append(table)
        
    elif report_type == "equities":
        elements.append(Paragraph("Public Equities Holdings", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        equities = db.query(EquityHolding).filter(EquityHolding.deleted_at.is_(None)).all()
        
        data = [['Ticker', 'Name', 'Exchange', 'Quantity', 'Cost Basis', 'Current Value', 'Gain/Loss']]
        for e in equities:
            gain_loss = (e.current_value_kwd or 0) - (e.cost_basis_amount or 0)
            data.append([
                e.ticker,
                e.name[:30],
                e.exchange.value if e.exchange else '',
                str(e.quantity),
                format_money(e.cost_basis_amount or 0),
                format_money(e.current_value_kwd or 0),
                format_money(gain_loss)
            ])
        
        table = Table(data, colWidths=[0.8*inch, 2*inch, 1*inch, 0.8*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ]))
        elements.append(table)
        
    elif report_type == "real-estate":
        elements.append(Paragraph("Real Estate Portfolio", styles['Heading2']))
        elements.append(Spacer(1, 10))
        
        properties = db.query(Property).filter(Property.deleted_at.is_(None)).all()
        
        data = [['Property', 'Type', 'Location', 'Purchase Price', 'Current Value', 'Units', 'Ownership']]
        for p in properties:
            units_count = db.query(Unit).filter(Unit.property_id == p.id, Unit.deleted_at.is_(None)).count()
            data.append([
                p.name[:25],
                p.property_type.value if p.property_type else '',
                f"{p.city}, {p.country}",
                format_money(p.purchase_price_amount or 0),
                format_money(p.current_value_amount or p.purchase_price_amount or 0),
                str(units_count),
                f"{p.ownership_percentage/100:.0f}%"
            ])
        
        table = Table(data, colWidths=[1.8*inch, 1*inch, 1.2*inch, 1.2*inch, 1.2*inch, 0.6*inch, 0.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a365d')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e0')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f7fafc')]),
        ]))
        elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=portfolio_report_{date.today()}.pdf"}
    )
