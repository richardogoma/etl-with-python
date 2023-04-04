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

# Declaring global variables from config file
try:
    config_file = "config.ini"
    if not os.path.exists(config_file):
        raise IOError(f"Configuration file {config_file} does not exist")
    else:
        config = ConfigParser()
        config.read(config_file)
        source_descriptor = config["FILE"]["source_file_desc"]
        dest_descriptor = config["FILE"]["dest_file_desc"]
        client_app_name = config["CONFIG"]["app_name"]
except IOError as e:
    print("Error: " + str(e))
    sys.exit()

# Retrieving api key from environment variable
try:
    api_key = os.environ["rapid_api_key"]
except KeyError:
    print("Error: 'rapid_api_key' environment variable is not set")
    sys.exit()


def get_country(val, row):
    geolocator = Nominatim(user_agent=client_app_name)
    geocode = partial(geolocator.geocode, language="en")
    location = geocode(row.city)
    return str(location).split(", ")[-1].lower()


def get_currency(val, row):
    country = CountryInfo(row.country)
    return country.currencies()[0].upper()


def convert_currency(val, row, base_cur, dest_cur, amount):
    url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"
    querystring = {"from": base_cur, "to": dest_cur, "amount": amount, "date": row.date}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com",
    }
    response = requests.request(
        "GET", url, headers=headers, params=querystring, timeout=60
    )
    if response.status_code == 200:
        deserialized_response = response.json()
        return deserialized_response["result"]


def transform_data(data):
    # Testing for the source dataset's existence
    try:
        if not os.path.exists(data):
            raise IOError(f"Source dataset {data} does not exist")
    except IOError as io_err:
        print("Error: " + str(io_err))
        sys.exit()

    # PETL transformation pipelines
    try:
        isodate = etl.dateparser("%Y-%m-%d")
        table = (
            etl.fromcsv(data)
            # Piping only features of interest
            .cut(*range(0, 11))
            # Deduplicating rows
            .distinct()
            # Expunging worthless records
            .select(lambda row: not (row.eur == "" and row.hrk == "" and row.lcy == ""))
            # Normalizing the date feature using REGEX
            .sub("date", r"^([0-9]{2})\.([0-9]{2})\.$", r"2018-\2-\1")
            .sub("date", r"^([0-9]{2})\.([0-9]{2})\.([0-9]{4})\.$", r"\3-\2-\1")
            .convert("date", isodate)
            # Inserting missing country values via geocoding
            .sub("city", r"^(warszaw)$", r"warsaw")
            .convert(
                "country",
                get_country,
                where=lambda row: row.country == "",
                pass_row=True,
            )
            .sub("country", r"^(czech|czechia)$", r"czech republic")
            # Inserting missing currency values via countryinfo API
            .convert(
                "currency",
                get_currency,
                where=lambda row: row.currency == "",
                pass_row=True,
            )
            # Converting from local (lcy) currency to Croatian Kuna (HRK) for missing (hrk) values
            .convert(
                "hrk",
                lambda v, row: convert_currency(v, row, row.currency, "HRK", row.lcy),
                where=lambda row: row.hrk == "",
                pass_row=True,
            )
            # Converting from the Croatian Kuna (HRK) to EUR for missing (eur) values
            .convert(
                "eur",
                lambda v, row: convert_currency(v, row, "HRK", "EUR", row.hrk),
                where=lambda row: row.eur == "",
                pass_row=True,
            )
            # Dropping the lcy feature due to its sparsity
            .cutout("lcy")
            # Normalizing the data type of all rates features
            .convert(("hrk", "eur"), lambda v: round(Decimal(v), 2))
        )
        return table
    except etl.errors.FieldSelectionError as petl_err:
        print("Error: " + str(petl_err))
        sys.exit()


def load_data(table):
    print("Loading transformed data to CSV ....")
    table.progress(50).tocsv(dest_descriptor, "UTF-8")


def main():
    load_data(table=transform_data(source_descriptor))


if __name__ == "__main__":
    main()
