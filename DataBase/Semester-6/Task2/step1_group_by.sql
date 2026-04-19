SET search_path TO publishing, public;

-- 1. Сколько заказов у каждого клиента.
SELECT
    c.id AS customer_id,
    c.name AS customer_name,
    COUNT(o.id) AS orders_count
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name;

-- 2. Средний и максимальный тираж изданий по каждому автору.
SELECT
    a.id AS author_id,
    a.full_name AS author_name,
    AVG(e.circulation) AS avg_circulation,
    MAX(e.circulation) AS max_circulation
FROM authors a
JOIN edition_authors ea ON ea.author_id = a.id
JOIN editions e ON e.id = ea.edition_id
GROUP BY a.id, a.full_name;

-- 3. Число завершённых заказов по каждой типографии.
SELECT
    t.id AS typography_id,
    t.name AS typography_name,
    COUNT(o.id) AS completed_orders_count
FROM typographies t
JOIN orders o ON o.typography_id = t.id
WHERE o.completed_at IS NOT NULL
GROUP BY t.id, t.name;

-- 4. Минимальная и максимальная дата приёма заказа по каждому типу продукции.
SELECT
    pt.code AS product_type,
    MIN(o.received_at) AS first_received_at,
    MAX(o.received_at) AS last_received_at
FROM product_types pt
JOIN orders o ON o.product_type_id = pt.id
GROUP BY pt.code
ORDER BY pt.code;

-- 5. Число заказов по каждому изданию, отсортированное по убыванию.
SELECT
    e.title AS edition_title,
    COUNT(o.id) AS orders_count
FROM editions e
JOIN orders o ON o.edition_id = e.id
GROUP BY e.title
ORDER BY orders_count DESC, edition_title;

-- 6. Среднее количество печатных листов по типу клиента.
SELECT
    ct.code AS customer_type,
    AVG(e.sheet_count) AS avg_sheet_count
FROM customer_types ct
JOIN customers c ON c.customer_type_id = ct.id
JOIN orders o ON o.customer_id = c.id
JOIN editions e ON e.id = o.edition_id
GROUP BY ct.code
ORDER BY ct.code;

-- 7. Типографии, у которых больше одного заказа.
SELECT
    t.name AS typography_name,
    COUNT(o.id) AS orders_count
FROM typographies t
JOIN orders o ON o.typography_id = t.id
GROUP BY t.name
HAVING COUNT(o.id) > 1
ORDER BY orders_count DESC, typography_name;

-- 8. Авторы, у которых суммарный тираж их изданий не меньше 4000.
SELECT
    a.full_name AS author_name,
    SUM(e.circulation) AS total_circulation
FROM authors a
JOIN edition_authors ea ON ea.author_id = a.id
JOIN editions e ON e.id = ea.edition_id
GROUP BY a.full_name
HAVING SUM(e.circulation) >= 4000
ORDER BY total_circulation DESC, author_name;

-- 9. Клиенты с более чем одним заказом, у которых есть хотя бы один незавершённый заказ.
SELECT
    c.name AS customer_name,
    COUNT(o.id) AS orders_count,
    COUNT(*) FILTER (WHERE o.completed_at IS NULL) AS open_orders_count
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
HAVING COUNT(o.id) > 1
   AND COUNT(*) FILTER (WHERE o.completed_at IS NULL) > 0
ORDER BY customer_name;

-- 10. По каждому типу продукции: число заказов, средний и максимальный тираж связанных изданий.
SELECT
    pt.code AS product_type,
    COUNT(o.id) AS orders_count,
    AVG(e.circulation) AS avg_circulation,
    MAX(e.circulation) AS max_circulation
FROM product_types pt
JOIN orders o ON o.product_type_id = pt.id
JOIN editions e ON e.id = o.edition_id
GROUP BY pt.code
ORDER BY pt.code;
