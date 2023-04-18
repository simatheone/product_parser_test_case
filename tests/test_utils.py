import pytest

from src.exceptions import JSONKeyNotFound, ProductNotFound, SomethingWentWrong
from src.utils import (
    fetch_product_data,
    get_product_data_from_website,
    parse_fetched_product_data,
    check_fetched_product_data_keys,
    parse_fetched_product_colors,
    parse_fetched_product_quantity,
)


def test_get_product_data_from_website_no_product(fetch_empty_product_data):
    """
    Test case for get_product_data_from_website when no product is found on the website.

    Args:
    - fetch_empty_product_data: pytest fixture that provides mocked empty product data
    """
    with pytest.raises(ProductNotFound):
        get_product_data_from_website(12345)


@pytest.mark.parametrize(
    'product_data, expected_result',
    [
        (
            'mock_fetch_product_data_whole_product',
            'expected_result_product_data'
        ),
        (
            'mock_fetch_product_data_with_empty_colors',
            'expected_result_product_data_with_empty_colors',
        ),
        (
            'mock_fetch_product_data_with_empty_sizes',
            'expected_result_product_data_with_empty_sizes',
        ),
    ],
)
def test_get_product_data_from_website_success(product_data, expected_result, request):
    """
    Test case for get_product_data_from_website when the function returns expected
    results.

    Args:
    - product_data: Fixture that provides mock product data for testing.
    - expected_result: Fixture that provides expected result for comparison.
    - request: pytest fixture used to retrieve other fixtures.
    """
    product_data = request.getfixturevalue(product_data)
    expected_result = request.getfixturevalue(expected_result)
    assert get_product_data_from_website(product_data) == expected_result


@pytest.mark.parametrize(
    'product_data',
    [
        'fetched_product_data_with_no_sizes',
        'fetched_product_data_with_no_colors',
        'fetched_product_data_wrong_keys',
    ],
)
def test_check_fetched_product_data_keys(product_data, request):
    """
    Test case for check_fetched_product_data_keys when keys are not present in a
    response JSON.

    Args:
    - product_data: Fixture that provides mock product data for testing.
    - request: pytest fixture used to retrieve other fixtures.
    """
    product_fixture = request.getfixturevalue(product_data)
    with pytest.raises(JSONKeyNotFound):
        check_fetched_product_data_keys(product_fixture)


def test_fetch_product_data_success(response_successful):
    """
    Test case for fetch_product_data when the response is successful and all product
    data is fetched.

    Args:
    - response_successful: pytest fixture that provides mocked successful response
    """
    product_id = 123123123
    fetched_product_data = fetch_product_data(product_id)
    assert fetched_product_data['id'] == product_id


def test_fetch_product_data_failure(response_failure):
    """
    Test case for fetch_product_data when the response status code differs from 200.

    Args:
    - response_failure: pytest fixture that provides mocked failure response
    """
    with pytest.raises(SomethingWentWrong):
        fetch_product_data(12345)


def test_parse_fetched_product_data(
    fetched_whole_product_data, expected_result_parse_fetched_product_data
):
    """
    Test case for parse_fetched_product_data when the function successfully parses
    fetched product data.

    Args:
    - fetched_whole_product_data: Fixture that provides mock fetched product
      data for testing.
    - expected_result_parse_fetched_product_data: Fixture that provides expected
      result for comparison.
    """
    assert (
        parse_fetched_product_data(fetched_whole_product_data)
        == expected_result_parse_fetched_product_data
    )


def test_parse_fetched_product_colors_success(
    fetched_product_colors_valid, expected_result_fetched_valid_colors
):
    """
    Test case for parse_fetched_product_colors with valid colors data of a fetched
    product.

    Args:
    - fetched_product_colors_valid: pytest fixture that provides valid colors data.
    - expected_result_fetched_valid_colors: pytest fixture that provides the expected
      result for the test.
    """
    assert (
        parse_fetched_product_colors(fetched_product_colors_valid)
        == expected_result_fetched_valid_colors
    )


def test_parse_fetched_product_colors_failure_no_name_key(
    fetched_product_colors_without_name_key,
):
    """
    Test case for parse_fetched_product_colors when the colors data of a fetched product
    does not contain the 'name' key.

    Args:
    - fetched_product_colors_without_name_key: pytest fixture that provides
    colors data without 'name' key.
    """
    with pytest.raises(JSONKeyNotFound):
        parse_fetched_product_colors(fetched_product_colors_without_name_key)


def test_parse_fetched_product_quantity_success(
    fetched_product_sizes_valid, expected_result_fetched_valid_sizes
):
    """
    Test case for parse_fetched_product_quantity when the fetched product has
    valid 'sizes' data.

    Args:
    - fetched_product_sizes_valid: pytest fixture that provides fetched product data
      with valid 'sizes'.
    - expected_result_fetched_valid_sizes: pytest fixture that provides the expected
      result for the test.
    """
    assert (
        parse_fetched_product_quantity(fetched_product_sizes_valid)
        == expected_result_fetched_valid_sizes
    )


def test_parse_fetched_product_quantity_failure_no_stocks_key(
    fetched_product_sizes_without_stocks_key,
):
    """
    Test case for parse_fetched_product_quantity when the 'stocks' key is not present
    in the product 'sizes'.

    Args:
    - fetched_product_sizes_without_stocks_key: pytest fixture that provides
    fetched product data without 'stocks' key.
    """
    with pytest.raises(JSONKeyNotFound):
        parse_fetched_product_quantity(fetched_product_sizes_without_stocks_key)


def test_parse_fetched_product_quantity_failure_no_qty_key(
    fetched_product_sizes_without_qty_key,
):
    """
    Test case for parse_fetched_product_quantity when the 'qty' key is not present
    in the product 'sizes'.

    Args:
    - fetched_product_sizes_without_qty_key: pytest fixture that provides
    fetched product data without 'qty' key.
    """
    with pytest.raises(JSONKeyNotFound):
        parse_fetched_product_quantity(fetched_product_sizes_without_qty_key)
