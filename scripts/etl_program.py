#!/usr/bin/env python3
import os
import sys
import petl as etl
from configparser import ConfigParser
from functools import partial
from geopy.geocoders import Nominatim
from countryinfo import CountryInfo
from forex_python.converter import CurrencyRates
from decimal import Decimal

# Declaring global configurations from config file
config = ConfigParser()
if os.path.exists('../config.ini'):
    config.read('../config.ini')
    source_descriptor = config['CONFIG']['source_file_desc']
    dest_descriptor = config['CONFIG']['dest_file_desc']
    geolocator = Nominatim(user_agent=config['CONFIG']['app_name'])
else:
    print("Configuration File descriptor `config.ini` does not exist")
    sys.exit()

def get_country(val, row):
    geocode = partial(geolocator.geocode, language="en")
    location = geocode(row.city)
    return str(location).split(', ')[-1].lower()

def get_currency(val, row):
    country = CountryInfo(row.country)
    return country.currencies()[0].upper()

def convert_currency(val, row, base_cur, dest_cur, amount, inverse: bool) -> Decimal:
    c = CurrencyRates(force_decimal=True)
    rates = c.get_rates(base_cur, row.date)
    if inverse:
        return round(amount/rates[dest_cur], 2)
    else:
        return round(amount * rates[dest_cur], 2)

def transform_data():
    try: 
        isodate = etl.dateparser('%d-%m-%Y')
        table = (
            etl
            .fromcsv(source_descriptor).cut(*range(0,11))    # Piping only features of interest

            # Deduplicating rows
            .distinct()

            # Expunging worthless records
            .select(lambda rec: rec.eur != '' and rec.hrk != '' and rec.lcy != '')
            
            # Normalizing the date feature using REGEX
            .sub('date', r"([0-9]{2})\.([0-9]{2})\.$", r"\1-\2-2018")
            .sub('date', r"([0-9]{2})\.([0-9]{2})\.([0-9]{4})\.$", r"\1-\2-\3")
            .convert('date', isodate)

            # Inserting missing country values via geocoding
            .sub('city', r'^(warszaw)$', r'warsaw')
            .convert('country', get_country,
                     where=lambda row: row.country == '', pass_row=True)
            .sub('country', r'^(czech|czechia)$', r'czech republic')

            # Inserting missing currency values via countryinfo API
            .convert('currency', get_currency, 
                     where=lambda row: row.currency == '', pass_row=True)

            # Normalizing the data type of all rates features
            .convert(('hrk', 'lcy', 'eur'), lambda v: Decimal(v))

            # Converting from local (lcy) currency to Croatian Kuna (ISO: HRK) for missing (hrk) values
            .convert('hrk', 
                     lambda v, row: convert_currency(v, row, 'HRK', row.currency, row.lcy, True),
                     where=lambda row: row.hrk == None, pass_row=True)

            # Converting from the Croatian Kuna (ISO: HRK) to EUR for missing (eur) values
            .convert('eur', 
                     lambda v, row: convert_currency(v, row, 'HRK', 'EUR', row.hrk, False),
                     where=lambda row: row.eur == None, pass_row=True)

            # Dropping the lcy feature due to its sparsity
            .cutout('lcy')
        )
        return table
    except Exception as e:
        print(str(e))
        sys.exit()

def load_data(table):
    print("Loading transformed data to CSV ....")
    table.progress(10).tocsv(dest_descriptor, 'UTF-8')

def main():
    load_data(table=transform_data())

if __name__ == '__main__':
    main()
