from typing import Any

from fastapi import HTTPException, status

from src.constants import ErrorCodes


class DetailedHTTPException(HTTPException):
    """Base Detailed Exception for inheritance.
    Status code 500 Internal server error.
    """

    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = ErrorCodes.SERVER_ERROR

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class NotFound(DetailedHTTPException):
    """Default Exception for status code 404 Not Found."""

    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = ErrorCodes.NOT_FOUND


class BadRequest(DetailedHTTPException):
    """Default Exception for status code 400 Bad Request."""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = ErrorCodes.BAD_REQUEST


class ProductAlreadyExists(BadRequest):
    """Exception for the case when Product already exists."""

    DETAIL = ErrorCodes.PRODUCT_ALREADY_EXISTS


class ProductDoesNotExist(NotFound):
    """Exception for the case when Product does not exist."""

    DETAIL = ErrorCodes.PRODUCT_DOES_NOT_EXIST


class ProductNotFound(NotFound):
    """Exception for the case when Product is not found."""

    DETAIL = ErrorCodes.PRODUCT_NOT_FOUND


class SomethingWentWrong(BadRequest):
    """Exception for the case when on request to website response
    status code differs from 200.
    """

    DETAIL = ErrorCodes.SMTH_WENT_WRONG
