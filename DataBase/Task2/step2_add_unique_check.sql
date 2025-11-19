-- Step 2: ADD CHECK and UNIQUE constraints (ALTER TABLE)

ALTER TABLE customers
  ADD CONSTRAINT chk_customer_type CHECK (type IN ('person','organization')),
  ADD CONSTRAINT uq_customer_phone UNIQUE(phone);

ALTER TABLE orders
  ADD CONSTRAINT chk_dates CHECK (date_completed >= date_received),
  ADD CONSTRAINT uq_order_comp UNIQUE(id, customer_id);

ALTER TABLE editions
  ADD CONSTRAINT chk_vol CHECK (volume_sheets > 0),
  ADD CONSTRAINT chk_run CHECK (print_run > 0);

ALTER TABLE authors
  ADD CONSTRAINT uq_author UNIQUE(full_name, address),
  ADD CONSTRAINT chk_author_phone CHECK (phone ~ '^[0-9+\-() ]+$');
