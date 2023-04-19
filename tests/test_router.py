import pytest

from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_products_all_endpoint_no_products(async_client: AsyncClient):
    response = await async_client.get('products/all?page=1&size=10')
    assert (
        response.status_code == status.HTTP_200_OK
    ), 'Response status code differs fromn expected status code 200.'
    assert response.json() == {
        'items': [],
        'page': 1,
        'pages': 0,
        'size': 10,
        'total': 0,
    }


@pytest.mark.asyncio
async def test_products_all_endpoint_with_multi_products(
    create_multiple_product, async_client: AsyncClient
):
    response = await async_client.get('products/all?page=1&size=10')
    assert (
        response.status_code == status.HTTP_200_OK
    ), 'Response status code differs fromn expected status code 200.'
    assert response.json()['total'] == 2
    assert response.json()['items'][0]['nm_id'] == 2
    assert response.json()['items'][1]['nm_id'] == 1


@pytest.mark.asyncio
async def test_get_not_existing_product(async_client: AsyncClient):
    product_id = 111
    response = await async_client.get(f'products/{product_id}')
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), 'Response status code differs fromn expected status code 404.'
    assert response.json() == {'detail': 'Product does not exist.'}


@pytest.mark.asyncio
async def test_get_existing_product(create_new_product, async_client: AsyncClient):
    product_id = 143422485
    response = await async_client.get(f'products/{product_id}')
    json_response = response.json()
    assert (
        response.status_code == status.HTTP_200_OK
    ), 'Response status code differs fromn expected status code 200.'
    assert json_response['nm_id'] == product_id


@pytest.mark.asyncio
async def test_create_product(async_client: AsyncClient):
    product_id = 139760619
    response = await async_client.post('products/', json={'nm_id': product_id})
    assert (
        response.status_code == status.HTTP_201_CREATED
    ), 'Response status code differs fromn expected status code 201.'
    assert response.json()['nm_id'] == product_id


@pytest.mark.asyncio
async def test_delete_existing_product(async_client: AsyncClient):
    product_id = 143422485
    response = await async_client.delete(f'products/{product_id}')
    assert (
        response.status_code == status.HTTP_204_NO_CONTENT
    ), 'Response status code differs fromn expected status code 204.'


@pytest.mark.asyncio
async def test_delete_not_existing_product(async_client: AsyncClient):
    product_id = 111
    response = await async_client.delete(f'products/{product_id}')
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), 'Response status code differs fromn expected status code 404.'
    assert response.json() == {'detail': 'Product does not exist.'}


@pytest.mark.asyncio
async def test_create_product_twice(async_client: AsyncClient):
    product_id = 139760619
    response = await async_client.post('products/', json={'nm_id': product_id})
    response = await async_client.post('products/', json={'nm_id': product_id})
    assert (
        response.status_code == status.HTTP_400_BAD_REQUEST
    ), 'Response status code differs fromn expected status code 400.'
    assert response.json() == {'detail': 'Product with this id already exists.'}
