#!bin/bash

SYMBOL=$1
psql -c "DROP TABLE ${SYMBOL}"