-- Запрос 1: DISTINCT по типам заказчиков, у которых есть заказы
SELECT DISTINCT c.type AS customer_type
FROM customers AS c
INNER JOIN orders AS o ON o.customer_id = c.id;

-- Запрос 2: DISTINCT по названиям изданий, на которые есть заказы
SELECT DISTINCT e.title AS edition_title
FROM editions AS e
INNER JOIN orders AS o ON o.edition_id = e.id;
