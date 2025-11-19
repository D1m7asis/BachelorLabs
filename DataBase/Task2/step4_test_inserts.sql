-- Step 4: INSERT tests

-- OK
INSERT INTO customers(type,name,phone) VALUES('person','Иванов Иван','+79995553322');

-- FAIL UNIQUE phone
INSERT INTO customers(type,name,phone) VALUES('person','Петров Петр','+79995553322');

-- FAIL CHECK type
INSERT INTO customers(type,name,phone) VALUES('invalid','Test','123');

-- OK edition
INSERT INTO editions(title,volume_sheets,print_run) VALUES('Учебник',10,500);

-- FAIL CHECK volume_sheets
INSERT INTO editions(title,volume_sheets,print_run) VALUES('Журнал',0,200);

-- OK author
INSERT INTO authors(full_name,address,phone) VALUES('Иванов И.И.','Адрес','12345');

-- FAIL CHECK phone
INSERT INTO authors(full_name,address,phone) VALUES('Test','Addr','bad_phone');

-- OK order
INSERT INTO orders(customer_id, edition_id, product_type, date_received, date_completed)
VALUES(1,1,'Книга','2025-01-01','2025-01-05');

-- FAIL CHECK date_completed < date_received
INSERT INTO orders(customer_id, edition_id, product_type, date_received, date_completed)
VALUES(1,1,'Книга','2025-01-05','2025-01-01');
