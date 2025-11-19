-- Step 5: UPDATE constraint tests

-- 1. OK: update customer type correctly
UPDATE customers SET type='organization' WHERE id=1;

-- 2. FAIL CHECK: invalid type
UPDATE customers SET type='invalid_type' WHERE id=1;

-- 3. FAIL UNIQUE: duplicate phone
INSERT INTO customers(type,name,phone) VALUES('person','Temp','+70000000000');
UPDATE customers SET phone='+70000000000' WHERE id=1;

-- 4. OK: update edition volume
UPDATE editions SET volume_sheets=20 WHERE id=1;

-- 5. FAIL CHECK: negative volume_sheets
UPDATE editions SET volume_sheets=-5 WHERE id=1;

-- 6. OK: update order completed date
UPDATE orders SET date_completed='2025-01-10' WHERE id=1;

-- 7. FAIL CHECK: completed earlier than received
UPDATE orders SET date_completed='2024-12-01' WHERE id=1;
