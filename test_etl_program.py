import petl as etl
import random
from etl_program import transform_data

random_row = random.randint(1, 10)
# Read a random row from CSV file into a petl table
table = (
    etl.fromcsv("data/test_data.csv")
    .addrownumbers()
    .select("row", lambda v: v == random_row)
    .cutout("row")
)

# sink random row to memory in bytes
sink = etl.MemorySource()
table.tocsv(sink)
random_data = sink.getvalue()


def test_transform_data():
    """There should be no record with missing values for test to pass"""
    source = etl.MemorySource(random_data)
    test_table = transform_data(source)
    test_table2 = etl.select(test_table, lambda row: any(v is None for v in row))
    assert 0 == etl.nrows(test_table2)
