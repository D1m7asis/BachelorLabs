-- Запрос 5: авторы с длиной ФИО больше 10 символов
SELECT
    full_name,
    LENGTH(full_name) AS name_length
FROM authors
WHERE LENGTH(full_name) > 10
ORDER BY name_length DESC;

-- Запрос 6: издания, в названии которых встречается слово "литература" (без учёта регистра)
SELECT
    id,
    title,
    UPPER(title) AS upper_title
FROM editions
WHERE UPPER(title) LIKE '%ЛИТЕРАТУРА%';

-- Запрос 7: длительность выполнения заказа (в днях)
SELECT
    id,
    customer_id,
    date_received,
    date_completed,
    EXTRACT(DAY FROM AGE(date_completed, date_received)) AS days_to_complete
FROM orders
WHERE date_completed IS NOT NULL
  AND date_completed > date_received;

-- Запрос 8: последние 4 цифры телефона заказчика
SELECT
    name,
    phone,
    RIGHT(phone, 4) AS last4_digits
FROM customers
WHERE phone IS NOT NULL;
