-- Step 1: CREATE TABLE with basic structure (no constraints)

CREATE TABLE customers (
  id serial PRIMARY KEY,
  type text,
  name text,
  contact_name text,
  address text,
  phone text,
  fax text
);

CREATE TABLE editions (
  id serial PRIMARY KEY,
  title text,
  volume_sheets int,
  print_run int
);

CREATE TABLE authors (
  id serial PRIMARY KEY,
  full_name text,
  address text,
  phone text,
  info text
);

CREATE TABLE orders (
  id serial PRIMARY KEY,
  customer_id int,
  product_type text,
  edition_id int,
  typography_name text,
  typography_addr text,
  typography_tel text,
  date_received date,
  date_completed date,
  is_completed boolean
);

CREATE TABLE edition_authors (
  id serial PRIMARY KEY,
  edition_id int,
  author_id int
);
