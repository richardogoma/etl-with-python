# Mini project demonstrating ETL with Python and `petl`

This is a secondary project or study of Mislav Vuletić's daily-expense-manager project with a focus on the processing of the dataset in the primary project.

> The goal of Mislav's case study was to process daily expenses with machine learning algorithms to understand and predict an individual's spending behaviour. 

```bash
git clone https://github.com/MasterMedo/daily-expense-manager.git
```

The dataset used for the study needed **pre-processing and enrichment** with data from secondary sources; this was done on the same program as the analysis or investigation.

It might be sufficient to persist ETL and Analysis workloads on the same program when conducting a personal study, especially with small datasets. But in a business environment, transformational or ETL workloads shouldn't be siloed in multiple Jupyter notebooks littered everywhere across the organization. 
> It is a data management best practice to manage ETL workloads centrally and in a unified fashion, especially for mission critical datasets. Data analysts/scientists can have access to high quality data reliably if an ETL data pipeline is developed and managed by ETL/Data engineers.

## Project requirements
This is a python project and it is portable. 
```bash
python3 -m venv .venv
source .venv/bin/activate
which pip
pip install -r requirements.txt
```
This project utilizes the `petl` package on PyPi.
> `petl` transformation pipelines make minimal use of system memory and can scale to millions of rows if speed is not a priority. This package makes extensive use of lazy evaluation and iterators. This means, generally, that a pipeline will not actually be executed until data is requested.

## Source data features
The period of data collection is year 2018. 
1. hrk - croatian kuna, amount of money spent in the currency of Croatia, <br>
2. vendor - company that I bought an item/service from,  <br>
3. date - DD.MM.YYYY. or DD.MM.,  <br>
4. description - specifically what I spent money on (ice-skating, food, bus, alcohol...),  <br>
5. meansofpayment - cash/credit-card/paypal,  <br>
6. city - lowercase name of the city,  <br>
7. category - more general than description e.g. (bus, train, tram) -> transport,  <br>
8. currency - three letter code of the currency e.g. HRK, EUR, PLN...,  <br>
9. country - lowercase name of the country (shortened name if possible e.g. czechia),  <br>
10. lcy - local currency, amount of money spent in the local currency of current transaction,  <br>
11. eur - euro, amount of money spent in euros,  <br>
12. tags - something that will remind me of the record,  <br>
13. recurrence - is the expense likely to be repeated (yes/no)

## Data Source Quality Issues
The data source is `file=../data/expenses.csv`, please refer to `../scripts/datainspector.sh`

### Noisy flat-file features
We have unnamed headers with white spaces delimited by comma in csv file
image.png

### Incomplete/Missing records
Over 55% of records in the data source have missing values in features of importance
image.png

Refer to `cat ../data/empties.csv`

### Inconsistent date formats
The format of dates in the date field has to be homogeneous, but the data set has either `dd.mm.` or `dd.mm.yyyy.` formats.
image.png

Refer to `cat ../data/anomalousdates.csv`

### Duplicate records
image.png

### Data Sparsity
image.png

While the `currency` feature appears to have an approx. 1:2 scarcity ratio, we can source this data from secondary sources (geolocation APIs) using the `city` and `country` features.

The study used euros (EUR) and Croatian Kuna (ISO: HRK) as the currencies of focus. The missing `hrk` values would be derived from the `lcy` (or local currency) field, and the missing values in the `eur` field would derived via forex APIs using the `hrk` field. 

**Could the `hrk`, `lcy` and `eur` fields be missing simultaneously?**

image.png

We don't have such instances in the dataset, but if we have cases where `hrk`, `lcy` and `eur` features are missing _simultaneously_, they would be expunged, as such records present no value to the analysis. 

It is expected that the `lcy` would be the only sparse field, and would be discarded at the tail end of the transformational pipeline. 

## Program Output
image.png