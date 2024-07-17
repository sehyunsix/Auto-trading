#시작시간변환

SYMBOL=$1

psql -c "ALTER TABLE ${SYMBOL} ADD open_time_stamp timestamp;

UPDATE ${SYMBOL}
SET open_time_stamp = TO_TIMESTAMP(open_time/1000);

ALTER TABLE ${SYMBOL} ALTER COLUMN open_time_stamp set not null;"


#종가시간변환

psql -c "ALTER TABLE ${SYMBOL} ADD close_time_stamp timestamp;

UPDATE ${SYMBOL}
SET close_time_stamp = TO_TIMESTAMP(close_time/1000);

ALTER TABLE ${SYMBOL} ALTER COLUMN close_time_stamp set not null;"
