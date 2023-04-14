class ErrorCodes:
    NOT_FOUND = 'Not Found'
    BAD_REQUEST = 'Bad Request'
    SERVER_ERROR = 'Server Error'
    PRODUCT_NOT_FOUND = (
        'Unable to find a product with the provided ID. '
        'Check the ID of the product you are entering.'
    )
    PRODUCT_DOES_NOT_EXIST = 'Product does not exist.'
    PRODUCT_ALREADY_EXISTS = 'Product with id already exists.'
    SMTH_WENT_WRONG = 'Something went wrong on requesting data from the website.'


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
