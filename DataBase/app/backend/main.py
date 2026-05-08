import os
from contextlib import contextmanager
from datetime import date
from typing import Any

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from psycopg import errors
from psycopg.rows import dict_row
from pydantic import BaseModel, Field


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "publishing"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
}


app = FastAPI(
    title="Publishing Database API",
    description="API for the publishing house database coursework UI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@contextmanager
def db_connection():
    conn = psycopg.connect(**DB_CONFIG, row_factory=dict_row)
    try:
        with conn.cursor() as cur:
            cur.execute("SET search_path TO publishing, public")
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def fetch_all(query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return list(cur.fetchall())


def fetch_one(query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            return cur.fetchone()


def execute_call(query: str, params: tuple[Any, ...]) -> dict[str, str]:
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
        return {"status": "ok"}
    except (errors.RaiseException, errors.CheckViolation, errors.UniqueViolation, errors.ForeignKeyViolation) as exc:
        raise HTTPException(status_code=400, detail=str(exc).splitlines()[0]) from exc
    except psycopg.Error as exc:
        raise HTTPException(status_code=500, detail=str(exc).splitlines()[0]) from exc


def call_refcursor(procedure: str, params: tuple[Any, ...], cursor_name: str) -> list[dict[str, Any]]:
    try:
        with db_connection() as conn:
            with conn.cursor() as cur:
                placeholders = ", ".join(["%s"] * (len(params) + 1))
                cur.execute(f"CALL {procedure}({placeholders})", (*params, cursor_name))
                cur.execute(f"FETCH ALL FROM {cursor_name}")
                return list(cur.fetchall())
    except psycopg.Error as exc:
        raise HTTPException(status_code=400, detail=str(exc).splitlines()[0]) from exc


class CustomerCreate(BaseModel):
    customer_type_code: str = Field(pattern="^(person|organization)$")
    name: str = Field(min_length=1)
    contact_name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    phone: str = Field(min_length=3)
    fax: str | None = None


class CustomerAddressUpdate(BaseModel):
    address: str = Field(min_length=1)


class TypographyCreate(BaseModel):
    name: str = Field(min_length=1)
    address: str = Field(min_length=1)
    phone: str = Field(min_length=3)


class AuthorCreate(BaseModel):
    full_name: str = Field(min_length=1)
    address: str | None = None
    phone: str | None = None
    bio: str | None = None


class EditionCirculationUpdate(BaseModel):
    circulation: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: int = Field(gt=0)
    product_type_code: str = Field(min_length=1)
    edition_id: int = Field(gt=0)
    typography_id: int | None = Field(default=None, gt=0)
    received_at: date
    completed_at: date | None = None


class CompleteOrder(BaseModel):
    completed_at: date


@app.get("/health")
def health() -> dict[str, Any]:
    row = fetch_one("SELECT current_database() AS database, current_schema() AS schema")
    return {"status": "ok", "database": row}


@app.get("/dashboard")
def dashboard() -> dict[str, Any]:
    totals = fetch_one(
        """
        SELECT
            COUNT(*) AS total_orders,
            COUNT(*) FILTER (WHERE completed_at IS NULL) AS open_orders,
            COUNT(*) FILTER (WHERE completed_at IS NOT NULL) AS completed_orders
        FROM orders
        """
    )
    active_typographies = fetch_one(
        """
        SELECT COUNT(*) AS active_typographies
        FROM (
            SELECT typography_id
            FROM orders
            WHERE typography_id IS NOT NULL
            GROUP BY typography_id
        ) t
        """
    )
    latest_orders = fetch_all(
        """
        SELECT *
        FROM view_order_details
        ORDER BY received_at DESC, order_id DESC
        LIMIT 6
        """
    )
    customer_stats = fetch_all(
        """
        SELECT *
        FROM view_customer_order_stats
        ORDER BY orders_count DESC, customer_name
        LIMIT 5
        """
    )
    typography_workload = fetch_all(
        """
        SELECT *
        FROM view_typography_workload
        ORDER BY orders_count DESC, typography_name
        """
    )
    return {
        "totals": totals,
        "active_typographies": active_typographies["active_typographies"],
        "latest_orders": latest_orders,
        "customer_stats": customer_stats,
        "typography_workload": typography_workload,
    }


@app.get("/orders")
def orders_list(status: str = Query("all", pattern="^(all|open|completed)$")) -> list[dict[str, Any]]:
    where = ""
    if status == "open":
        where = "WHERE completed_at IS NULL"
    elif status == "completed":
        where = "WHERE completed_at IS NOT NULL"
    return fetch_all(
        f"""
        SELECT *
        FROM view_order_details
        {where}
        ORDER BY received_at DESC, order_id DESC
        """
    )


@app.post("/orders")
def create_order(payload: OrderCreate) -> dict[str, str]:
    return execute_call(
        "CALL create_order_with_validation(%s, %s, %s, %s, %s, %s)",
        (
            payload.customer_id,
            payload.product_type_code,
            payload.edition_id,
            payload.typography_id,
            payload.received_at,
            payload.completed_at,
        ),
    )


@app.post("/orders/{order_id}/complete")
def complete_order(order_id: int, payload: CompleteOrder) -> dict[str, str]:
    return execute_call(
        "CALL complete_order_by_id(%s, %s)",
        (order_id, payload.completed_at),
    )


@app.get("/customers")
def customers(q: str = "") -> list[dict[str, Any]]:
    if q:
        return call_refcursor("find_customers_by_name_part", (q,), "cur_customers_by_name")
    return fetch_all(
        """
        SELECT
            c.id,
            c.name,
            ct.code AS customer_type_code,
            ct.title AS customer_type,
            c.contact_name,
            c.address,
            c.phone,
            c.fax
        FROM customers c
        JOIN customer_types ct ON ct.id = c.customer_type_id
        ORDER BY c.name
        """
    )


@app.post("/customers")
def create_customer(payload: CustomerCreate) -> dict[str, str]:
    return execute_call(
        "CALL add_customer_with_validation(%s, %s, %s, %s, %s, %s)",
        (
            payload.customer_type_code,
            payload.name,
            payload.contact_name,
            payload.address,
            payload.phone,
            payload.fax,
        ),
    )


@app.patch("/customers/{customer_id}/address")
def update_customer_address(customer_id: int, payload: CustomerAddressUpdate) -> dict[str, str]:
    return execute_call("CALL update_customer_address(%s, %s)", (customer_id, payload.address))


@app.get("/editions")
def editions(q: str = "") -> list[dict[str, Any]]:
    if q:
        return call_refcursor("find_editions_by_title_part", (q,), "cur_editions_by_title")
    return fetch_all("SELECT id, title, sheet_count, circulation FROM editions ORDER BY title")


@app.patch("/editions/{edition_id}/circulation")
def update_edition_circulation(edition_id: int, payload: EditionCirculationUpdate) -> dict[str, str]:
    return execute_call("CALL update_edition_circulation(%s, %s)", (edition_id, payload.circulation))


@app.get("/authors")
def authors(q: str = "") -> list[dict[str, Any]]:
    return fetch_all(
        """
        SELECT id, full_name, address, phone, bio
        FROM authors
        WHERE full_name ILIKE %s
        ORDER BY full_name
        """,
        (f"%{q}%",),
    )


@app.post("/authors")
def create_author(payload: AuthorCreate) -> dict[str, str]:
    return execute_call(
        "CALL add_author_with_validation(%s, %s, %s, %s)",
        (payload.full_name, payload.address, payload.phone, payload.bio),
    )


@app.get("/typographies")
def typographies(q: str = "") -> list[dict[str, Any]]:
    return fetch_all(
        """
        SELECT id, name, address, phone
        FROM typographies
        WHERE name ILIKE %s
        ORDER BY name
        """,
        (f"%{q}%",),
    )


@app.post("/typographies")
def create_typography(payload: TypographyCreate) -> dict[str, str]:
    return execute_call(
        "CALL add_typography_with_validation(%s, %s, %s)",
        (payload.name, payload.address, payload.phone),
    )


@app.get("/reference/product-types")
def product_types() -> list[dict[str, Any]]:
    return fetch_all("SELECT code, title FROM product_types ORDER BY title")


@app.get("/analytics/customer-stats")
def analytics_customer_stats() -> list[dict[str, Any]]:
    return fetch_all("SELECT * FROM view_customer_order_stats ORDER BY orders_count DESC, customer_name")


@app.get("/analytics/typography-workload")
def analytics_typography_workload() -> list[dict[str, Any]]:
    return fetch_all("SELECT * FROM view_typography_workload ORDER BY orders_count DESC, typography_name")


@app.get("/analytics/open-orders")
def analytics_open_orders() -> list[dict[str, Any]]:
    return fetch_all("SELECT * FROM view_open_orders ORDER BY received_at")


@app.get("/analytics/completed-orders")
def analytics_completed_orders() -> list[dict[str, Any]]:
    return fetch_all("SELECT * FROM view_completed_orders ORDER BY completed_at DESC")
