-- Step 6: DELETE constraint tests

-- Prepare linked data
INSERT INTO authors(full_name,address,phone) VALUES('Delete Test','Addr','111');
INSERT INTO editions(title,volume_sheets,print_run) VALUES('Del Edition',5,100);
INSERT INTO edition_authors(edition_id,author_id) VALUES(2,2);

-- 1. Test CASCADE: deleting edition removes edition_authors row
DELETE FROM editions WHERE id=2;

-- 2. Test CASCADE: deleting author removes edition_authors row
DELETE FROM authors WHERE id=2;

-- 3. Test DELETE on orders (customer cascade)
INSERT INTO customers(type,name,phone) VALUES('person','DelTest','222');
INSERT INTO editions(title,volume_sheets,print_run) VALUES('DelTestEd',10,200);
INSERT INTO orders(customer_id,edition_id,product_type,date_received,date_completed)
VALUES(3,3,'Book','2025-01-01','2025-01-02');

DELETE FROM customers WHERE id=3;  -- should delete order
