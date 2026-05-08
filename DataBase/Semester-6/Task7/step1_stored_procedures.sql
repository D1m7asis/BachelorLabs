SET search_path TO publishing, public;

DELETE FROM orders
WHERE received_at = DATE '2025-04-01'
  AND customer_id IN (
      SELECT id
      FROM customers
      WHERE phone = '+74012999887'
  );

DELETE FROM customers
WHERE phone IN ('+74012999887', '+79998887766', '+74012224466');

DELETE FROM authors
WHERE full_name = 'Sergey Belov'
  AND address = 'Kaliningrad, Gorkogo 18';

DELETE FROM typographies
WHERE name = 'City Print Studio';

DROP PROCEDURE IF EXISTS get_customer_by_id(int, refcursor);
DROP PROCEDURE IF EXISTS find_customers_by_name_part(text, refcursor);
DROP PROCEDURE IF EXISTS get_edition_by_id(int, refcursor);
DROP PROCEDURE IF EXISTS find_editions_by_title_part(text, refcursor);
DROP PROCEDURE IF EXISTS add_customer_with_validation(text, text, text, text, text, text);
DROP PROCEDURE IF EXISTS add_typography_with_validation(text, text, text);
DROP PROCEDURE IF EXISTS add_author_with_validation(text, text, text, text);
DROP PROCEDURE IF EXISTS create_order_with_validation(int, text, int, int, date, date);
DROP PROCEDURE IF EXISTS update_customer_address(int, text);
DROP PROCEDURE IF EXISTS update_edition_circulation(int, int);
DROP PROCEDURE IF EXISTS complete_order_by_id(int, date);
DROP PROCEDURE IF EXISTS complete_orders_for_typography(int, date);

-- 1. Search one customer by identifier.
CREATE OR REPLACE PROCEDURE get_customer_by_id(
    IN p_customer_id int,
    INOUT p_result refcursor
)
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN p_result FOR
        SELECT
            c.id,
            c.name,
            ct.title AS customer_type,
            c.contact_name,
            c.address,
            c.phone,
            c.fax
        FROM customers c
        JOIN customer_types ct ON ct.id = c.customer_type_id
        WHERE c.id = p_customer_id;
END;
$$;

-- 2. Search customers by part of name.
CREATE OR REPLACE PROCEDURE find_customers_by_name_part(
    IN p_name_part text,
    INOUT p_result refcursor
)
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN p_result FOR
        SELECT
            c.id,
            c.name,
            ct.title AS customer_type,
            c.phone
        FROM customers c
        JOIN customer_types ct ON ct.id = c.customer_type_id
        WHERE c.name ILIKE '%' || p_name_part || '%'
        ORDER BY c.name;
END;
$$;

-- 3. Search one edition by identifier.
CREATE OR REPLACE PROCEDURE get_edition_by_id(
    IN p_edition_id int,
    INOUT p_result refcursor
)
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN p_result FOR
        SELECT
            e.id,
            e.title,
            e.sheet_count,
            e.circulation
        FROM editions e
        WHERE e.id = p_edition_id;
END;
$$;

-- 4. Search editions by part of title.
CREATE OR REPLACE PROCEDURE find_editions_by_title_part(
    IN p_title_part text,
    INOUT p_result refcursor
)
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN p_result FOR
        SELECT
            e.id,
            e.title,
            e.sheet_count,
            e.circulation
        FROM editions e
        WHERE e.title ILIKE '%' || p_title_part || '%'
        ORDER BY e.title;
END;
$$;

