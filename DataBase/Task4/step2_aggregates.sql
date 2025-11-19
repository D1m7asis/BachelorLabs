-- Запрос 3: количество завершённых заказов по каждому заказчику
SELECT
    c.id,
    c.name,
    COUNT(o.id) AS completed_orders_count
FROM customers c
JOIN orders o ON o.customer_id = c.id
WHERE o.is_completed = TRUE
GROUP BY c.id, c.name
ORDER BY completed_orders_count DESC;

-- Запрос 4: агрегаты по изданиям (средний объём и мин/макс тираж)
SELECT
    AVG(volume_sheets) AS avg_volume_sheets,
    MIN(print_run)     AS min_print_run,
    MAX(print_run)     AS max_print_run
FROM editions
WHERE print_run > 0;
