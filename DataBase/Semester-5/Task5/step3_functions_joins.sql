-- Запрос 5: длина названия издания и число авторов (LEFT JOIN + LENGTH + агрегат)
SELECT
    e.id                       AS edition_id,
    e.title                    AS edition_title,
    LENGTH(e.title)            AS title_length,
    COUNT(DISTINCT a.id)       AS authors_count
FROM editions AS e
LEFT JOIN edition_authors AS ea ON ea.edition_id = e.id
LEFT JOIN authors         AS a  ON a.id = ea.author_id
WHERE e.volume_sheets > 0
GROUP BY e.id, e.title
ORDER BY authors_count DESC, title_length DESC;

-- Запрос 6: последние 4 цифры телефона заказчика и количество его заказов (RIGHT + COUNT)
SELECT
    c.name                AS customer_name,
    c.phone               AS customer_phone,
    RIGHT(c.phone, 4)     AS last4_digits,
    COUNT(o.id)           AS orders_count
FROM customers AS c
INNER JOIN orders AS o ON o.customer_id = c.id
WHERE c.phone IS NOT NULL
GROUP BY c.name, c.phone
ORDER BY orders_count DESC;

-- Запрос 7: длительность выполнения заказа в днях (EXTRACT + AGE)
SELECT
    o.id                                        AS order_id,
    c.name                                      AS customer_name,
    e.title                                     AS edition_title,
    o.date_received,
    o.date_completed,
    EXTRACT(DAY FROM AGE(o.date_completed, o.date_received)) AS days_to_complete
FROM orders   AS o
INNER JOIN customers AS c ON c.id = o.customer_id
INNER JOIN editions  AS e ON e.id = o.edition_id
WHERE o.date_completed IS NOT NULL
  AND o.date_completed > o.date_received;