-- 5. Add a customer with validation.
CREATE OR REPLACE PROCEDURE add_customer_with_validation(
    IN p_customer_type_code text,
    IN p_name text,
    IN p_contact_name text,
    IN p_address text,
    IN p_phone text,
    IN p_fax text DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_customer_type_id int;
BEGIN
    SELECT id
    INTO v_customer_type_id
    FROM customer_types
    WHERE code = p_customer_type_code;

    IF v_customer_type_id IS NULL THEN
        RAISE EXCEPTION 'Unknown customer type code: %', p_customer_type_code;
    END IF;

    IF EXISTS (SELECT 1 FROM customers WHERE phone = p_phone) THEN
        RAISE EXCEPTION 'Customer with phone % already exists', p_phone;
    END IF;

    INSERT INTO customers (
        customer_type_id,
        name,
        contact_name,
        address,
        phone,
        fax
    )
    VALUES (
        v_customer_type_id,
        p_name,
        p_contact_name,
        p_address,
        p_phone,
        p_fax
    );

    RAISE NOTICE 'Customer % added', p_name;
END;
$$;

-- 6. Add a typography with validation.
CREATE OR REPLACE PROCEDURE add_typography_with_validation(
    IN p_name text,
    IN p_address text,
    IN p_phone text
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM typographies WHERE name = p_name) THEN
        RAISE EXCEPTION 'Typography with name % already exists', p_name;
    END IF;

    INSERT INTO typographies (name, address, phone)
    VALUES (p_name, p_address, p_phone);

    RAISE NOTICE 'Typography % added', p_name;
END;
$$;

-- 7. Add an author with validation.
CREATE OR REPLACE PROCEDURE add_author_with_validation(
    IN p_full_name text,
    IN p_address text,
    IN p_phone text,
    IN p_bio text DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM authors
        WHERE full_name = p_full_name
          AND address IS NOT DISTINCT FROM p_address
    ) THEN
        RAISE EXCEPTION 'Author % already exists for the same address', p_full_name;
    END IF;

    INSERT INTO authors (full_name, address, phone, bio)
    VALUES (p_full_name, p_address, p_phone, p_bio);

    RAISE NOTICE 'Author % added', p_full_name;
END;
$$;

-- 8. Add an order with validation.
CREATE OR REPLACE PROCEDURE create_order_with_validation(
    IN p_customer_id int,
    IN p_product_type_code text,
    IN p_edition_id int,
    IN p_typography_id int,
    IN p_received_at date,
    IN p_completed_at date DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_product_type_id int;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM customers WHERE id = p_customer_id) THEN
        RAISE EXCEPTION 'Customer with id % was not found', p_customer_id;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM editions WHERE id = p_edition_id) THEN
        RAISE EXCEPTION 'Edition with id % was not found', p_edition_id;
    END IF;

    IF p_typography_id IS NOT NULL
       AND NOT EXISTS (SELECT 1 FROM typographies WHERE id = p_typography_id) THEN
        RAISE EXCEPTION 'Typography with id % was not found', p_typography_id;
    END IF;

    SELECT id
    INTO v_product_type_id
    FROM product_types
    WHERE code = p_product_type_code;

    IF v_product_type_id IS NULL THEN
        RAISE EXCEPTION 'Unknown product type code: %', p_product_type_code;
    END IF;

    IF p_completed_at IS NOT NULL AND p_completed_at < p_received_at THEN
        RAISE EXCEPTION 'Completion date cannot be earlier than received date';
    END IF;

    INSERT INTO orders (
        customer_id,
        product_type_id,
        edition_id,
        typography_id,
        received_at,
        completed_at
    )
    VALUES (
        p_customer_id,
        v_product_type_id,
        p_edition_id,
        p_typography_id,
        p_received_at,
        p_completed_at
    );

    RAISE NOTICE 'Order for customer % created', p_customer_id;
END;
$$;

