#!/usr/bin/env python3
import requests
from decimal import Decimal
import petl as etl

isodate = etl.dateparser("%Y-%m-%d")
def retrieve_rates():
    eur_hrk_rates = {}
    url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/timeseries"
    querystring = {"start_date":"2018-01-01","end_date":"2018-12-31","from":"HRK","to":"EUR"}
    headers = {
        "X-RapidAPI-Key": "c892889770msh34b4611091f1e65p1b3a02jsnaca2efec6843",
        "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com",
    }
    response = requests.request("GET", url, headers=headers, params=querystring, timeout=60)
    if response.status_code == 200:
        deserialized_response = response.json()
        rates = deserialized_response['rates']
        for date, rate in rates.items():
            norm_date = isodate(date)
            eur_hrk_rates[norm_date] = rate['HRK']
        return eur_hrk_rates

r = retrieve_rates()

table1 = [['foo', 'bar', 'baz'],
           ['A', '2.4', 12],
          ['B', '5.7', 34],
          ['C', '1.2', 56]]

table2 = etl.convert(table1, 'foo', lambda v, row: float(row.bar) / r[isodate('2018-11-20')], pass_row=True)
table2

