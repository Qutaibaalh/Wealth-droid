A comprehensive portfolio management dashboard for ALrashid family office. Tracks investments across multiple asset classes including public equities, bonds/sukuk, real estate (300+ units), and private funds (30+ investments). Built for the accounting team and investment committee with role-based access for 5+ users.
Tech Stack

Frontend: React 18 + TypeScript + Tailwind CSS
Backend: FastAPI (Python 3.11)
Database: PostgreSQL
Hosting: Local/on-premise server (security requirement)
Auth: Password protection required (username and password)


Business Requirements
Asset Classes to Support
1. Public Equities

Exchanges: All GCC, US (NYSE/NASDAQ), UK/EU, Egypt, Asian markets
Data per holding:

Ticker symbol
Quantity
Cost basis / purchase price
Purchase date
Current market value
Realized gains/losses (from sold positions)
Unrealized gains/losses
Corporate actions: bonus shares, rights issues, stock splits
Dividends received
Selling price and date (for closed positions)


Price updates: Automatic daily updates with historical snapshots preserved or Manual entry 

2. Fixed Income (Bonds, Sukuk, Funds)

Types: Corporate bonds, sukuk, fixed income funds
Data per holding:

Face value
Coupon rate
Maturity date
Current market value (or cost if no fair value available)
IRR to date
Promised/expected returns
Management fees


Trading status: Track both exchange-traded and held-to-maturity

3. Real Estate

Scale: 10+ properties, 300+ units (commercial and residential)
Data per property:

Current estimated value
Purchase price and date
Rental income
Operating expenses
Maintenance costs (unit-wise breakdown)
Occupancy reports
Collection status
Outstanding amounts
IRR
Fair value change history
Actual rent vs budget comparison


Valuations: Updated yearly
Ownership: Held through multiple companies and SPVs (track ownership structure)
Additional features: Procurement process tracking, rental management

4. Private Funds & PE

Scale: 30+ fund investments plus co-investments and direct PE deals
Data per investment:

Committed capital
Called capital
Distributions (declared vs received/paid)
Current NAV
IRR
Management fees
Taxes
Key event dates
Fund manager details


Update frequency: Varies by fund (monthly, quarterly, annually, or on-demand)


Currency Handling
Base Currencies

Primary: KWD (Kuwaiti Dinar)
Secondary: USD

Supported Currencies
KWD, USD, GBP, EUR, AED, SAR, EGP (and others as needed)
Conversion Rules

Automatic conversion using prevailing exchange rates
Manual override capability for specific transactions
Store original currency and converted values separately


User Access & Security
Users

Minimum 5 users with dashboard access
Role-based permissions (full detail vs summary views)
CFO needs different metrics than Investment Committee members

Security Requirements


Password protection required

Audit logging for sensitive actions

Platforms

Desktop and mobile responsive


Dashboard Views & Reporting
Required Views

Total portfolio value over time (line chart)
Allocation by asset class (pie chart)
Performance vs benchmark comparison
Individual asset detail pages
Exposure analysis across multiple dimensions
IRR matrix view

Role-Specific Views

CFO: Additional financial metrics and detailed breakdowns
IC Members: Summary views with key investment metrics

Reports

PDF export capability for family members and meetings
Customizable report templates

Alerts & Notifications

System should support configurable alerts (thresholds, events, etc.)


Data Management
Current State

Data currently in Excel (multiple databases being consolidated)
Historical data needs to be prepared/migrated

Historical Data

Retain data since inception of each active investment
Preserve price history at defined intervals (not just latest)

Update Patterns
Asset TypeUpdate FrequencyMethodPublic equitiesDaily (automatic)API feedBonds/sukukDaily (automatic)API feedReal estateYearly + eventsStructured input formPrivate fundsPer statementStructured input form
Input Forms

Structured input forms required for manual updates
Event-based entry (distributions, valuations, capital calls, etc.)
Data validation and audit trail


Key Metrics & KPIs
Primary Metrics

Portfolio IRR (overall and per asset class)
Exposure breakdowns by:

Asset class
Geography
Currency
Sector/industry
Holding company/SPV


Realized vs unrealized gains
Income yield (dividends, rent, distributions)