-- 9. Update one field in customer card.
CREATE OR REPLACE PROCEDURE update_customer_address(
    IN p_customer_id int,
    IN p_new_address text
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE customers
    SET address = p_new_address
    WHERE id = p_customer_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Customer with id % was not found', p_customer_id;
    END IF;

    RAISE NOTICE 'Address updated for customer %', p_customer_id;
END;
$$;

-- 10. Update one field in edition card.
CREATE OR REPLACE PROCEDURE update_edition_circulation(
    IN p_edition_id int,
    IN p_new_circulation int
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_new_circulation <= 0 THEN
        RAISE EXCEPTION 'Circulation must be greater than zero';
    END IF;

    UPDATE editions
    SET circulation = p_new_circulation
    WHERE id = p_edition_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Edition with id % was not found', p_edition_id;
    END IF;

    RAISE NOTICE 'Circulation updated for edition %', p_edition_id;
END;
$$;

-- 11. Complete one order by identifier.
CREATE OR REPLACE PROCEDURE complete_order_by_id(
    IN p_order_id int,
    IN p_completed_at date
)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE orders
    SET completed_at = p_completed_at
    WHERE id = p_order_id
      AND p_completed_at >= received_at;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Order % was not found or completion date is invalid', p_order_id;
    END IF;

    RAISE NOTICE 'Order % completed', p_order_id;
END;
$$;

-- 12. Complete all open orders for one typography.
CREATE OR REPLACE PROCEDURE complete_orders_for_typography(
    IN p_typography_id int,
    IN p_completed_at date
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_updated_count int;
BEGIN
    UPDATE orders
    SET completed_at = p_completed_at
    WHERE typography_id = p_typography_id
      AND completed_at IS NULL
      AND received_at <= p_completed_at;

    GET DIAGNOSTICS v_updated_count = ROW_COUNT;

    RAISE NOTICE 'Orders completed for typography %: %', p_typography_id, v_updated_count;
END;
$$;

-- Demo calls.

-- 1. Customer by id.
BEGIN;
CALL get_customer_by_id(1, 'cur_customer_by_id');
FETCH ALL FROM cur_customer_by_id;
COMMIT;

-- 2. Customers by part of name.
BEGIN;
CALL find_customers_by_name_part('Alex', 'cur_customers_by_name');
FETCH ALL FROM cur_customers_by_name;
COMMIT;

-- 3. Edition by id.
BEGIN;
CALL get_edition_by_id(3, 'cur_edition_by_id');
FETCH ALL FROM cur_edition_by_id;
COMMIT;

-- 4. Editions by part of title.
BEGIN;
CALL find_editions_by_title_part('Guide', 'cur_editions_by_title');
FETCH ALL FROM cur_editions_by_title;
COMMIT;

-- 5. Add customer.
CALL add_customer_with_validation(
    'organization',
    'West Coast Printing Club',
    'I. Sergeeva',
    'Baltiysk, Naberezhnaya 19',
    '+74012999887',
    NULL
);

SELECT id, name, phone
FROM customers
WHERE phone = '+74012999887';

-- 6. Add typography.
CALL add_typography_with_validation(
    'City Print Studio',
    'Kaliningrad, Sovetskaya 44',
    '+74012224466'
);

SELECT id, name, phone
FROM typographies
WHERE name = 'City Print Studio';

-- 7. Add author.
CALL add_author_with_validation(
    'Sergey Belov',
    'Kaliningrad, Gorkogo 18',
    '+79995557788',
    'Author of educational publications'
);

SELECT id, full_name, phone
FROM authors
WHERE full_name = 'Sergey Belov';

-- 8. Add order.
DO $$
DECLARE
    v_customer_id int;
    v_edition_id int;
    v_typography_id int;
BEGIN
    SELECT id INTO v_customer_id
    FROM customers
    WHERE phone = '+74012999887';

    SELECT id INTO v_edition_id
    FROM editions
    WHERE title = 'Modern Pedagogy Guide';

    SELECT id INTO v_typography_id
    FROM typographies
    WHERE name = 'City Print Studio';

    CALL create_order_with_validation(
        v_customer_id,
        'brochure',
        v_edition_id,
        v_typography_id,
        DATE '2025-04-01',
        NULL
    );
END;
$$;

SELECT
    o.id,
    c.name AS customer_name,
    o.received_at,
    o.completed_at
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE c.phone = '+74012999887'
ORDER BY o.id DESC
LIMIT 1;

-- 9. Update customer address.
DO $$
DECLARE
    v_customer_id int;
BEGIN
    SELECT id INTO v_customer_id
    FROM customers
    WHERE phone = '+74012999887';

    CALL update_customer_address(
        v_customer_id,
        'Baltiysk, Portovaya 21'
    );
END;
$$;

SELECT id, name, address
FROM customers
WHERE phone = '+74012999887';

-- 10. Update edition circulation.
DO $$
DECLARE
    v_edition_id int;
BEGIN
    SELECT id INTO v_edition_id
    FROM editions
    WHERE title = 'Regional Science Catalog';

    CALL update_edition_circulation(
        v_edition_id,
        1400
    );
END;
$$;

SELECT id, title, circulation
FROM editions
WHERE title = 'Regional Science Catalog';

-- 11. Complete one order.
DO $$
DECLARE
    v_order_id int;
BEGIN
    SELECT o.id INTO v_order_id
    FROM orders o
    JOIN customers c ON c.id = o.customer_id
    WHERE c.phone = '+74012999887'
      AND o.received_at = DATE '2025-04-01';

    CALL complete_order_by_id(v_order_id, DATE '2025-04-05');
END;
$$;

SELECT
    o.id,
    o.received_at,
    o.completed_at
FROM orders o
JOIN customers c ON c.id = o.customer_id
WHERE c.phone = '+74012999887'
  AND o.received_at = DATE '2025-04-01';

-- 12. Complete all open orders for one typography.
DO $$
DECLARE
    v_typography_id int;
BEGIN
    SELECT id INTO v_typography_id
    FROM typographies
    WHERE name = 'Baltic Typography';

    CALL complete_orders_for_typography(
        v_typography_id,
        DATE '2025-04-10'
    );
END;
$$;

SELECT
    o.id,
    t.name AS typography_name,
    o.received_at,
    o.completed_at
FROM orders o
JOIN typographies t ON t.id = o.typography_id
WHERE t.name = 'Baltic Typography'
ORDER BY o.id;
