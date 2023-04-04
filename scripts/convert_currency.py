#!/usr/bin/env python3
import requests


def convert(base_cur, dest_cur, amt, dt):
    url = "https://currency-conversion-and-exchange-rates.p.rapidapi.com/convert"
    querystring = {"from": base_cur, "to": dest_cur, "amount": amt, "date": dt}
    headers = {
        "X-RapidAPI-Key": "----Your API key goes here----",
        "X-RapidAPI-Host": "currency-conversion-and-exchange-rates.p.rapidapi.com",
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()


r = convert("PLN", "HRK", "239.40", "2018-09-20")
print(r["result"], type(r), r)
