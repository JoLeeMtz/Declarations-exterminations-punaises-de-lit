-- SQLite
create table declarations_punaises_lit (
  id integer primary key AUTOINCREMENT,
  NO_DECLARATION integer,
  DATE_DECLARATION DATETIME,
  DATE_INSP_VISPRE DATE,
  NBR_EXTERMIN NUMERIC,
  DATE_DEBUTTRAIT DATE,
  DATE_FINTRAIT DATE,
  No_QR TEXT,
  NOM_QR TEXT,
  NOM_ARROND TEXT,
  COORD_X FLOAT,
  COORD_Y FLOAT,
  LONGITUDE FLOAT,
  LATITUDE FLOAT
);