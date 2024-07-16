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

-- 시작시간변환

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO postgres;

UPDATE ethusdt

ALTER TABLE ethusdt ADD open_time_stamp timestamp;

UPDATE ethusdt
SET open_time_stamp = TO_TIMESTAMP(open_time/1000);


-- 종가시간변환

ALTER TABLE ethsudt ADD close_time_stamp timestamp;

UPDATE ethusdt
SET close_time_stamp = TO_TIMESTAMP(close_time/1000);

ALTER TABLE ethusdt ALTER COLUMN close_time_stamp set not null;
