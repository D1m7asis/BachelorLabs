SET search_path TO publishing, public;

-- 1. UNION: все названия клиентов и типографий без повторов.
SELECT name AS entity_name, 'customer' AS entity_type
FROM customers
UNION
SELECT name AS entity_name, 'typography' AS entity_type
FROM typographies;

-- 2. UNION ALL: все телефоны клиентов и типографий с сохранением повторов.
SELECT phone, 'customer' AS source_type
FROM customers
UNION ALL
SELECT phone, 'typography' AS source_type
FROM typographies;

-- 3. UNION: все названия изданий и названия типов продукции.
SELECT title AS item_name, 'edition' AS source_type
FROM editions
UNION
SELECT title AS item_name, 'product_type' AS source_type
FROM product_types;

-- 4. INTERSECT: клиенты, у которых есть и завершённые, и незавершённые заказы.
SELECT c.name
FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.completed_at IS NOT NULL
INTERSECT
SELECT c.name
FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.completed_at IS NULL;

-- 5. EXCEPT: издания, которые существуют в базе, но ни разу не фигурируют в незавершённых заказах.
SELECT e.title
FROM editions e
EXCEPT
SELECT e.title
FROM editions e
JOIN orders o ON o.edition_id = e.id
WHERE o.completed_at IS NULL;
