import pytest

@pytest.fixture
def product_data():
    return {
            'name':'product',
            'discription':'product_discription',
            'price':10,
            'in_stock':1,
            'category':'category',
            'seller':'seller',
            'owner':'owner',
            }