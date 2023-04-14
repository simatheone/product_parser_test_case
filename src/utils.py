from typing import Any

import requests
from fastapi import status

from src.constants import RESPONSE_KEY_MAPPING, URL_LINK
from src.exceptions import ProductNotFound, SomethingWentWrong


def get_product_data_from_website(nm_id: int) -> tuple[list[str], dict[str, Any]]:
    """Retrieve and parse product data from a website.

    Args:
    - nm_id (int): The ID of the product to fetch.

    Raises:
    - SomethingWentWrong: If there was an error while fetching the product data.

    Returns:
    - Result of a function `parser_fetched_product_data`.
    """

    fetched_product_data = fetch_product_data(nm_id)
    if not fetched_product_data:
        raise ProductNotFound()
    return parser_fetched_product_data(fetched_product_data)


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


def parser_fetched_product_data(
    fetched_product_data: dict[str, Any]
) -> tuple[list[str], dict[str, Any]]:
    """Parses the fetched data from a product and extracts relevant information.

    Args:
    - fetched_product_data (dict): The dictionary of data returned from the function
    `fetch_product_data`.

    Raises:
    - None.

    Returns:
    - A tuple containing:
        - A list of strings with the names of the product's colors.
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

    parsed_data = {}
    for new_key, response_key in RESPONSE_KEY_MAPPING.items():
        field_value = fetched_product_data[response_key]
        parsed_data[new_key] = field_value

    product_colors = []
    if fetched_product_data['colors']:
        for color in fetched_product_data['colors']:
            product_colors.append(color['name'])

    total_quantity = 0
    if fetched_product_data['sizes']:
        for size in fetched_product_data['sizes']:
            if size['stocks']:
                for quantity in size['stocks']:
                    total_quantity += quantity['qty']

    parsed_data['quantity'] = total_quantity

    return product_colors, parsed_data
