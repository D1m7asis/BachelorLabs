BEGIN;

-- 1. Create table to store unique typography details
CREATE TABLE IF NOT EXISTS typographies (
  id serial PRIMARY KEY,
  name text NOT NULL,
  addr text,
  tel text,
  CONSTRAINT uq_typography UNIQUE(name, addr, tel)
);

-- 2. Add reference column to orders
ALTER TABLE orders
  ADD COLUMN IF NOT EXISTS typography_id int;

-- 3. Seed typographies from existing orders data
INSERT INTO typographies(name, addr, tel)
SELECT DISTINCT typography_name, typography_addr, typography_tel
FROM orders
WHERE typography_name IS NOT NULL
  OR typography_addr IS NOT NULL
  OR typography_tel IS NOT NULL
ON CONFLICT DO NOTHING;

-- 4. Link orders to typographies
UPDATE orders o
SET typography_id = t.id
FROM typographies t
WHERE o.typography_name = t.name
  AND o.typography_addr = t.addr
  AND o.typography_tel = t.tel
  AND o.typography_id IS NULL;

-- 5. Enforce foreign key once data is aligned (guard if rerun)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'fk_orders_typography'
  ) THEN
    ALTER TABLE orders
      ADD CONSTRAINT fk_orders_typography FOREIGN KEY(typography_id)
        REFERENCES typographies(id);
  END IF;
END;
$$;

-- 6. Drop duplicated typography columns from orders if they still exist
ALTER TABLE orders
  DROP COLUMN IF EXISTS typography_name,
  DROP COLUMN IF EXISTS typography_addr,
  DROP COLUMN IF EXISTS typography_tel;

COMMIT;
