SET search_path TO publishing, public;

-- 1. Найти заказы на издание с максимальным тиражом.
SELECT
    o.id AS order_id,
    c.name AS customer_name,
    e.title AS edition_title,
    e.circulation
FROM orders o
JOIN customers c ON c.id = o.customer_id
JOIN editions e ON e.id = o.edition_id
WHERE e.circulation = (
    SELECT MAX(circulation)
    FROM editions
);

-- 2. Найти издания, у которых тираж выше среднего по всем изданиям.
SELECT
    id,
    title,
    circulation
FROM editions
WHERE circulation > (
    SELECT AVG(circulation)
    FROM editions
);

-- 3. Найти клиентов, у которых число заказов равно максимальному числу заказов среди всех клиентов.
SELECT
    c.id,
    c.name,
    COUNT(o.id) AS orders_count
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.id, c.name
HAVING COUNT(o.id) = (
    SELECT MAX(customer_order_count)
    FROM (
        SELECT COUNT(*) AS customer_order_count
        FROM orders
        GROUP BY customer_id
    ) stats
);

-- 4. Найти авторов, число связанных изданий у которых не меньше среднего числа изданий на автора.
SELECT
    a.id,
    a.full_name,
    COUNT(ea.edition_id) AS editions_count
FROM authors a
JOIN edition_authors ea ON ea.author_id = a.id
GROUP BY a.id, a.full_name
HAVING COUNT(ea.edition_id) >= (
    SELECT AVG(author_edition_count)
    FROM (
        SELECT COUNT(*) AS author_edition_count
        FROM edition_authors
        GROUP BY author_id
    ) stats
);

-- 5. Найти типографии, у которых число заказов равно минимальному числу заказов среди всех типографий.
SELECT
    t.id,
    t.name,
    COUNT(o.id) AS orders_count
FROM typographies t
JOIN orders o ON o.typography_id = t.id
GROUP BY t.id, t.name
HAVING COUNT(o.id) = (
    SELECT MIN(typography_order_count)
    FROM (
        SELECT COUNT(*) AS typography_order_count
        FROM orders
        WHERE typography_id IS NOT NULL
        GROUP BY typography_id
    ) stats
);
