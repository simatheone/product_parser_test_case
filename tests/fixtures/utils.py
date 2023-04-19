import requests
import pytest
from fastapi import status

from src import utils


class MockResponse:
    def __init__(self, json_response, status_code):
        self.json_response = json_response
        self.status_code = status_code

    def json(self):
        return self.json_response


@pytest.fixture
def response_successful(monkeypatch):
    def mock_get(*args, **kwargs):
        json_response = {
            'data': {
                'products': [
                    {
                        'id': 123123123,
                        'root': 555555,
                        'subjectId': 626,
                        'name': 'Mocker Product Name',
                        'brand': 'Mocked Brand Name',
                        'brandId': 4444,
                        'siteBrandId': 45454,
                        'supplierId': 723416,
                        'sale': 15,
                        'priceU': 19999000,
                        'salePriceU': 16999100,
                        'pics': 2,
                        'rating': 5,
                        'feedbacks': 20,
                        'colors': [{'name': 'серый', 'id': 28374}],
                    },
                ],
            },
        }
        status_code = status.HTTP_200_OK
        return MockResponse(json_response, status_code)

    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.fixture
def response_failure(monkeypatch):
    def mock_get(*args, **kwargs):
        json_response = {
            'data': {
                'products': [],
            },
        }
        status_code = status.HTTP_404_NOT_FOUND
        return MockResponse(json_response, status_code)

    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.fixture
def fetch_empty_product_data(monkeypatch):
    def mock_fetch_product_data(*args, **kwargs):
        return []

    monkeypatch.setattr(utils, 'fetch_product_data', mock_fetch_product_data)


@pytest.fixture
def fetched_whole_product_data():
    return {
        'id': 143422485,
        'name': 'Футболка мужская набор 3 шт однотонные хлопок',
        'brand': 'OKO-group',
        'brandId': 93472,
        'siteBrandId': 103472,
        'supplierId': 409934,
        'sale': 42,
        'priceU': 231100,
        'salePriceU': 134000,
        'rating': 5,
        'feedbacks': 2240,
        'colors': [
            {'name': 'синий', 'id': 255},
            {'name': 'серый', 'id': 8421504},
            {'name': 'красный', 'id': 16711680},
        ],
        'sizes': [
            {
                'stocks': [
                    {
                        'qty': 196,
                    },
                    {
                        'qty': 1,
                    },
                ],
            },
            {
                'stocks': [
                    {
                        'qty': 263,
                    }
                ],
            },
            {
                'stocks': [
                    {
                        'qty': 156,
                    }
                ],
            },
            {
                'stocks': [
                    {
                        'qty': 143,
                    }
                ],
            },
            {
                'stocks': [
                    {
                        'qty': 147,
                    }
                ],
            },
        ],
    }


@pytest.fixture
def expected_result_product_data():
    return (
        [
            'синий',
            'серый',
            'красный',
        ],
        {
            'nm_id': 143422485,
            'name': 'Футболка мужская набор 3 шт однотонные хлопок',
            'brand': 'OKO-group',
            'brand_id': 93472,
            'site_brand_id': 103472,
            'supplier_id': 409934,
            'sale': 42,
            'price': 231100,
            'sale_price': 134000,
            'rating': 5,
            'feedbacks': 2240,
            'quantity': 906,
        },
    )


@pytest.fixture
def expected_result_parse_fetched_product_data():
    return {
        'nm_id': 143422485,
        'name': 'Футболка мужская набор 3 шт однотонные хлопок',
        'brand': 'OKO-group',
        'brand_id': 93472,
        'site_brand_id': 103472,
        'supplier_id': 409934,
        'sale': 42,
        'price': 231100,
        'sale_price': 134000,
        'rating': 5,
        'feedbacks': 2240,
    }


@pytest.fixture
def fetched_product_data_wrong_keys():
    return {
        'ID': 143422485,
        'Name': 'Футболка мужская набор 3 шт однотонные хлопок',
        'brandE': 'OKO-group',
        'brandID': 93472,
        'ID_siteBrand': 103472,
        'ID_supplier': 409934,
        'saleU': 42,
        'price': 231100,
        'salePrice': 134000,
        'ratin': 5,
        'feedback': 2240,
        'colours': [
            {'name': 'синий', 'id': 255},
            {'name': 'серый', 'id': 8421504},
            {'name': 'красный', 'id': 16711680},
        ],
        'sizess': [],
    }


@pytest.fixture
def fetched_product_data_with_empty_sizes():
    return {
        'id': 143422485,
        'name': 'Футболка мужская набор 3 шт однотонные хлопок',
        'brand': 'OKO-group',
        'brandId': 93472,
        'siteBrandId': 103472,
        'supplierId': 409934,
        'sale': 42,
        'priceU': 231100,
        'salePriceU': 134000,
        'rating': 5,
        'feedbacks': 2240,
        'colors': [
            {'name': 'синий', 'id': 255},
            {'name': 'серый', 'id': 8421504},
            {'name': 'красный', 'id': 16711680},
        ],
        'sizes': [],
    }


@pytest.fixture
def expected_result_product_data_with_empty_sizes():
    return (
        [
            'синий',
            'серый',
            'красный',
        ],
        {
            'nm_id': 143422485,
            'name': 'Футболка мужская набор 3 шт однотонные хлопок',
            'brand': 'OKO-group',
            'brand_id': 93472,
            'site_brand_id': 103472,
            'supplier_id': 409934,
            'sale': 42,
            'price': 231100,
            'sale_price': 134000,
            'rating': 5,
            'feedbacks': 2240,
            'quantity': 0,
        },
    )


