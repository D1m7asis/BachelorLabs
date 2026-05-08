# Publishing DB UI

Web UI for the PostgreSQL publishing house database coursework.

## Stack

- Backend: FastAPI, psycopg 3, PostgreSQL.
- Frontend: React, Vite, Recharts, lucide-react.
- Database: existing `publishing` schema from `DataBase/Semester-5/final` plus app views/procedures from `DataBase/app/db`.

## Database

From `DataBase/docker`:

```powershell
docker compose up -d
```

The init scripts load:

1. semester 5 final schema, constraints, seed data, and base views;
2. app views based on semester 6 VIEW work;
3. app stored procedures based on semester 6 laboratory work 7.

If the `pgdata` Docker volume already exists from an older run, PostgreSQL will not re-run init scripts. Recreate the volume when you need a clean database with the new app objects:

```powershell
docker compose down -v
docker compose up -d
```

## Backend

From `DataBase/app/backend`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Frontend

From `DataBase/app/frontend`:

```powershell
npm install
copy .env.example .env
npm run dev
```

UI:

```text
http://127.0.0.1:5173
```

## User Scenarios

- Work in a polished control-room dashboard with metric cards, charts, command navigation, sortable tables, and responsive layouts.
- Review dashboard totals, recent orders, and typography workload.
- Filter all, open, and completed orders.
- Create a new order through `create_order_with_validation`.
- Complete an order through `complete_order_by_id`.
- Search customers and editions.
- Add customers, authors, and typographies through validation procedures.
- Update customer address and edition circulation through procedures.
- Inspect analytics views for customers, typographies, open orders, and completed orders.

When the API is not running, the frontend falls back to demo data and shows a demo-mode banner. This keeps the interface presentable for review while still using the real API as soon as it is available.
