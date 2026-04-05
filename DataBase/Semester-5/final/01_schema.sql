CREATE SCHEMA IF NOT EXISTS publishing;
SET search_path TO publishing, public;

CREATE TABLE IF NOT EXISTS customer_types (
  id serial PRIMARY KEY,
  code text NOT NULL UNIQUE,
  title text NOT NULL
);

CREATE TABLE IF NOT EXISTS product_types (
  id serial PRIMARY KEY,
  code text NOT NULL UNIQUE,
  title text NOT NULL
);

CREATE TABLE IF NOT EXISTS customers (
  id serial PRIMARY KEY,
  customer_type_id int NOT NULL,
  name text NOT NULL,
  contact_name text,
  address text NOT NULL,
  phone text NOT NULL,
  fax text
);

CREATE TABLE IF NOT EXISTS typographies (
  id serial PRIMARY KEY,
  name text NOT NULL,
  address text NOT NULL,
  phone text NOT NULL
);

CREATE TABLE IF NOT EXISTS editions (
  id serial PRIMARY KEY,
  title text NOT NULL,
  sheet_count int NOT NULL,
  circulation int NOT NULL
);

CREATE TABLE IF NOT EXISTS authors (
  id serial PRIMARY KEY,
  full_name text NOT NULL,
  address text,
  phone text,
  bio text
);

CREATE TABLE IF NOT EXISTS edition_authors (
  edition_id int NOT NULL,
  author_id int NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
  id serial PRIMARY KEY,
  customer_id int NOT NULL,
  product_type_id int NOT NULL,
  edition_id int NOT NULL,
  typography_id int,
  received_at date NOT NULL,
  completed_at date
);
