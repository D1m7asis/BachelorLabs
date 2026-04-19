SET search_path TO publishing, public;

-- 1. Промаркировать издания по тиражу.
SELECT
    id,
    title,
    circulation,
    CASE
        WHEN circulation < 1500 THEN 'small circulation'
        WHEN circulation BETWEEN 1500 AND 2500 THEN 'medium circulation'
        ELSE 'large circulation'
    END AS circulation_level
FROM editions
ORDER BY title;

-- 2. Вывести клиентов с типом "person" или "organization" в человекочитаемом виде.
SELECT
    c.id,
    c.name,
    CASE
        WHEN ct.code = 'person' THEN 'private customer'
        WHEN ct.code = 'organization' THEN 'organization customer'
        ELSE 'unknown type'
    END AS customer_kind
FROM customers c
JOIN customer_types ct ON ct.id = c.customer_type_id
ORDER BY c.name;

-- 3. Вывести заказы с пометкой "completed" или "in progress".
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    e.title AS edition_title,
    CASE
        WHEN o.completed_at IS NOT NULL THEN 'completed'
        ELSE 'in progress'
    END AS order_status
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN editions e ON e.id = o.edition_id
ORDER BY o.id;

-- 4. Отсортировать заказы так, чтобы незавершённые были выше завершённых.
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    o.received_at,
    o.completed_at
FROM orders o
JOIN customers c ON c.id = o.customer_id
ORDER BY
    CASE
        WHEN o.completed_at IS NULL THEN 0
        ELSE 1
    END,
    o.received_at DESC;

-- 5. Посчитать число завершённых и незавершённых заказов по каждому клиенту.
SELECT
    c.name AS customer_name,
    SUM(CASE WHEN o.completed_at IS NOT NULL THEN 1 ELSE 0 END) AS completed_orders,
    SUM(CASE WHEN o.completed_at IS NULL THEN 1 ELSE 0 END) AS open_orders
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
ORDER BY c.name;

-- 6. Посчитать число заказов по категориям тиража изданий.
SELECT
    CASE
        WHEN e.circulation < 1500 THEN 'small circulation'
        WHEN e.circulation BETWEEN 1500 AND 2500 THEN 'medium circulation'
        ELSE 'large circulation'
    END AS circulation_level,
    COUNT(o.id) AS orders_count
FROM editions e
JOIN orders o ON o.edition_id = e.id
GROUP BY
    CASE
        WHEN e.circulation < 1500 THEN 'small circulation'
        WHEN e.circulation BETWEEN 1500 AND 2500 THEN 'medium circulation'
        ELSE 'large circulation'
    END
ORDER BY circulation_level;

-- 7. Вывести типографии и их статус загрузки по числу заказов.
SELECT
    t.name AS typography_name,
    COUNT(o.id) AS orders_count,
    CASE
        WHEN COUNT(o.id) = 0 THEN 'idle'
        WHEN COUNT(o.id) = 1 THEN 'light load'
        ELSE 'active load'
    END AS workload_status
FROM typographies t
LEFT JOIN orders o ON o.typography_id = t.id
GROUP BY t.name
ORDER BY t.name;

-- 8. Найти клиентов, у которых преобладают незавершённые заказы.
SELECT
    c.name AS customer_name,
    SUM(CASE WHEN o.completed_at IS NULL THEN 1 ELSE 0 END) AS open_orders,
    SUM(CASE WHEN o.completed_at IS NOT NULL THEN 1 ELSE 0 END) AS completed_orders
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
HAVING SUM(CASE WHEN o.completed_at IS NULL THEN 1 ELSE 0 END)
     > SUM(CASE WHEN o.completed_at IS NOT NULL THEN 1 ELSE 0 END)
ORDER BY c.name;

-- 9. Показать авторов и категорию продуктивности по числу изданий.
SELECT
    a.full_name AS author_name,
    COUNT(ea.edition_id) AS editions_count,
    CASE
        WHEN COUNT(ea.edition_id) = 1 THEN 'single-edition author'
        WHEN COUNT(ea.edition_id) = 2 THEN 'regular author'
        ELSE 'high-output author'
    END AS productivity_level
FROM authors a
JOIN edition_authors ea ON ea.author_id = a.id
GROUP BY a.full_name
ORDER BY editions_count DESC, author_name;

-- 10. Вывести типы продукции и средний тираж, классифицируя их как high/low demand.
SELECT
    pt.code AS product_type,
    AVG(e.circulation) AS avg_circulation,
    CASE
        WHEN AVG(e.circulation) >= 2000 THEN 'high demand'
        ELSE 'standard demand'
    END AS demand_level
FROM product_types pt
JOIN orders o ON o.product_type_id = pt.id
JOIN editions e ON e.id = o.edition_id
GROUP BY pt.code
ORDER BY pt.code;