Performance Tracking

Benchmark comparison capability
Time-weighted and money-weighted returns
Attribution analysis


Data Model Conventions
Database

All monetary values stored as integers in smallest unit (fils for KWD, cents for USD)
Always store original currency alongside converted values
Dates stored as UTC, displayed in Kuwait timezone (Asia/Kuwait)
Use UUIDs for record IDs
Soft delete pattern (deleted_at column)

Naming

Tables: snake_case (e.g., portfolio_holdings, real_estate_units)
Columns: snake_case
Foreign keys: {table}_id format


API Design
Endpoints Pattern
GET    /api/v1/portfolio/summary
GET    /api/v1/holdings?asset_class=equity
GET    /api/v1/holdings/{id}
POST   /api/v1/holdings
PUT    /api/v1/holdings/{id}
DELETE /api/v1/holdings/{id}

GET    /api/v1/real-estate/properties
GET    /api/v1/real-estate/properties/{id}/units
GET    /api/v1/real-estate/occupancy-report

GET    /api/v1/private-funds
GET    /api/v1/private-funds/{id}/capital-calls
POST   /api/v1/private-funds/{id}/distributions

GET    /api/v1/reports/pdf?type=summary&period=Q4-2025
GET    /api/v1/exchange-rates?base=KWD&date=2025-01-15
Response Format

Always return Pydantic schemas, not raw dicts
Include pagination for list endpoints
Consistent error response structure


Commands
bash# Frontend
cd frontend && npm run dev

# Backend
cd backend && uvicorn app.main:app --reload

# Database
docker-compose up -d postgres
cd backend && alembic upgrade head

# Run tests
cd backend && pytest
cd frontend && npm test


Design Thinking
Before coding, understand the context and commit to a BOLD aesthetic direction:

Purpose: What problem does this interface solve? Who uses it?
Tone: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
Constraints: Technical requirements (framework, performance, accessibility).
Differentiation: What makes this UNFORGETTABLE? What's the one thing someone will remember?
CRITICAL: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:

Production-grade and functional
Visually striking and memorable
Cohesive with a clear aesthetic point-of-view
Meticulously refined in every detail
Frontend Aesthetics Guidelines
Focus on:

Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
Spatial Composition: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
Backgrounds & Visual Details: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.
Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

IMPORTANT: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

<><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Frontend Code Review
Intent
Use this skill whenever the user asks to review frontend code (especially .tsx, .ts, or .js files). Support two review modes:

Pending-change review – inspect staged/working-tree files slated for commit and flag checklist violations before submission.
File-targeted review – review the specific file(s) the user names and report the relevant checklist findings.
Stick to the checklist below for every applicable file and mode.

Checklist
See references/code-quality.md, references/performance.md, references/business-logic.md for the living checklist split by category—treat it as the canonical set of rules to follow.

Flag each rule violation with urgency metadata so future reviewers can prioritize fixes.
Required output
When invoked, the response must exactly follow one of the two templates:

Template A (any findings)
# Code review
Found <N> urgent issues need to be fixed:

## 1 <brief description of bug>
FilePath: <path> line <line>
<relevant code snippet or pointer>


### Suggested fix
<brief description of suggested fix>

---
... (repeat for each urgent issue) ...

Found <M> suggestions for improvement:

## 1 <brief description of suggestion>
FilePath: <path> line <line>
<relevant code snippet or pointer>


### Suggested fix
<brief description of suggested fix>

---

... (repeat for each suggestion) ...
If there are no urgent issues, omit that section. If there are no suggestions, omit that section.


If the issue number is more than 10, summarize as "10+ urgent issues" or "10+ suggestions" and just output the first 10 issues.

Don't compress the blank lines between sections; keep them as-is for readability.

If you use Template A (i.e., there are issues to fix) and at least one issue requires code changes, append a brief follow-up question after the structured output asking whether the user wants you to apply the suggested fix(es). For example: "Would you like me to use the Suggested fix section to address these issues?"

Template B (no issues)
## Code review
No issues found.

<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>
 Plan Mode

- Make the plan extremely concise. Sacrifice grammar for the sake of concision.
- At the end of each plan, give me a list of unresolved questions to answer, if any.
