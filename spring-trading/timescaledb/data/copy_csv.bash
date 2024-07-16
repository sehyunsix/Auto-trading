#!/bin/bash
SYMBOL=$1

timescaledb-parallel-copy \
  --connection "host=localhost user=root password=password port=5432" \
  --db-name postgres \
  --table  ethusdt \
  --file ${SYMBOL}-total.csv \
  --workers 4 \
  --copy-options "CSV"
