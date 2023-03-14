#!/usr/bin/env python3
import os
import sys
import petl as etl
from configparser import ConfigParser
import re

# Declaring global configurations from config file
config = ConfigParser()
if os.path.exists('../config.ini'):
    config.read('../config.ini')
    file = config['CONFIG']['file_desc']
else:
    print("Configuration File descriptor `config.ini` does not exist")
    sys.exit()

def NormalizeDates(val, row):
    isodate = etl.dateparser('%d-%m-%Y')
    pattern = r"[0-9]{2}.[0-9]{2}.$"
    if re.search(pattern, val):
        val = '-'.join(val[:len(val)].split('.'))
        val += '2018'
    if val.endswith('.'):
        val = '-'.join(val[:len(val)-1].split('.'))
    return isodate(val)

def TransformData():
    table = (
        etl
        .fromcsv(file).cut(*range(0,11))
        .convert('date', NormalizeDates, pass_row=True)
    )
    print(table.look())

TransformData()
