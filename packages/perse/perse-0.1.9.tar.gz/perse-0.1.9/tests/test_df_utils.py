import pytest
import numpy as np
from perse import DataFrame

@pytest.fixture
def data_():
    np.random.seed(42)
    data = {
        'A': range(10),
        'B': range(10),
        'C': range(10)
    }
    return DataFrame(data)

def test_to_csv(data_):
    data_.to_csv('test.csv')
    data_ > 'test2.csv'

def test_to_json(data_):
    data_.to_csv('test.json')
    data_ > 'test2.json'

def test_to_excel(data_):
    data_.to_csv('test.xlsx')
    data_ > 'test2.xlsx'