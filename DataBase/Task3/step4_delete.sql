-- DELETE 1: удалить незавершённые старые заказы
DELETE FROM orders
WHERE is_completed = FALSE
  AND date_received < CURRENT_DATE - INTERVAL '30 days';

-- DELETE 5 (ключевая): удалить заказы организаций через USING
DELETE FROM orders o
USING customers c
WHERE o.customer_id = c.id
  AND c.type = 'organization';

-- DELETE 4: удалить связи author-edition для изданий без заказов
DELETE FROM edition_authors ea
WHERE NOT EXISTS (
    SELECT 1 FROM orders o
    WHERE o.edition_id = ea.edition_id
);

-- DELETE 2: удалить авторов без изданий
DELETE FROM authors a
WHERE NOT EXISTS (
    SELECT 1
    FROM edition_authors ea
    WHERE ea.author_id = a.id
);

-- DELETE 3: удалить копии изданий
DELETE FROM editions
WHERE title LIKE '%(копия)%';
