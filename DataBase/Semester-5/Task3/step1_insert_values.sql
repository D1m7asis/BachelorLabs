-- INSERT 1: добавление новых заказчиков
INSERT INTO customers (type, name, contact_name, address, phone, fax)
VALUES
('person', 'Алексеев Петр', 'Алексеев Петр', 'Калининград, ул. Южная 14', '+79991112233', NULL),
('organization', 'ООО "ИздательПлюс"', 'Егорова Л.В.', 'Калининград, ул. Балтийская 9', '+74012345678', '+74012345679');

-- INSERT 2: добавление авторов
INSERT INTO authors (full_name, address, phone, info)
VALUES
('Сидоров И.А.', 'Советск, ул. Набережная 5', '+79995550101', 'Автор учебной литературы'),
('Маркова Е.В.', 'Гурьевск, ул. Лесная 8', '+79997773322', 'Специалист по историческим изданиям');

-- INSERT 3: добавление изданий
INSERT INTO editions (title, volume_sheets, print_run)
VALUES
('Русская литература XX века', 15, 3000),
('История Европейских государств', 22, 1500);

-- INSERT 4: добавление заказов
INSERT INTO orders (customer_id, edition_id, product_type, date_received, date_completed, is_completed)
SELECT c.id, e.id, 'Учебник', '2025-01-10', '2025-01-15', TRUE
FROM customers c, editions e
WHERE c.name = 'Алексеев Петр'
  AND e.title = 'Русская литература XX века';

INSERT INTO orders (customer_id, edition_id, product_type, date_received, date_completed, is_completed)
SELECT c.id, e.id, 'Справочник', '2025-01-12', '2025-01-20', TRUE
FROM customers c, editions e
WHERE c.name = 'ООО "ИздательПлюс"'
  AND e.title = 'История Европейских государств';

-- INSERT 5: добавление связей издание-автор
INSERT INTO edition_authors (edition_id, author_id)
SELECT e.id, a.id
FROM editions e, authors a
WHERE e.title = 'Русская литература XX века'
  AND a.full_name = 'Сидоров И.А.';

INSERT INTO edition_authors (edition_id, author_id)
SELECT e.id, a.id
FROM editions e, authors a
WHERE e.title = 'Русская литература XX века'
  AND a.full_name = 'Маркова Е.В.';

INSERT INTO edition_authors (edition_id, author_id)
SELECT e.id, a.id
FROM editions e, authors a
WHERE e.title = 'История Европейских государств'
  AND a.full_name = 'Маркова Е.В.';
