import petl as etl
from etl_program import transform_data


def test_transform_data():
    """There should be no record with missing values for test to pass"""
    test_table = transform_data("data/test_data.csv")
    test_table2 = etl.select(test_table, lambda rec: any(v == None for v in rec))
    assert 0 == etl.nrows(test_table2)
