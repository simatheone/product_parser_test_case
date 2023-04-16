from pydantic import BaseModel, Field, NonNegativeInt


class ORMMode(BaseModel):
    """Base model with set orm_mode."""

    class Config:
        orm_mode = True


class ColorBase(BaseModel):
    """Base Color schema."""

    color_id: int
    name: str


class Color(ColorBase):
    """Scheme for creating/getting a new color."""

    color_id: int
    name: str = Field(..., max_length=64)


class ColorResponse(ColorBase, ORMMode):
    """Response Color schema."""


class ProductBase(BaseModel):
    """Base Product schema."""

    nm_id: NonNegativeInt
    name: str
    brand: str
    brand_id: NonNegativeInt
    site_brand_id: NonNegativeInt
    supplier_id: NonNegativeInt
    sale: NonNegativeInt
    price: NonNegativeInt
    sale_price: NonNegativeInt
    rating: NonNegativeInt
    feedbacks: NonNegativeInt
    quantity: NonNegativeInt
    colors: list[ColorResponse] | None


class ProductCreate(ProductBase):
    """Scheme for creating a new product."""

    nm_id: NonNegativeInt
    name: str = Field(..., max_length=256)
    brand: str = Field(..., max_length=256)
    sale: NonNegativeInt = Field(default=0, exclusiveMaximum=100)
    rating: NonNegativeInt = Field(default=0, exclusiveMaximum=5)
    feedbacks: NonNegativeInt = Field(default=0)
    colors: list[Color] = []
    quantity: NonNegativeInt = Field(default=0)


class ProductResponse(ProductBase, ORMMode):
    """Response Product schema."""

    class Config:
        schema_extra = {
            'example': {
                'nm_id': 111,
                'name': 'Пуловер',
                'brand': 'Y.O.U',
                'brand_id': 987,
                'site_brand_id': 439,
                'supplier_id': 458,
                'sale': 0,
                'price': 105000,
                'sale_price': 105000,
                'rating': 0,
                'feedbacks': 0,
                'quantity': 0,
                'colors': [{'color_id': 1, 'name': 'коричневый'}],
            }
        }


class ProductRequest(BaseModel):
    """Request Product schema."""

    nm_id: NonNegativeInt

    class Config:
        schema_extra = {
            'example': {'nm_id': 139760619},
        }
