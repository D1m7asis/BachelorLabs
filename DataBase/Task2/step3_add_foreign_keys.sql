-- Step 3: ADD FOREIGN KEY constraints

ALTER TABLE orders
  ADD CONSTRAINT fk_orders_customer FOREIGN KEY(customer_id)
    REFERENCES customers(id) ON DELETE CASCADE;

ALTER TABLE orders
  ADD CONSTRAINT fk_orders_edition FOREIGN KEY(edition_id)
    REFERENCES editions(id) ON DELETE SET NULL;

ALTER TABLE edition_authors
  ADD CONSTRAINT fk_ed_author_edition FOREIGN KEY(edition_id)
    REFERENCES editions(id) ON DELETE CASCADE;

ALTER TABLE edition_authors
  ADD CONSTRAINT fk_ed_author_author FOREIGN KEY(author_id)
    REFERENCES authors(id) ON DELETE CASCADE;

-- 1) FK: заказ → типография
ALTER TABLE orders
  ADD CONSTRAINT fk_orders_typography FOREIGN KEY(typography_id)
    REFERENCES typographies(id) ON DELETE SET NULL;

ALTER TABLE orders
  ADD CONSTRAINT chk_orders_dates
  CHECK (
    date_completed IS NULL
    OR date_completed >= date_received
  );
