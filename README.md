# ALrashid Portfolio Management

Comprehensive portfolio management dashboard for ALrashid family office.

## Quick Start

### Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# Run database migrations
docker-compose exec backend alembic upgrade head

# Seed initial data (creates admin user)
docker-compose exec backend python scripts/seed_data.py
```

Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env

# Run migrations
alembic upgrade head

# Seed data
python scripts/seed_data.py

# Start server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

## Default Users

After seeding:
- Admin: `admin` / `admin123`
- CFO: `cfo` / `cfo123`
- IC Member: `ic_member` / `ic123`

## Tech Stack

- **Frontend**: React 18, TypeScript, Tailwind CSS, Recharts
- **Backend**: FastAPI, SQLAlchemy, Alembic
- **Database**: PostgreSQL
- **Auth**: JWT tokens with role-based access

## Features

- Multi-asset class tracking (Equities, Fixed Income, Real Estate, Private Funds)
- Multi-currency support with KWD as base currency
- Role-based dashboards and permissions
- Real estate unit management with occupancy reports
- Private fund capital calls and distributions tracking
- PDF report generation
- Audit logging
