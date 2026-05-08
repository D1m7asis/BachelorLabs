SET search_path TO publishing, public;

CREATE OR REPLACE VIEW view_order_details AS
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    c.address AS customer_address,
    ct.code AS customer_type,
    pt.code AS product_type,
    e.title AS edition_title,
    t.name AS typography_name,
    t.address AS typography_address,
    o.received_at,
    o.completed_at,
    (o.completed_at IS NOT NULL) AS is_completed
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN customer_types ct ON ct.id = c.customer_type_id
JOIN product_types pt ON pt.id = o.product_type_id
JOIN editions e ON e.id = o.edition_id
LEFT JOIN typographies t ON t.id = o.typography_id;

CREATE OR REPLACE VIEW view_author_editions AS
SELECT
    a.id AS author_id,
    a.full_name AS author_name,
    e.id AS edition_id,
    e.title AS edition_title,
    e.sheet_count,
    e.circulation
FROM authors a
JOIN edition_authors ea ON ea.author_id = a.id
JOIN editions e ON e.id = ea.edition_id;

CREATE OR REPLACE VIEW view_open_orders AS
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    e.title AS edition_title,
    o.received_at
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN editions e ON e.id = o.edition_id
WHERE o.completed_at IS NULL;

CREATE OR REPLACE VIEW view_completed_orders AS
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    e.title AS edition_title,
    o.received_at,
    o.completed_at
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN editions e ON e.id = o.edition_id
WHERE o.completed_at IS NOT NULL;

CREATE OR REPLACE VIEW view_customer_order_stats AS
SELECT
    c.id AS customer_id,
    c.name AS customer_name,
    COUNT(o.id) AS orders_count,
    COUNT(*) FILTER (WHERE o.completed_at IS NULL) AS open_orders_count,
    COUNT(*) FILTER (WHERE o.completed_at IS NOT NULL) AS completed_orders_count
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name;

CREATE OR REPLACE VIEW view_typography_workload AS
SELECT
    t.id AS typography_id,
    t.name AS typography_name,
    COUNT(o.id) AS orders_count,
    MIN(o.received_at) AS first_order_date,
    MAX(o.received_at) AS last_order_date
FROM typographies t
LEFT JOIN orders o ON o.typography_id = t.id
GROUP BY t.id, t.name;

CREATE OR REPLACE VIEW view_organization_customers AS
SELECT
    c.id,
    c.customer_type_id,
    c.name,
    c.contact_name,
    c.address,
    c.phone,
    c.fax
FROM customers c
WHERE c.customer_type_id = 2
WITH LOCAL CHECK OPTION;

CREATE OR REPLACE VIEW view_person_customers AS
SELECT
    c.id,
    c.customer_type_id,
    c.name,
    c.contact_name,
    c.address,
    c.phone,
    c.fax
FROM customers c
WHERE c.customer_type_id = 1
WITH LOCAL CHECK OPTION;
