# etl-with-python
Mini project demonstrating ETL with Python and petl

A simple example demonstrating an entire ETL process

Multiple Data sources
Destination: SQL Database

Two data sources: 
1. Bank of canada valet API: https://www.bankofcanada.ca/valet/docs
_The Bank of Canada Valet Web Services offers programmatic access to global financial data. By using the Valet API, you can retrieve financial data and information from the Bank of Canada — such as daily exchange rates of the Canadian dollar against the European euro._

Specifically, we'll be working with the "Canadian dollar to US dollar daily exchange rate"; "label": "CAD/USD".

2. An expense report (In an Excel spreadsheet)

Destination:
A local SQL Server database table. Refer to the DDL script for table specification. 


Along with Python, we'll be using PETL package, which is used for handling ETL workloads in a Python environment. 

See documentation @https://petl.readthedocs.io/en/stable/intro.html

`petl` is a general purpose Python package for extracting, transforming and loading tables of data.
This package makes extensive use of lazy evaluation and iterators. This means, generally, that a pipeline will not actually be executed until data is requested.

## Refs
- https://github.com/dsartori/ETLDemo/blob/master/DemoDBDDL.sql
- https://www.youtube.com/watch?v=InLgSUw_ZOE
- https://petl.readthedocs.io/en/stable/index.html
- https://www.bankofcanada.ca/valet/docs
- https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-database
