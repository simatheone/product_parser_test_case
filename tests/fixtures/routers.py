import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Product


@pytest_asyncio.fixture
async def create_new_product(async_session: AsyncSession) -> None:
    new_product = Product(
        **{
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
        }
    )
    new_product.colors = []
    async_session.add(new_product)
    await async_session.commit()


@pytest_asyncio.fixture
async def create_multiple_product(async_session: AsyncSession):
    products = []
    for value in range(1, 3):
        product = {
            'nm_id': value,
            'name': f'Футболка мужская {value}',
            'brand': 't-shirt',
            'brand_id': value,
            'site_brand_id': value,
            'supplier_id': value,
            'sale': 42,
            'price': 231100,
            'sale_price': 134000,
            'rating': 5,
            'feedbacks': 240,
            'quantity': 10,
            'colors': [],
        }
        products.append(product)

    products = await async_session.execute(insert(Product), products)
    await async_session.commit()
