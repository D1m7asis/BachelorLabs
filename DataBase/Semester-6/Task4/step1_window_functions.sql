SET search_path TO publishing, public;

-- 1. Для каждого заказа показать средний, минимальный и максимальный тираж изданий по клиенту.
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    e.title AS edition_title,
    e.circulation,
    AVG(e.circulation) OVER (PARTITION BY c.id) AS avg_circulation_by_customer,
    MIN(e.circulation) OVER (PARTITION BY c.id) AS min_circulation_by_customer,
    MAX(e.circulation) OVER (PARTITION BY c.id) AS max_circulation_by_customer
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN editions e ON e.id = o.edition_id
ORDER BY c.name, o.id;

-- 2. Для каждого заказа показать разницу между тиражом издания и средним тиражом заказов клиента.
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    e.title AS edition_title,
    e.circulation,
    AVG(e.circulation) OVER (PARTITION BY c.id) AS avg_circulation_by_customer,
    e.circulation - AVG(e.circulation) OVER (PARTITION BY c.id) AS diff_from_customer_avg
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN editions e ON e.id = o.edition_id
ORDER BY c.name, o.id;

-- 3. Отсортировать заказы по средней дате приёма заказов клиента.
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    o.received_at,
    AVG(EXTRACT(EPOCH FROM o.received_at::timestamp))
      OVER (PARTITION BY c.id) AS avg_received_at_epoch
FROM orders o
JOIN customers c ON c.id = o.customer_id
ORDER BY AVG(EXTRACT(EPOCH FROM o.received_at::timestamp))
           OVER (PARTITION BY c.id), o.received_at;

-- 4. Показать накопительное число заказов по каждой типографии.
SELECT
    o.id AS order_id,
    t.name AS typography_name,
    o.received_at,
    COUNT(o.id) OVER (
        PARTITION BY t.id
        ORDER BY o.received_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_orders_count
FROM orders o
JOIN typographies t ON t.id = o.typography_id
ORDER BY t.name, o.received_at;

-- 5. Показать накопительный суммарный тираж заказов по каждому клиенту.
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    e.circulation,
    SUM(e.circulation) OVER (
        PARTITION BY c.id
        ORDER BY o.received_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_circulation_sum
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN editions e ON e.id = o.edition_id
ORDER BY c.name, o.received_at;

-- 6. Показать количество заказов и средний тираж внутри каждого типа продукции.
SELECT
    o.id AS order_id,
    pt.code AS product_type,
    e.circulation,
    COUNT(*) OVER (PARTITION BY pt.id) AS orders_count_by_product_type,
    AVG(e.circulation) OVER (PARTITION BY pt.id) AS avg_circulation_by_product_type
FROM orders o
JOIN product_types pt ON pt.id = o.product_type_id
JOIN editions e ON e.id = o.edition_id
ORDER BY pt.code, o.id;

-- 7. Показать для каждого автора минимальный, максимальный и средний тираж его изданий.
SELECT
    a.full_name AS author_name,
    e.title AS edition_title,
    e.circulation,
    MIN(e.circulation) OVER (PARTITION BY a.id) AS min_circulation_by_author,
    MAX(e.circulation) OVER (PARTITION BY a.id) AS max_circulation_by_author,
    AVG(e.circulation) OVER (PARTITION BY a.id) AS avg_circulation_by_author
FROM authors a
JOIN edition_authors ea ON ea.author_id = a.id
JOIN editions e ON e.id = ea.edition_id
ORDER BY author_name, edition_title;

-- 8. Показать порядковый номер заказа внутри клиента по дате приёма.
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    o.received_at,
    COUNT(*) OVER (
        PARTITION BY c.id
        ORDER BY o.received_at
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS order_sequence_for_customer
FROM orders o
JOIN customers c ON c.id = o.customer_id
ORDER BY c.name, o.received_at;

-- 9. Показать средний тираж изданий по типу клиента для каждого заказа.
SELECT
    o.id AS order_id,
    ct.code AS customer_type,
    e.title AS edition_title,
    e.circulation,
    AVG(e.circulation) OVER (PARTITION BY ct.id) AS avg_circulation_by_customer_type
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN customer_types ct ON ct.id = c.customer_type_id
JOIN editions e ON e.id = o.edition_id
ORDER BY customer_type, o.id;

-- 10. Для каждого заказа показать долю тиража его издания от суммарного тиража заказов той же типографии.
SELECT
    o.id AS order_id,
    t.name AS typography_name,
    e.title AS edition_title,
    e.circulation,
    SUM(e.circulation) OVER (PARTITION BY t.id) AS total_circulation_by_typography,
    ROUND(
        e.circulation::numeric
        / SUM(e.circulation) OVER (PARTITION BY t.id)::numeric,
        4
    ) AS circulation_share
FROM orders o
JOIN typographies t ON t.id = o.typography_id
JOIN editions e ON e.id = o.edition_id
ORDER BY typography_name, o.id;
