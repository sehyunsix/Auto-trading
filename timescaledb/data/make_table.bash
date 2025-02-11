#!/bin/bash

SYMBOL=$1
SYMBOL=${SYMBOL^^}
set -e




echo "make table now...."

psql -c  "
CREATE TABLE ${SYMBOL}(

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

);"

echo "grand permition user now...."


psql -c "GRANT INSERT, UPDATE, DELETE, SELECT ON ${SYMBOL} TO sehyun;"

echo "copy csv now......."

timescaledb-parallel-copy \
  --connection "host=localhost user=root password=password port=5432" \
  --db-name root \
  --table  ${SYMBOL,,} \
  --file ${SYMBOL}-total.csv \
  --workers 4 \
  --copy-options "CSV"

echo "open_time column edited now......."


psql -c "ALTER TABLE ${SYMBOL} ADD open_time_stamp timestamp;

UPDATE ${SYMBOL}
SET open_time_stamp = TO_TIMESTAMP(open_time/1000);

ALTER TABLE ${SYMBOL} ALTER COLUMN open_time_stamp set not null;
ALTER TABLE ${SYMBOL} DROP COLUMN open_time;
ALTER TABLE ${SYMBOL} RENAME COLUMN open_time_stamp TO open_time;"


#종가시간변환

echo "close_time column edited now......."


psql -c "ALTER TABLE ${SYMBOL} ADD close_time_stamp timestamp;

UPDATE ${SYMBOL}
SET close_time_stamp = TO_TIMESTAMP(close_time/1000);

ALTER TABLE ${SYMBOL} ALTER COLUMN close_time_stamp set not null;
ALTER TABLE ${SYMBOL} DROP COLUMN close_time;
ALTER TABLE ${SYMBOL} RENAME COLUMN close_time_stamp TO close_time;"
