Table customers
{
  id            serial [pk]
  type          text          // частное лицо / организация
  name          text          // ФИО или название организации
  contact_name  text          // контактная персона
  address       text
  phone         text
  fax           text
}

Table orders {
  id              serial [pk]
  customer_id     int         // заказчик
  product_type    text        // вид печатной продукции
  edition_id      int         // связанное издание
  typography_name text
  typography_addr text
  typography_tel  text
  date_received   date
  date_completed  date
  is_completed    boolean
}

Table editions {
  id             serial [pk]   // код издания
  title          text
  volume_sheets  int           // объем в печатных листах
  print_run      int           // тираж
}

Table authors {
  id       serial [pk]
  full_name text
  address   text
  phone     text
  info      text               // дополнительные сведения
}

Table edition_authors {
  id          serial [pk]
  edition_id  int
  author_id   int
}
