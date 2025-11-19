-- INSERT SELECT 1: копирование заказчиков, у которых есть заказы
INSERT INTO customers (type, name, contact_name, address, phone, fax)
SELECT c.type, c.name, c.contact_name, c.address, c.phone || '_copy', c.fax
FROM customers c
JOIN orders o ON o.customer_id = c.id;

-- INSERT SELECT 2: заказ по изданиям с несколькими авторами
INSERT INTO orders (customer_id, edition_id, product_type, date_received, date_completed, is_completed)
SELECT 1 AS customer_id, e.id, 'Автоматический заказ', CURRENT_DATE, CURRENT_DATE + 5, FALSE
FROM editions e
JOIN edition_authors ea ON ea.edition_id = e.id
GROUP BY e.id
HAVING COUNT(ea.author_id) > 1;

-- INSERT SELECT 3: авторы, чьи издания заказывали
INSERT INTO authors (full_name, address, phone, info)
SELECT a.full_name || ' (копия)', a.address, a.phone || '9', 'Автор с заказами'
FROM authors a
JOIN edition_authors ea ON ea.author_id = a.id
JOIN orders o ON o.edition_id = ea.edition_id;

-- INSERT SELECT 4: копирование изданий, на которые есть заказы
INSERT INTO editions (title, volume_sheets, print_run)
SELECT e.title || ' (копия)', e.volume_sheets, e.print_run
FROM editions e
JOIN orders o ON o.edition_id = e.id;

-- INSERT SELECT 5: связка авторов с копиями изданий
INSERT INTO edition_authors (edition_id, author_id)
SELECT e_new.id, ea.author_id
FROM editions e
JOIN editions e_new ON e_new.title = e.title || ' (копия)'
JOIN edition_authors ea ON ea.edition_id = e.id;
