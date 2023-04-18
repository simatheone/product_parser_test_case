from typing import Any, Sequence

from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Color, Product
from src.schemas import CustomParams, ProductCreate


class ProductService:
    """Service class for handling database operations related to products.

    Attributes:
    - model: The SQLAlchemy model representing the `Product` entity in the database.

    Methods:
    - `get_product`: Retrieves a product from the database by its unique identifier.
    - `get_product_multi`: Retrieves multiple products from the database.
    - `create_product`: Creates a new product in the database with the provided data.
    - `remove_product`: Removes a product from the database by its unique identifier.
    - `get_color_by_name`: Retrieves a color from the database by its name.
    """

    def __init__(self, model):
        self.model = model

    async def get_product(
        self, product_id: int, session: AsyncSession
    ) -> Product | None:
        """Retrieves a product from the database by its unique identifier.

        Args:
        - product_id (int): The ID of the product to retrieve.
        - session (AsyncSession): The async SQLAlchemy session to use for database
          operations.

        Raises:
        - None

        Returns:
        - Union[Product, None]: The product with the specified ID if it exists in
          the database, or None if it does not exist.
        """

        stmt = (
            select(self.model)
            .options(selectinload(self.model.colors))
            .where(self.model.nm_id == product_id)
        )
        product_db = await session.execute(stmt)
        return product_db.scalars().first()

    async def get_product_multi(
        self, params: CustomParams, session: AsyncSession
    ) -> Sequence[Product]:
        """Retrieves multiple products from the database.

        Args:
        - session (AsyncSession): The async SQLAlchemy session to use for database
          operations.

        Raises:
        - None

        Returns:
        - Union[Sequence[Product], None]: A sequence of products if there are any
          in the database, or None if the database is empty.
        """
        stmt = (
            select(self.model)
            .options(selectinload(self.model.colors))
            .group_by(self.model.brand, self.model.nm_id)
            .order_by(
                self.model.sale_price,
                desc(self.model.nm_id),
            )
        )
        products_db = await paginate(conn=session, query=stmt, params=params)
        return products_db

    async def create_product(
        self,
        product_data_in: dict[str, Any],
        colors: list[str] | list[None],
        session: AsyncSession,
    ) -> ProductCreate:
        """Create a new product in the database with the provided data.

        Args:
        - product_data_in (dict): A dictionary containing the data for the new
          product.
        - colors (list[str]): A list of color names associated with the new
          product.
        - session (AsyncSession): An async SQLAlchemy session.

        Raises:
        - None

        Returns:
        - ProductCreate: A Pydantic schema representing the newly created product.
        """
        db_product = self.model(**product_data_in)
        db_product.colors = []
        for color_name in colors:
            color = await self.get_color_by_name(color_name, session)
            if color is None:
                color = Color(name=color_name)
                session.add(color)
            db_product.colors.append(color)

        session.add(db_product)
        await session.commit()
        return db_product

    async def remove_product(self, product_id: int, session: AsyncSession) -> None:
        """Removes a product from the database by its unique identifier.

        Args:
        - product_id (int): The ID of the product to remove.
        - session (AsyncSession): The async SQLAlchemy session to use for database
          operations.

        Raises:
        - None

        Returns:
        - None.
        """
        await session.execute(delete(self.model).where(self.model.nm_id == product_id))
        await session.commit()

    async def get_color_by_name(
        self, color_name: str, session: AsyncSession
    ) -> Color | None:
        """Retrieves a color from the database by its name.

        Args:
        - color_name (str): The name of the color to retrieve.
        - session (AsyncSession): The async SQLAlchemy session to use for database
          operations.

        Raises:
        - None

        Returns:
        - Union[Color, None]: The color with the specified name if it exists in the
          database, or None if it does not exist.
        """
        color = await session.execute(select(Color).where(Color.name == color_name))
        return color.scalars().first()


product_service = ProductService(Product)
