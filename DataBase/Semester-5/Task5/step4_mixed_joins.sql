-- Запрос 8: RIGHT JOIN + LEFT JOIN — все заказчики и их заказы/издания
SELECT
    c.id      AS customer_id,
    c.name    AS customer_name,
    o.id      AS order_id,
    e.title   AS edition_title
FROM orders AS o
RIGHT JOIN customers AS c ON o.customer_id = c.id
LEFT  JOIN editions  AS e ON e.id = o.edition_id
ORDER BY c.name, o.id;

-- Запрос 9: FULL JOIN авторов и их изданий
SELECT
    a.full_name    AS author_name,
    e.title        AS edition_title
FROM authors AS a
FULL JOIN edition_authors AS ea ON ea.author_id = a.id
FULL JOIN editions        AS e  ON e.id = ea.edition_id
ORDER BY author_name, edition_title;

-- Запрос 10: последние 5 заказов с именем клиента и названием издания (JOIN + TO_CHAR + ORDER BY + LIMIT)
SELECT
    o.id                                        AS order_id,
    c.name                                      AS customer_name,
    e.title                                     AS edition_title,
    TO_CHAR(o.date_received, 'YYYY-MM-DD')      AS date_received_fmt
FROM orders   AS o
INNER JOIN customers AS c ON c.id = o.customer_id
INNER JOIN editions  AS e ON e.id = o.edition_id
WHERE o.date_received IS NOT NULL
ORDER BY o.date_received DESC
LIMIT 5;
