SET search_path TO publishing, public;

-- 1. Ранжировать издания по тиражу.
SELECT
    id,
    title,
    circulation,
    RANK() OVER (ORDER BY circulation DESC) AS circulation_rank
FROM editions
ORDER BY circulation_rank, title;

-- 2. Плотно ранжировать издания по количеству печатных листов.
SELECT
    id,
    title,
    sheet_count,
    DENSE_RANK() OVER (ORDER BY sheet_count DESC) AS sheet_count_dense_rank
FROM editions
ORDER BY sheet_count_dense_rank, title;

-- 3. Нумерация заказов внутри каждого клиента по дате приёма.
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    o.received_at,
    ROW_NUMBER() OVER (
        PARTITION BY c.id
        ORDER BY o.received_at
    ) AS order_number_for_customer
FROM orders o
JOIN customers c ON c.id = o.customer_id
ORDER BY c.name, order_number_for_customer;

-- 4. Ранжировать заказы по тиражу издания внутри каждой типографии.
SELECT
    o.id AS order_id,
    t.name AS typography_name,
    e.title AS edition_title,
    e.circulation,
    RANK() OVER (
        PARTITION BY t.id
        ORDER BY e.circulation DESC
    ) AS circulation_rank_in_typography
FROM orders o
JOIN typographies t ON t.id = o.typography_id
JOIN editions e ON e.id = o.edition_id
ORDER BY typography_name, circulation_rank_in_typography, edition_title;

-- 5. Плотно ранжировать авторов по количеству изданий.
SELECT
    a.full_name AS author_name,
    COUNT(ea.edition_id) AS editions_count,
    DENSE_RANK() OVER (
        ORDER BY COUNT(ea.edition_id) DESC
    ) AS author_dense_rank
FROM authors a
JOIN edition_authors ea ON ea.author_id = a.id
GROUP BY a.id, a.full_name
ORDER BY author_dense_rank, author_name;

-- 6. Разбить издания на 3 группы по тиражу.
SELECT
    id,
    title,
    circulation,
    NTILE(3) OVER (ORDER BY circulation DESC) AS circulation_bucket
FROM editions
ORDER BY circulation DESC, title;

-- 7. Показать процентный ранг заказа по дате внутри клиента.
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    o.received_at,
    PERCENT_RANK() OVER (
        PARTITION BY c.id
        ORDER BY o.received_at
    ) AS percent_rank_by_customer
FROM orders o
JOIN customers c ON c.id = o.customer_id
ORDER BY c.name, o.received_at;

-- 8. Показать накопленную долю заказов по типу продукции.
SELECT
    o.id AS order_id,
    pt.code AS product_type,
    o.received_at,
    CUME_DIST() OVER (
        PARTITION BY pt.id
        ORDER BY o.received_at
    ) AS cume_dist_by_product_type
FROM orders o
JOIN product_types pt ON pt.id = o.product_type_id
ORDER BY product_type, o.received_at;

-- 9. Нумерация изданий внутри автора по убыванию тиража.
SELECT
    a.full_name AS author_name,
    e.title AS edition_title,
    e.circulation,
    ROW_NUMBER() OVER (
        PARTITION BY a.id
        ORDER BY e.circulation DESC, e.title
    ) AS edition_row_number_for_author
FROM authors a
JOIN edition_authors ea ON ea.author_id = a.id
JOIN editions e ON e.id = ea.edition_id
ORDER BY author_name, edition_row_number_for_author;

-- 10. Ранг клиентов по количеству заказов.
SELECT
    c.name AS customer_name,
    COUNT(o.id) AS orders_count,
    RANK() OVER (
        ORDER BY COUNT(o.id) DESC
    ) AS customer_rank,
    DENSE_RANK() OVER (
        ORDER BY COUNT(o.id) DESC
    ) AS customer_dense_rank
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name
ORDER BY customer_rank, customer_name;
