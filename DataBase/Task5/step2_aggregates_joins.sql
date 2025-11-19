-- Запрос 3: количество завершённых заказов по каждому заказчику
SELECT
    c.id            AS customer_id,
    c.name          AS customer_name,
    COUNT(o.id)     AS completed_orders_count
FROM customers AS c
INNER JOIN orders AS o ON o.customer_id = c.id
WHERE o.is_completed = TRUE
GROUP BY c.id, c.name
ORDER BY completed_orders_count DESC;

-- Запрос 4: количество различных изданий по каждому заказчику
SELECT
    c.name                    AS customer_name,
    COUNT(DISTINCT e.id)      AS editions_count
FROM customers AS c
LEFT JOIN orders   AS o ON o.customer_id = c.id
LEFT JOIN editions AS e ON e.id = o.edition_id
GROUP BY c.name
ORDER BY editions_count DESC;
