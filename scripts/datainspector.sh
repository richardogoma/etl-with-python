#!/usr/bin/env bash

# Install python project dependencies
pip install -r requirements.txt

file=../data/expenses.csv
head $file
cat $file | petl "fromcsv().look()"
cat $file | petl "fromcsv().nrows()"
cat $file | wc -l   # Number of raw lines (header inclusive)

# Fields of interest
cat $file | petl "fromcsv().cut(*range(0,11)).header()"

echo "----> Inspecting file for anomalies"
# Eyeballing missing values (first/last 5 rows) in file
cat $file \
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: any(v == '' for v in rec)).head()"
cat $file \
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: any(v == '' for v in rec)).tail()"
cat $file \ 
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: any(v == '' for v in rec)).nrows()"

# Show the fields with missing values (data sparsity)
headers=$(head -n 1 $file | tr ',' '\n' | head -n 11); \
for var in $headers; do \
	nrows=$(cat $file | petl "fromcsv().cut(*range(0,11)).select(lambda rec: rec['$var'] == '').nrows()"); \
	if [ $nrows -ne 0 ]; then \
		echo "$var field has missing/empty values ----> nrows: $nrows"; \
        echo "----> eyeballing top rows of $var field"; \
        cat $file | petl "fromcsv().cut(*range(0,11)).select(lambda rec: rec['$var'] == '').look()"; \
	fi
done

cat $file \
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: any(v == '' for v in rec)).tocsv('../data/empties.csv')"

cat ../data/empties.csv | wc
cat ../data/empties.csv | wc -l


# Inspecting the date field
cat $file \
    | petl "fromcsv().cut(*range(0,11)).search('date', '[0-9]{2}\.[0-9]{2}\.$').lookall()"

cat $file \
    | petl "fromcsv().cut(*range(0,11)).searchcomplement('date', '[0-9]{2}\.[0-9]{2}\.[0-9]{4}\.$').look()"

cat $file \
    | petl "fromcsv().cut(*range(0,11)).searchcomplement('date', '[0-9]{2}\.[0-9]{2}\.[0-9]{4}\.$').tocsv('../data/anomalousdates.csv')"

cat ../data/anomalousdates.csv | wc -l


# Inspecting the currencies field
cat $file \
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: rec.eur == '').look()"

# If `eur` field is missing, we can engineer it from `hrk`
cat $file \
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: (rec.eur == '' and rec.hrk == '')).look()"

# If `hrk` field is missing, we can engineer it from `lcy` and `currency` fields
cat $file \
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: (rec.hrk == '')).look()"

cat $file \
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: (rec.hrk == '' and rec.lcy == '')).look()"

 cat $file \
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: (rec.hrk != '')).rowslice(5, 15)"

cat $file \
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: (rec.eur == '' and rec.lcy == '')).look()"

cat $file \
    | petl "fromcsv().cut(*range(0,11)).select(lambda rec: (rec.eur == '' and rec.hrk == '' and rec.lcy == '')).look()"

# Potential issues
# 1. Both the 'hrk' and `lcy` and `city` fields are missing; although, there are no such instances, but if existent, we'll remove such rows.
# 2. There are many instances of lcy and eur fields being empty simultaneously; so direct conversion is inhibited, whereas, there were values for the hrk. So there has to be a two stage conditional currency conversion. 

# Inspecting the source file for duplicate records
cat $file \
    | petl "fromcsv().cut(*range(0,11)).duplicates().nrows()"

cat $file \
    | petl "fromcsv().cut(*range(0,11)).duplicates().lookall()"

echo "----> Deduplicating rows"
cat $file \
    | petl "fromcsv().cut(*range(0,11)).distinct().nrows()"

# Running the program
chmod +x etl_program.py
./etl_program.py

echo "----> Eyeballing loaded dataset"
# nano ../data/expenses_enriched.csv
# head ../data/expenses_enriched.csv
cat ../data/expenses_enriched.csv | petl "fromcsv().look()"