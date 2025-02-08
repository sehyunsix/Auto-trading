-- Table 생성

CREATE TABLE ETHUSDT(

  open_time BIGINT NOT NULL,
  open_price DOUBLE PRECISION NULL,
  high_price DOUBLE PRECISION NULL,
  low_price DOUBLE PRECISION NULL,
  close_price DOUBLE PRECISION NULL,
  volume DOUBLE PRECISION NULL,
  close_time BIGINT NOT NULL,
  quote_volume DOUBLE PRECISION NULL,
  count INT NULL,
  taker_buy_volume DOUBLE PRECISION NULL,
  taker_buy_quote_volume DOUBLE PRECISION NULL,
  ignore TEXT NULL

);


-- 유저생성

CREATE USER sehyun WITH PASSWORD '1234';
GRANT INSERT, UPDATE, DELETE,SELECT ON ethusdt TO sehyun



