#!/usr/bin/env bash

# Inspect the first 11 fields/features/columns of a dataset for sparsity
file=$projecthome/data/expenses.csv
headers=$(head -n 1 $file | tr ',' '\n' | head -n 11); \
totalrows=$(cat $file | petl "fromcsv().nrows()"); \
for var in $headers; do \
	nrows=$(cat $file | petl "fromcsv().cut(*range (0,11)).select(lambda rec: rec['$var'] == '').nrows()"); \
	if [ $nrows -ne 0 ]; then \
		prop=$(echo "scale=2; $nrows / $totalrows * 100" | bc); \
		echo "$var field has $nrows missing/empty values; ($prop%) sparse"; \
		echo "----> eyeballing top five rows of the $var field"; \
		cat $file | petl "fromcsv().cut(*range (0,11)).select(lambda rec: rec['$var'] == '').look()"; \
	fi
done
