SET search_path TO publishing, public;

ALTER TABLE customer_types
  DROP CONSTRAINT IF EXISTS uq_customer_types_title,
  DROP CONSTRAINT IF EXISTS chk_customer_types_code_not_blank,
  DROP CONSTRAINT IF EXISTS chk_customer_types_title_not_blank,
  ADD CONSTRAINT uq_customer_types_title UNIQUE (title),
  ADD CONSTRAINT chk_customer_types_code_not_blank CHECK (btrim(code) <> ''),
  ADD CONSTRAINT chk_customer_types_title_not_blank CHECK (btrim(title) <> '');

ALTER TABLE product_types
  DROP CONSTRAINT IF EXISTS uq_product_types_title,
  DROP CONSTRAINT IF EXISTS chk_product_types_code_not_blank,
  DROP CONSTRAINT IF EXISTS chk_product_types_title_not_blank,
  ADD CONSTRAINT uq_product_types_title UNIQUE (title),
  ADD CONSTRAINT chk_product_types_code_not_blank CHECK (btrim(code) <> ''),
  ADD CONSTRAINT chk_product_types_title_not_blank CHECK (btrim(title) <> '');

ALTER TABLE customers
  DROP CONSTRAINT IF EXISTS fk_customers_customer_type,
  DROP CONSTRAINT IF EXISTS uq_customers_phone,
  DROP CONSTRAINT IF EXISTS chk_customers_name_not_blank,
  DROP CONSTRAINT IF EXISTS chk_customers_address_not_blank,
  DROP CONSTRAINT IF EXISTS chk_customers_phone_format,
  DROP CONSTRAINT IF EXISTS chk_customers_contact_name_not_blank,
  DROP CONSTRAINT IF EXISTS chk_customers_fax_format,
  ADD CONSTRAINT fk_customers_customer_type
    FOREIGN KEY (customer_type_id) REFERENCES customer_types(id),
  ADD CONSTRAINT uq_customers_phone UNIQUE (phone),
  ADD CONSTRAINT chk_customers_name_not_blank CHECK (btrim(name) <> ''),
  ADD CONSTRAINT chk_customers_address_not_blank CHECK (btrim(address) <> ''),
  ADD CONSTRAINT chk_customers_phone_format CHECK (phone ~ '^[0-9+() -]+$'),
  ADD CONSTRAINT chk_customers_contact_name_not_blank CHECK (contact_name IS NULL OR btrim(contact_name) <> ''),
  ADD CONSTRAINT chk_customers_fax_format CHECK (fax IS NULL OR fax ~ '^[0-9+() -]+$');

ALTER TABLE typographies
  DROP CONSTRAINT IF EXISTS uq_typographies_identity,
  DROP CONSTRAINT IF EXISTS uq_typographies_name,
  DROP CONSTRAINT IF EXISTS chk_typographies_name_not_blank,
  DROP CONSTRAINT IF EXISTS chk_typographies_address_not_blank,
  DROP CONSTRAINT IF EXISTS chk_typographies_phone_format,
  ADD CONSTRAINT uq_typographies_identity UNIQUE NULLS NOT DISTINCT (name, address, phone),
  ADD CONSTRAINT uq_typographies_name UNIQUE (name),
  ADD CONSTRAINT chk_typographies_name_not_blank CHECK (btrim(name) <> ''),
  ADD CONSTRAINT chk_typographies_address_not_blank CHECK (btrim(address) <> ''),
  ADD CONSTRAINT chk_typographies_phone_format CHECK (phone ~ '^[0-9+() -]+$');

ALTER TABLE editions
  DROP CONSTRAINT IF EXISTS uq_editions_title,
  DROP CONSTRAINT IF EXISTS chk_editions_title_not_blank,
  DROP CONSTRAINT IF EXISTS chk_editions_sheet_count,
  DROP CONSTRAINT IF EXISTS chk_editions_circulation,
  ADD CONSTRAINT uq_editions_title UNIQUE (title),
  ADD CONSTRAINT chk_editions_title_not_blank CHECK (btrim(title) <> ''),
  ADD CONSTRAINT chk_editions_sheet_count CHECK (sheet_count > 0),
  ADD CONSTRAINT chk_editions_circulation CHECK (circulation > 0);

ALTER TABLE authors
  DROP CONSTRAINT IF EXISTS uq_authors_full_name_address,
  DROP CONSTRAINT IF EXISTS chk_authors_full_name_not_blank,
  DROP CONSTRAINT IF EXISTS chk_authors_phone_format,
  DROP CONSTRAINT IF EXISTS chk_authors_bio_not_blank,
  ADD CONSTRAINT uq_authors_full_name_address UNIQUE NULLS NOT DISTINCT (full_name, address),
  ADD CONSTRAINT chk_authors_full_name_not_blank CHECK (btrim(full_name) <> ''),
  ADD CONSTRAINT chk_authors_phone_format CHECK (phone IS NULL OR phone ~ '^[0-9+() -]+$'),
  ADD CONSTRAINT chk_authors_bio_not_blank CHECK (bio IS NULL OR btrim(bio) <> '');

ALTER TABLE edition_authors
  DROP CONSTRAINT IF EXISTS pk_edition_authors,
  DROP CONSTRAINT IF EXISTS fk_edition_authors_edition,
  DROP CONSTRAINT IF EXISTS fk_edition_authors_author,
  ADD CONSTRAINT pk_edition_authors PRIMARY KEY (edition_id, author_id),
  ADD CONSTRAINT fk_edition_authors_edition
    FOREIGN KEY (edition_id) REFERENCES editions(id) ON DELETE CASCADE,
  ADD CONSTRAINT fk_edition_authors_author
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE;

ALTER TABLE orders
  DROP CONSTRAINT IF EXISTS fk_orders_customer,
  DROP CONSTRAINT IF EXISTS fk_orders_product_type,
  DROP CONSTRAINT IF EXISTS fk_orders_edition,
  DROP CONSTRAINT IF EXISTS fk_orders_typography,
  DROP CONSTRAINT IF EXISTS chk_orders_completed_at,
  ADD CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
  ADD CONSTRAINT fk_orders_product_type
    FOREIGN KEY (product_type_id) REFERENCES product_types(id),
  ADD CONSTRAINT fk_orders_edition
    FOREIGN KEY (edition_id) REFERENCES editions(id),
  ADD CONSTRAINT fk_orders_typography
    FOREIGN KEY (typography_id) REFERENCES typographies(id) ON DELETE SET NULL,
  ADD CONSTRAINT chk_orders_completed_at
    CHECK (completed_at IS NULL OR completed_at >= received_at);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_product_type_id ON orders(product_type_id);
CREATE INDEX IF NOT EXISTS idx_orders_edition_id ON orders(edition_id);
CREATE INDEX IF NOT EXISTS idx_orders_typography_id ON orders(typography_id);
CREATE INDEX IF NOT EXISTS idx_orders_received_at ON orders(received_at);
CREATE INDEX IF NOT EXISTS idx_edition_authors_author_id ON edition_authors(author_id);
