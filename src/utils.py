from typing import Any

import requests
from fastapi import status

from src.constants import RESPONSE_KEY_MAPPING, URL_LINK
from src.exceptions import JSONKeyNotFound, ProductNotFound, SomethingWentWrong


def get_product_data_from_website(
    nm_id: int,
) -> tuple[list[str] | list[None], dict[str, Any]]:
    """
    Retrieve and parse product data from a website.

    Args:
    - nm_id (int): The ID of the product to fetch.

    Raises:
    - SomethingWentWrong: If there was an error while fetching the product data.

    Returns:
    - Result of a functions `parse_fetched_product_data`,
      `parse_fetched_product_colors`.
    """
    fetched_product_data = fetch_product_data(nm_id)
    if not fetched_product_data:
        raise ProductNotFound()

    check_fetched_product_data_keys(fetched_product_data)

    parsed_product_data = parse_fetched_product_data(fetched_product_data)

    product_colors = []
    product_quantity = 0
    if fetched_product_data['colors']:
        product_colors = parse_fetched_product_colors(fetched_product_data['colors'])

    if fetched_product_data['sizes']:
        product_quantity = parse_fetched_product_quantity(fetched_product_data['sizes'])

    parsed_product_data['quantity'] = product_quantity
    return product_colors, parsed_product_data


def check_fetched_product_data_keys(fetched_product_data: dict[str, Any]) -> None:
    """
    Checks if the required keys are present in the fetched product data dictionary.

    Args:
    - fetched_product_data: The dictionary containing the fetched product data.

    Raises:
    - JSONKeyNotFound: If any of the required keys from RESPONSE_KEY_MAPPING values,
    'colors' and 'sizes', are not found.
    """
    for response_key in RESPONSE_KEY_MAPPING.values():
        if fetched_product_data.get(response_key, None) is None:
            raise JSONKeyNotFound()

    if fetched_product_data.get('colors', None) is None:
        raise JSONKeyNotFound()

    if fetched_product_data.get('sizes', None) is None:
        raise JSONKeyNotFound()


def fetch_product_data(nm_id: int) -> dict[str, Any]:
    """Fetches product data from the URL_LINK.

    Args:
    - nm_id (int): The ID of the product to fetch.

    Returns:
    - dict[str, Any]: A dictionary containing the fetched product data.

    Raises:
    - SomethingWentWrong: If there was an error while fetching the product data.
    """
    request_url = URL_LINK.format(nm_id=nm_id)
    response = requests.get(request_url)

    if response.status_code != status.HTTP_200_OK:
        raise SomethingWentWrong()

    json_response = response.json()
    product_data = json_response['data']['products']

    return dict(*product_data)


def parse_fetched_product_data(fetched_product_data: dict[str, Any]) -> dict[str, Any]:
    """
    Parses the fetched data from a product and extracts relevant information.

    Args:
    - fetched_product_data (dict): The dictionary containing the fetched product data.

    Returns:
    - A dictionary with the following keys and values:
        - nm_id (int): The product ID.
        - name (str): The name of the product.
        - brand (str): The brand name of the product.
        - brand_id (int): The brand ID of the product.
        - site_brand_id (int): The site brand ID of the product.
        - supplier_id (int): The supplier ID of the product.
        - sale (float): The discount percentage for the product.
        - price (int): The original price of the product.
        - sale_price (int): The sale price of the product.
        - rating (float): The rating of the product.
        - feedbacks (int): The number of feedbacks for the product.
    """
    parsed_product_data = {}
    for new_key, response_key in RESPONSE_KEY_MAPPING.items():
        field_value = fetched_product_data.get(response_key)
        parsed_product_data[new_key] = field_value

    return parsed_product_data


def parse_fetched_product_colors(
    fetched_product_colors: list[dict[str, Any]]
) -> list[str]:
    """
    Parses the colors data from the fetched product data dictionary.

    Args:
    - fetched_product_data (dict): The dictionary containing the fetched product data.

    Raises:
    - JSONKeyNotFound: If the 'name' key is not found in the 'colors' data.

    Returns:
    - A list of color names extracted from the fetched product data.
    """
    parsed_product_colors = []
    for color in fetched_product_colors:
        color_name = color.get('name', None)

        if color_name is None:
            raise JSONKeyNotFound()

        parsed_product_colors.append(color_name)
    return parsed_product_colors


def parse_fetched_product_quantity(fetched_product_sizes: list[dict[str, Any]]) -> int:
    """
    Parses the total quantity of a product from the fetched product data dictionary.

    Args:
    - fetched_product_data (dict): The dictionary containing the fetched product data.

    Raises:
    - JSONKeyNotFound: If the 'stocks' key or 'qty' key is not found in the
    'sizes' data.

    Returns:
    - The total quantity of the product extracted from the fetched product data.
    """
    total_quantity = 0
    for size in fetched_product_sizes:
        if size.get('stocks', None) is None:
            raise JSONKeyNotFound()

        for quantity in size['stocks']:
            if quantity.get('qty', None) is None:
                raise JSONKeyNotFound()

            total_quantity += quantity['qty']

    return total_quantity
