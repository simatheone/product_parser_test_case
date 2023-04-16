from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.constants import AdditionalResponses
from src.dependencies import (
    get_async_session,
    validate_product_exists,
    validate_unique_product,
)
from src.schemas import ProductRequest, ProductResponse
from src.service import product_service
from src.utils import get_product_data_from_website

router = APIRouter(
    prefix='/products',
    tags=[
        'Product',
    ],
)


@router.get('/all', response_model=list[ProductResponse])
async def get_all_products(session: AsyncSession = Depends(get_async_session)):
    """Endpoint to retrieve all products from the database."""
    return await product_service.get_product_multi(session)


@router.get(
    '/{product_id}',
    response_model=ProductResponse,
    responses={**AdditionalResponses.PRODUCT_GET_DELETE},
)
async def get_single_product(
    product_id: int = Depends(validate_product_exists),
    session: AsyncSession = Depends(get_async_session),
):
    """Endpoint to retrieve a single product by ID from the database.

    - **product_id** (int): The ID of the product to be retrieved (path parameter).
    """
    return await product_service.get_product(product_id, session)


@router.post(
    '/',
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    responses={**AdditionalResponses.PRODUCT_CREATE},
)
async def create_new_product(
    product_id: ProductRequest = Depends(validate_unique_product),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Endpoint to creates a new product in the database from the information of
    a product found on a website.

    - **product_id** (int): The ID of the product to be fetched and created
      (query parameter).
    """
    colors, product_info = get_product_data_from_website(product_id.nm_id)
    return await product_service.create_product(product_info, colors, session)


@router.delete(
    '/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**AdditionalResponses.PRODUCT_GET_DELETE},
)
async def delete_product(
    product_id: int = Depends(validate_product_exists),
    session: AsyncSession = Depends(get_async_session),
):
    """Endpoint to delete a product by ID.

    - **product_id** (int): The ID of the product to be deleted (path parameter).
    """
    await product_service.remove_product(product_id, session)
    return