@pytest.fixture
def fetched_product_data_with_empty_colors():
    return {
        'id': 143422485,
        'name': 'Футболка мужская набор 3 шт однотонные хлопок',
        'brand': 'OKO-group',
        'brandId': 93472,
        'siteBrandId': 103472,
        'supplierId': 409934,
        'sale': 42,
        'priceU': 231100,
        'salePriceU': 134000,
        'rating': 5,
        'feedbacks': 2240,
        'colors': [],
        'sizes': [
            {
                'stocks': [
                    {
                        'qty': 263,
                    }
                ],
            },
        ],
    }


@pytest.fixture
def expected_result_product_data_with_empty_colors():
    return (
        [],
        {
            'nm_id': 143422485,
            'name': 'Футболка мужская набор 3 шт однотонные хлопок',
            'brand': 'OKO-group',
            'brand_id': 93472,
            'site_brand_id': 103472,
            'supplier_id': 409934,
            'sale': 42,
            'price': 231100,
            'sale_price': 134000,
            'rating': 5,
            'feedbacks': 2240,
            'quantity': 263,
        },
    )


@pytest.fixture
def fetched_product_data_with_no_sizes():
    return {
        'id': 143422485,
        'name': 'Футболка мужская набор 3 шт однотонные хлопок',
        'brand': 'OKO-group',
        'brandId': 93472,
        'siteBrandId': 103472,
        'supplierId': 409934,
        'sale': 42,
        'priceU': 231100,
        'salePriceU': 134000,
        'rating': 5,
        'feedbacks': 2240,
        'colors': [
            {'name': 'синий', 'id': 255},
        ],
    }


@pytest.fixture
def expected_result_product_data_with_no_sizes():
    return {
        'id': 143422485,
        'name': 'Футболка мужская набор 3 шт однотонные хлопок',
        'brand': 'OKO-group',
        'brandId': 93472,
        'siteBrandId': 103472,
        'supplierId': 409934,
        'sale': 42,
        'priceU': 231100,
        'salePriceU': 134000,
        'rating': 5,
        'feedbacks': 2240,
        'colors': [
            'синий',
        ],
        'quantity': 0,
    }


@pytest.fixture
def fetched_product_data_with_no_colors():
    return {
        'id': 143422485,
        'name': 'Футболка мужская набор 3 шт однотонные хлопок',
        'brand': 'OKO-group',
        'brandId': 93472,
        'siteBrandId': 103472,
        'supplierId': 409934,
        'sale': 42,
        'priceU': 231100,
        'salePriceU': 134000,
        'rating': 5,
        'feedbacks': 2240,
        'sizes': [
            {
                'stocks': [
                    {
                        'qty': 263,
                    }
                ],
            },
        ],
    }


@pytest.fixture
def fetched_product_colors_valid():
    return [
        {'name': 'синий', 'id': 255},
        {'name': 'серый', 'id': 8421504},
        {'name': 'красный', 'id': 16711680},
    ]


@pytest.fixture
def expected_result_fetched_valid_colors():
    return [
        'синий',
        'серый',
        'красный',
    ]


@pytest.fixture
def fetched_product_colors_without_name_key():
    return [
        {'title': 'синий', 'id': 255},
        {'title': 'серый', 'id': 8421504},
        {'title': 'красный', 'id': 16711680},
    ]


@pytest.fixture
def fetched_product_sizes_without_stocks_key():
    return [
        {
            'stock': [
                {
                    'qty': 196,
                },
            ],
        },
        {
            'stock': [
                {
                    'qty': 263,
                }
            ],
        },
    ]


@pytest.fixture
def fetched_product_sizes_without_qty_key():
    return [
        {
            'stocks': [
                {
                    'quantity': 196,
                },
            ],
        },
        {
            'stocks': [
                {
                    'quantity': 263,
                }
            ],
        },
    ]


@pytest.fixture
def fetched_product_sizes_valid():
    return [
        {
            'stocks': [
                {
                    'qty': 196,
                },
            ],
        },
        {
            'stocks': [
                {
                    'qty': 263,
                }
            ],
        },
    ]


@pytest.fixture
def expected_result_fetched_valid_sizes():
    return 459


@pytest.fixture
def mock_fetch_product_data_whole_product(monkeypatch, fetched_whole_product_data):
    def mock_fetch_product_function(*args, **kwargs):
        return fetched_whole_product_data

    monkeypatch.setattr(utils, 'fetch_product_data', mock_fetch_product_function)


@pytest.fixture
def mock_fetch_product_data_with_empty_colors(
    monkeypatch, fetched_product_data_with_empty_colors
):
    def mock_fetch_product_function(*args, **kwargs):
        return fetched_product_data_with_empty_colors

    monkeypatch.setattr(utils, 'fetch_product_data', mock_fetch_product_function)


@pytest.fixture
def mock_fetch_product_data_with_empty_sizes(
    monkeypatch, fetched_product_data_with_empty_sizes
):
    def mock_fetch_product_function(*args, **kwargs):
        return fetched_product_data_with_empty_sizes

    monkeypatch.setattr(utils, 'fetch_product_data', mock_fetch_product_function)
