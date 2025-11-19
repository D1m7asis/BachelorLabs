-- UPDATE 1: изменить адрес у всех организаций
UPDATE customers
SET address = 'Калининград, ул. Центральная 21'
WHERE type = 'organization';

-- UPDATE 2: увеличить volume_sheets на 2 для крупных тиражей
UPDATE editions
SET volume_sheets = volume_sheets + 2
WHERE print_run > 2000;

-- UPDATE 3: отметить заказы завершёнными
UPDATE orders
SET is_completed = TRUE
WHERE date_completed < CURRENT_DATE;

-- UPDATE 4: связь через SELECT (2+ таблицы, исправлено)
UPDATE authors a
SET phone = a.phone || '9'
WHERE a.id IN (
    SELECT ea.author_id
    FROM edition_authors ea
    JOIN orders o ON o.edition_id = ea.edition_id
    JOIN customers c ON c.id = o.customer_id
    WHERE c.type = 'person'
);

-- UPDATE 5: смена product_type для копий изданий
UPDATE orders
SET product_type = 'Копия издания'
WHERE edition_id IN (
    SELECT id FROM editions WHERE title LIKE '%(копия)%'
);
