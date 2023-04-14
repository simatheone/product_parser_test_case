from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

product_color_bridge_table = Table(
    'product_color_bridge_table',
    Base.metadata,
    Column('nm_id', ForeignKey('product.nm_id', ondelete='CASCADE'), primary_key=True),
    Column(
        'color_id', ForeignKey('color.color_id', ondelete='CASCADE'), primary_key=True
    ),
)


class Product(Base):
    """Product model."""

    __tablename__ = 'product'

    nm_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(256))
    brand: Mapped[str] = mapped_column(String(256))
    brand_id: Mapped[int]
    site_brand_id: Mapped[int]
    supplier_id: Mapped[int]
    sale: Mapped[int] = mapped_column(default=0)
    price: Mapped[int]
    sale_price: Mapped[int]
    rating: Mapped[int] = mapped_column(default=0)
    feedbacks: Mapped[int] = mapped_column(default=0)
    colors: Mapped[list['Color']] = relationship(
        secondary=product_color_bridge_table,
        back_populates='products',
        cascade='all, delete',
    )
    quantity: Mapped[int] = mapped_column(default=0)

    def __repr__(self) -> str:
        """String representation of a Product model."""

        return (
            f'Product(id={self.nm_id}), Name={self.name}, Brand={self.brand}, '
            f'Price={self.price}, Rating={self.rating}'
        )


class Color(Base):
    """Color model."""

    __tablename__ = 'color'

    color_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    products: Mapped[list['Product']] = relationship(
        secondary=product_color_bridge_table,
        back_populates='colors',
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        """String representation of a Color model."""

        return f'Color | {self.name}'
