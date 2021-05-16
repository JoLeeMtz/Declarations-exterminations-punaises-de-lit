-- SQLite
create table users (
  email TEXT primary key,
  name TEXT,
  list_nom_qr TEXT,
  pwd TEXT,
  profile_picture BLOB
);