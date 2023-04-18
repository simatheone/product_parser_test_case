import pytest

from fastapi import status
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_products_all_endpoint(async_client: AsyncClient):
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
async def test_get_single_product(async_client: AsyncClient):
    response = await async_client.get('products/111')
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), 'Response status code differs fromn expected status code 404.'
    assert response.json() == {'detail': 'Product does not exist.'}


@pytest.mark.asyncio
async def test_delete_not_existing_product(async_client: AsyncClient):
    response = await async_client.delete('products/111')
    assert (
        response.status_code == status.HTTP_404_NOT_FOUND
    ), 'Response status code differs fromn expected status code 404.'
    assert response.json() == {'detail': 'Product does not exist.'}


@pytest.mark.asyncio
async def test_create_product(async_client: AsyncClient):
    response = await async_client.post('products/', json={'nm_id': 139760619})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['nm_id'] == 139760619


@pytest.mark.asyncio
async def test_delete_existing_product(async_client: AsyncClient):
    response = await async_client.delete('products/139760619')
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_create_product_twice(async_client: AsyncClient):
    response = await async_client.post('products/', json={'nm_id': 139760619})
    response = await async_client.post('products/', json={'nm_id': 139760619})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'detail': 'Product with this id already exists.'}
