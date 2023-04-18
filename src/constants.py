URL_LINK = 'https://card.wb.ru/cards/detail?curr=rub&dest=-1257786&spp=0&nm={nm_id}'

RESPONSE_KEY_MAPPING = {
    'nm_id': 'id',
    'name': 'name',
    'brand': 'brand',
    'brand_id': 'brandId',
    'site_brand_id': 'siteBrandId',
    'supplier_id': 'supplierId',
    'sale': 'sale',
    'price': 'priceU',
    'sale_price': 'salePriceU',
    'rating': 'rating',
    'feedbacks': 'feedbacks',
}


class ErrorCodes:
    """Constants for exception messages."""

    NOT_FOUND = 'Not Found'
    BAD_REQUEST = 'Bad Request'
    SERVER_ERROR = 'Server Error'
    PRODUCT_NOT_FOUND = (
        'Unable to find a product with the provided ID. '
        'Check the ID of the product you are entering.'
    )
    PRODUCT_DOES_NOT_EXIST = 'Product does not exist.'
    PRODUCT_ALREADY_EXISTS = 'Product with this id already exists.'
    SMTH_WENT_WRONG = 'Something went wrong on requesting data from the website.'
    PRODUCT_JSON_KEY_NOT_FOUND = (
        'An expected key was not found in response prodcut data or it was renamed. '
        'Unabled to parse fetched data.'
    )


class AdditionalResponses:
    """Additional error repsonses for Product endpoints."""

    PRODUCT_GET_DELETE = {
        404: {
            'content': {
                'application/json': {
                    'example': {'detail': ErrorCodes.PRODUCT_DOES_NOT_EXIST}
                },
            },
            'description': 'When a product does not exist in database.',
        }
    }
    PRODUCT_CREATE = {
        400: {
            'content': {
                'application/json': {
                    'example': {'detail': ErrorCodes.PRODUCT_ALREADY_EXISTS}
                },
            },
            'description': 'When a product already exists in database.',
        },
        404: {
            'content': {
                'application/json': {
                    'example': {'detail': ErrorCodes.PRODUCT_NOT_FOUND}
                },
            },
            'description': 'When you entered invalid product id.',
        },
        500: {
            'content': {
                'application/json': {'example': {'detail': ErrorCodes.SMTH_WENT_WRONG}},
            },
            'description': (
                'Due to some reasons it is impossible to '
                'make a proper request to the Wildberries website.'
            ),
        },
    }
