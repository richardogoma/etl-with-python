#!/usr/bin/env python3
import os
import sys
import petl as etl
import requests
from configparser import ConfigParser
from functools import partial
from geopy.geocoders import Nominatim
from countryinfo import CountryInfo
from decimal import Decimal

# Declaring global configurations from config file
config = ConfigParser()
if os.path.exists('../config.ini'):
    config.read('../config.ini')
    source_descriptor = config['CONFIG']['source_file_desc']
    dest_descriptor = config['CONFIG']['dest_file_desc']
    client_app_name = config['CONFIG']['app_name']
    api_key = config['SECRET']['rapid_api_key']
else:
    print("Configuration File descriptor `config.ini` does not exist")
    sys.exit()

def get_country(val, row):
    geolocator = Nominatim(user_agent=client_app_name)
    geocode = partial(geolocator.geocode, language="en")
    location = geocode(row.city)
    return str(location).split(', ')[-1].lower()

def get_currency(val, row):
    country = CountryInfo(row.country)
    return country.currencies()[0].upper()

def convert_currency(val, row, base_cur, dest_cur, amount):
    url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"
    querystring = {"from":base_cur,"to":dest_cur,"amount":amount,"date":row.date}
    headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com"
             }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        api_response = response.json()
        return api_response['result']

def transform_data():
    try: 
        isodate = etl.dateparser('%Y-%m-%d')
        table = (
            etl
            .fromcsv(source_descriptor).cut(*range(0,11))    # Piping only features of interest

            # Deduplicating rows
            .distinct()

            # Expunging worthless records
            .select(lambda row: not (row.eur == '' and row.hrk == '' and row.lcy == ''))
            
            # Normalizing the date feature using REGEX
            .sub('date', r"^([0-9]{2})\.([0-9]{2})\.$", r"2018-\2-\1")
            .sub('date', r"^([0-9]{2})\.([0-9]{2})\.([0-9]{4})\.$", r"\3-\2-1")
            .convert('date', isodate)

            # Inserting missing country values via geocoding
            .sub('city', r'^(warszaw)$', r'warsaw')
            .convert('country', get_country,
                     where=lambda row: row.country == '', pass_row=True)
            .sub('country', r'^(czech|czechia)$', r'czech republic')

            # Inserting missing currency values via countryinfo API
            .convert('currency', get_currency, 
                     where=lambda row: row.currency == '', pass_row=True)

            # Converting from local (lcy) currency to Croatian Kuna (HRK) for missing (hrk) values
            .convert('hrk', 
                     lambda v, row: convert_currency(v, row, row.currency, 'HRK', row.lcy),
                     where=lambda row: row.hrk == '', pass_row=True)

            # Converting from the Croatian Kuna (HRK) to EUR for missing (eur) values
            .convert('eur', 
                     lambda v, row: convert_currency(v, row, 'HRK', 'EUR', row.hrk),
                     where=lambda row: row.eur == '', pass_row=True)

            # Dropping the lcy feature due to its sparsity
            .cutout('lcy')

            # Normalizing the data type of all rates features
            .convert(('hrk', 'eur'), lambda v: round(Decimal(v), 2))
        )
        return table
    except Exception as e:
        print(str(e))
        sys.exit()

def load_data(table):
    print("Loading transformed data to CSV ....")
    table.progress(50).tocsv(dest_descriptor, 'UTF-8')

def main():
    load_data(table=transform_data())

if __name__ == '__main__':
    main()
