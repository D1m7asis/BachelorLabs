-- Запрос 9: издания с объёмом >= 10 листов, отсортированные по тиражу
SELECT
    id,
    title,
    print_run
FROM editions
WHERE volume_sheets >= 10
ORDER BY print_run DESC;

-- Запрос 10: последние 5 заказов по дате приёма (LIMIT обязателен)
SELECT
    id,
    customer_id,
    product_type,
    date_received
FROM orders
WHERE date_received IS NOT NULL
ORDER BY date_received DESC
LIMIT 5;
