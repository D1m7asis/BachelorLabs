SET search_path TO publishing, public;

-- 1. IN: найти клиентов, которые делали заказы в типографии "Baltic Typography".
SELECT
    c.id,
    c.name,
    c.phone
FROM customers c
WHERE c.id IN (
    SELECT o.customer_id
    FROM orders o
    JOIN typographies t ON t.id = o.typography_id
    WHERE t.name = 'Baltic Typography'
);

-- 2. NOT IN: найти издания, которые ещё ни разу не заказывались.
SELECT
    e.id,
    e.title
FROM editions e
WHERE e.id NOT IN (
    SELECT o.edition_id
    FROM orders o
);

-- 3. ANY: найти заказы, дата приёма которых не раньше хотя бы одного заказа клиента "Alexey Petrov".
SELECT
    o.id,
    o.received_at,
    c.name AS customer_name
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE o.received_at >= ANY (
    SELECT o2.received_at
    FROM orders o2
    JOIN customers c2 ON c2.id = o2.customer_id
    WHERE c2.name = 'Alexey Petrov'
);

-- 4. ALL: найти издания, тираж которых не меньше тиража всех изданий, заказанных клиентом "Publishing Plus LLC".
SELECT
    e.id,
    e.title,
    e.circulation
FROM editions e
WHERE e.circulation >= ALL (
    SELECT e2.circulation
    FROM orders o2
    JOIN customers c2 ON c2.id = o2.customer_id
    JOIN editions e2 ON e2.id = o2.edition_id
    WHERE c2.name = 'Publishing Plus LLC'
);

-- 5. EXISTS / NOT EXISTS: найти авторов, у которых есть хотя бы одно заказанное издание,
-- а также клиентов, у которых нет ни одного незавершённого заказа.
SELECT
    a.id,
    a.full_name
FROM authors a
WHERE EXISTS (
    SELECT 1
    FROM edition_authors ea
    JOIN orders o ON o.edition_id = ea.edition_id
    WHERE ea.author_id = a.id
);

SELECT
    c.id,
    c.name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM orders o
    WHERE o.customer_id = c.id
      AND o.completed_at IS NULL
);
