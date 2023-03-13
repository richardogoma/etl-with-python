#!/usr/bin/env python3
import os
import sys
import petl as etl
import sqlite3
from configparser import ConfigParser
import requests
# from datetime import datetime
import time
import json
from decimal import Decimal

# Declaring global configurations from config file
config = ConfigParser()
if os.path.exists('../main.ini'):
    config.read('../main.ini')
    http_params = config['CONFIG']['params']
    url = config['CONFIG']['url']
    database = config['CONFIG']['database']
    loading_table = config['CONFIG']['loading_table']
    file_desc = config['CONFIG']['flat_file_desc']
else:
    print("Configuration File descriptor `main.ini` does not exist")
    sys.exit()

def ConsumeAPI():
    """
    Consume the data from the API and deserialize JSON
    """
    try:
        response = requests.get(url, params=http_params)
        if response.status_code == 200:
            data = json.loads(response.text)
            for row in data['observations']:
                rates_data = {'date': row['d'], 'rate': row['FXUSDCAD']['v']}
                yield rates_data
    except Exception as e:
        print('Error making HTTP request: '+ str(e))
        sys.exit()

def ETLPipeline(api_data):
    """
    Ingesting data from API and Flat files into the ETL pipeline
    and performing basic transformations
    """
    try: 
        isodate = etl.dateparser('%Y-%m-%d')
        http_resp_tbl = (
            etl
            .fromdicts(api_data, header=['date', 'rate'])
            .convert('date', lambda row: isodate(row))
            .convert('rate', lambda row: Decimal(row))
        )

        flat_file_tbl = (
            etl
            .fromxlsx(file_desc, sheet='Github')
            .convert('date', 'date')
            .convert('USD', lambda row: round(Decimal(row), 2))
        )

        etl_load_table = (
            etl
            .outerjoin(http_resp_tbl, flat_file_tbl, key='date')
            .filldown('rate')
            .select('USD', lambda row: row != None)
            .addfield('CAD', lambda row: row.USD * row.rate)
        )

        print('--------> Printing first 5 rows of normalized table')
        print(etl_load_table.look())

        # etl.tocsv(etl_load_table, 'example.csv')
        
        # # Initialize loading database connection
        # ct = time.time()
        # cnxn = sqlite3.connect(database)
        # cursor = cnxn.cursor()
        # etl.todb(etl_load_table, cnxn, loading_table, create=True)
        # print(f"{etl.nrows(etl_load_table)} rows loaded in {time.time() - ct} secs")
        # cnxn.close()

    except Exception as e:
        print(str(e))
        sys.exit()

def main():
    resp = ConsumeAPI() 
    ETLPipeline(resp)

if __name__ == '__main__':
    main()