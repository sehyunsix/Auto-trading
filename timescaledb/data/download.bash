#!/bin/bash

SYMBOL=$1
SYMBOL=${SYMBOL^^}

for j in {2020..2023}
  do
    for i in {01..12} # zero-padded days 01, 02, 03, ... 31
    do
        # month of july 2023, day number is the `i` variable
        archiveName="${SYMBOL}-1m-${j}-${i}.zip"
        # download the .zip, extract it (saves .csv), and remove the .zip
        wget "https://data.binance.vision/data/spot/monthly/klines/${SYMBOL}/1m/${archiveName}" && unzip "./${archiveName}" && rm "./${archiveName}"
        cat ${archiveName//zip/csv} | wc -l
    done
  done
cat ${SYMBOL}-1m*.csv > $SYMBOL-total.csv
rm ${SYMBOL}-1*.csv
cat ${SYMBOL}-total.csv | wc -l






