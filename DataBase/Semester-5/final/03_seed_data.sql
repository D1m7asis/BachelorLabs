SET search_path TO publishing, public;

INSERT INTO customer_types (code, title)
VALUES
  ('person', 'Person'),
  ('organization', 'Organization')
ON CONFLICT (code) DO UPDATE
SET title = EXCLUDED.title;

INSERT INTO product_types (code, title)
VALUES
  ('textbook', 'Textbook'),
  ('reference', 'Reference Book'),
  ('catalog', 'Catalog'),
  ('brochure', 'Brochure'),
  ('auto_order', 'Automatic Order')
ON CONFLICT (code) DO UPDATE
SET title = EXCLUDED.title;

INSERT INTO customers (customer_type_id, name, contact_name, address, phone, fax)
VALUES
  (
    (SELECT id FROM customer_types WHERE code = 'person'),
    'Alexey Petrov',
    'Alexey Petrov',
    'Kaliningrad, Yuzhnaya 14',
    '+79991112233',
    NULL
  ),
  (
    (SELECT id FROM customer_types WHERE code = 'organization'),
    'Publishing Plus LLC',
    'L. Egorova',
    'Kaliningrad, Baltiyskaya 9',
    '+74012345678',
    '+74012345679'
  ),
  (
    (SELECT id FROM customer_types WHERE code = 'organization'),
    'Baltic Education Center',
    'M. Romanova',
    'Kaliningrad, Universitetskaya 3',
    '+74012300011',
    NULL
  ),
  (
    (SELECT id FROM customer_types WHERE code = 'person'),
    'Elena Smirnova',
    'Elena Smirnova',
    'Svetlogorsk, Morskaya 5',
    '+79990007766',
    NULL
  )
ON CONFLICT (phone) DO NOTHING;

INSERT INTO typographies (name, address, phone)
VALUES
  ('Baltic Typography', 'Kaliningrad, Mira 10', '+74012000001'),
  ('Amber Press', 'Kaliningrad, Portovaya 7', '+74012000002'),
  ('University Print House', 'Kaliningrad, Academic 2', '+74012000003')
ON CONFLICT (name) DO UPDATE
SET address = EXCLUDED.address,
    phone = EXCLUDED.phone;

INSERT INTO editions (title, sheet_count, circulation)
VALUES
  ('Russian Literature of the 20th Century', 15, 3000),
  ('History of European States', 22, 1500),
  ('Database Systems Workshop', 12, 2000),
  ('Regional Science Catalog', 8, 1200),
  ('Modern Pedagogy Guide', 18, 2500)
ON CONFLICT (title) DO UPDATE
SET sheet_count = EXCLUDED.sheet_count,
    circulation = EXCLUDED.circulation;

INSERT INTO authors (full_name, address, phone, bio)
VALUES
  ('Igor Sidorov', 'Sovetsk, Naberezhnaya 5', '+79995550101', 'Author of study literature'),
  ('Elena Markova', 'Guryevsk, Lesnaya 8', '+79997773322', 'Specialist in history editions'),
  ('Pavel Orlov', 'Kaliningrad, Chernyakhovskogo 12', '+79994443322', 'Database lecturer and methodologist'),
  ('Marina Volkova', 'Zelenogradsk, Parkovaya 11', '+79993334455', 'Compiler of educational catalogs')
ON CONFLICT (full_name, address) DO NOTHING;

INSERT INTO edition_authors (edition_id, author_id)
VALUES
  (
    (SELECT id FROM editions WHERE title = 'Russian Literature of the 20th Century'),
    (SELECT id FROM authors WHERE full_name = 'Igor Sidorov')
  ),
  (
    (SELECT id FROM editions WHERE title = 'Russian Literature of the 20th Century'),
    (SELECT id FROM authors WHERE full_name = 'Elena Markova')
  ),
  (
    (SELECT id FROM editions WHERE title = 'History of European States'),
    (SELECT id FROM authors WHERE full_name = 'Elena Markova')
  ),
  (
    (SELECT id FROM editions WHERE title = 'Database Systems Workshop'),
    (SELECT id FROM authors WHERE full_name = 'Pavel Orlov')
  ),
  (
    (SELECT id FROM editions WHERE title = 'Regional Science Catalog'),
    (SELECT id FROM authors WHERE full_name = 'Marina Volkova')
  ),
  (
    (SELECT id FROM editions WHERE title = 'Modern Pedagogy Guide'),
    (SELECT id FROM authors WHERE full_name = 'Pavel Orlov')
  ),
  (
    (SELECT id FROM editions WHERE title = 'Modern Pedagogy Guide'),
    (SELECT id FROM authors WHERE full_name = 'Marina Volkova')
  )
ON CONFLICT (edition_id, author_id) DO NOTHING;

INSERT INTO orders (
  customer_id,
  product_type_id,
  edition_id,
  typography_id,
  received_at,
  completed_at
)
VALUES
  (
    (SELECT id FROM customers WHERE phone = '+79991112233'),
    (SELECT id FROM product_types WHERE code = 'textbook'),
    (SELECT id FROM editions WHERE title = 'Russian Literature of the 20th Century'),
    (SELECT id FROM typographies WHERE name = 'Baltic Typography'),
    DATE '2025-01-10',
    DATE '2025-01-15'
  ),
  (
    (SELECT id FROM customers WHERE phone = '+74012345678'),
    (SELECT id FROM product_types WHERE code = 'reference'),
    (SELECT id FROM editions WHERE title = 'History of European States'),
    (SELECT id FROM typographies WHERE name = 'Amber Press'),
    DATE '2025-01-12',
    DATE '2025-01-20'
  ),
  (
    (SELECT id FROM customers WHERE phone = '+74012300011'),
    (SELECT id FROM product_types WHERE code = 'catalog'),
    (SELECT id FROM editions WHERE title = 'Regional Science Catalog'),
    (SELECT id FROM typographies WHERE name = 'University Print House'),
    DATE '2025-02-05',
    DATE '2025-02-09'
  ),
  (
    (SELECT id FROM customers WHERE phone = '+79990007766'),
    (SELECT id FROM product_types WHERE code = 'brochure'),
    (SELECT id FROM editions WHERE title = 'Modern Pedagogy Guide'),
    (SELECT id FROM typographies WHERE name = 'Baltic Typography'),
    DATE '2025-03-01',
    NULL
  ),
  (
    (SELECT id FROM customers WHERE phone = '+79991112233'),
    (SELECT id FROM product_types WHERE code = 'auto_order'),
    (SELECT id FROM editions WHERE title = 'Database Systems Workshop'),
    (SELECT id FROM typographies WHERE name = 'University Print House'),
    DATE '2025-03-15',
    NULL
  ),
  (
    (SELECT id FROM customers WHERE phone = '+74012345678'),
    (SELECT id FROM product_types WHERE code = 'textbook'),
    (SELECT id FROM editions WHERE title = 'Database Systems Workshop'),
    (SELECT id FROM typographies WHERE name = 'Amber Press'),
    DATE '2025-03-20',
    DATE '2025-03-27'
  )
ON CONFLICT DO NOTHING;
