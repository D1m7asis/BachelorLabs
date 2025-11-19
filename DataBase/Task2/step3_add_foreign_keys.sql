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
