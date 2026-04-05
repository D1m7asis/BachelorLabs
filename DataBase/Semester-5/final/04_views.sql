SET search_path TO publishing, public;

CREATE OR REPLACE VIEW order_details AS
SELECT
  o.id,
  c.name AS customer_name,
  ct.code AS customer_type,
  pt.code AS product_type,
  e.title AS edition_title,
  t.name AS typography_name,
  o.received_at,
  o.completed_at,
  (o.completed_at IS NOT NULL) AS is_completed
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN customer_types ct ON ct.id = c.customer_type_id
JOIN product_types pt ON pt.id = o.product_type_id
JOIN editions e ON e.id = o.edition_id
LEFT JOIN typographies t ON t.id = o.typography_id;

CREATE OR REPLACE VIEW edition_author_details AS
SELECT
  e.id AS edition_id,
  e.title AS edition_title,
  e.sheet_count,
  e.circulation,
  a.id AS author_id,
  a.full_name AS author_name
FROM editions e
JOIN edition_authors ea ON ea.edition_id = e.id
JOIN authors a ON a.id = ea.author_id;
