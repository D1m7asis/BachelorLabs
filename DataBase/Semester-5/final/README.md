# Final Semester 5 Database

This is the clean final version of the Semester 5 database.

## Files

1. `01_schema.sql` creates the schema and core tables.
2. `02_constraints.sql` adds keys, checks, and useful indexes.
3. `03_seed_data.sql` loads reference data and a richer demo dataset.
4. `04_views.sql` creates convenience views for querying.

## Final model

- The database is created directly in schema `publishing`.
- `customer_types` and `product_types` are the only reference tables.
- `customers` stays a single entity with one address and one phone.
- `typographies` stays a compact standalone directory.
- `editions.sheet_count` replaces the old `volume_sheets`.
- `editions.circulation` replaces the old `print_run`.
- `orders.completed_at` is the only source of truth for completion.
- `orders.edition_id` is required in the final model.

## Main objects

- Tables: `customer_types`, `product_types`, `customers`, `typographies`, `editions`, `authors`, `edition_authors`, `orders`
- Views: `order_details`, `edition_author_details`

## How to run

- Docker bootstrap loads only this folder through `DataBase/docker/init/001_run_semester5_migrations.sql`.
- Manual run order:
  1. `01_schema.sql`
  2. `02_constraints.sql`
  3. `03_seed_data.sql`
  4. `04_views.sql`
