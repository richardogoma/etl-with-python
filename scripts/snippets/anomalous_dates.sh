#!/usr/bin/env bash

# Inspect the variation of date formats in the dataset
# export projecthome='...Home directory of project workspace ...'

file=$projecthome/data/expenses.csv
cat $file \
	| petl "fromcsv().cut('date').sub('date', r'[0-9]', r'0').distinct() \
		.lookall()" 

# Eyeball the top rows of the anomalous date records
cat $file \
	| petl "fromcsv().cut(*range(0,7)).addrownumbers() \
		.searchcomplement('date', r'^[0-9]{2}\.[0-9]{2}\.[0-9]{4}\.$') \
		.head(2)" 

# Normalizing the date feature using REGEX
cat $file \
        | petl "fromcsv().cut(*range(0,7)).addrownumbers() \
		.sub('date', r'^([0-9]{2})\.([0-9]{2})\.$', r'\1-\2-2018') \
		.sub('date', r'^([0-9]{2})\.([0-9]{2})\.([0-9]{4})\.$', r'\1-\2-\3') \
		.rowslice(104, 106)" 
