import petl as etl
from configparser import ConfigParser
import os
import sys
from etl_program import transform_data

try:
    config_file = "config.ini"
    if not os.path.exists(config_file):
        raise IOError(f"Configuration file {config_file} does not exist")
    else:
        config = ConfigParser()
        config.read(config_file)
        test_descriptor = config["FILE"]["test_file_desc"]
except IOError as e:
    print("Error: " + str(e))
    sys.exit()


def test_transform_data():
    """There should be no record with missing values for test to pass"""
    test_table = transform_data(test_descriptor)
    test_table2 = etl.select(test_table, lambda row: any(v is None for v in row))
    assert 0 == etl.nrows(test_table2)
