from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import async_session
from src.exceptions import ProductAlreadyExists, ProductDoesNotExist
from src.schemas import ProductRequest
from src.service import product_service


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Returns an async generator that yields an async SQLAlchemy session.

    Yields:
    - AsyncSession: An async SQLAlchemy session.

    Raises:
    - None

    Note:
    - This function should be used as a dependency in route functions that require
    a database session.
    """

    async with async_session() as session:
        yield session


async def validate_product_exists(
    product_id: int, session: AsyncSession = Depends(get_async_session)
) -> int:
    """Validates that a product with the specified ID exists in the database.

    Args:
    - product_id (int): The ID of the product to validate.
    - session (AsyncSession): The async SQLAlchemy session to use for database operations.

    Returns:
    - int: The product ID if it exists in the database.

    Raises:
    - ProductDoesNotExist: If a product with the specified ID does not exist in the database.

    Note:
    - This function can be used as a dependency in route functions that require
    a product validation by ID.
    """

    if not await product_service.get_product(product_id, session):
        raise ProductDoesNotExist()
    return product_id


async def validate_unique_product(
    product_id_in: ProductRequest, session: AsyncSession = Depends(get_async_session)
) -> ProductRequest:
    """Validates that a product with the specified ID does not already exist in the database.

    Args:
    - product_id_in (ProductRequest): The ID of the product to validate.
    - session (AsyncSession): The async SQLAlchemy session to use for database operations.

    Returns:
    - ProductRequest: The product ID if it does not already exist in the database.

    Raises:
    - ProductAlreadyExists: If a product with the specified ID already exists in the database.

    Note:
    - This function can be used as a dependency in route functions that require
    a unique product ID.
    """

    if await product_service.get_product(product_id_in.nm_id, session):
        raise ProductAlreadyExists()
    return product_id_in
