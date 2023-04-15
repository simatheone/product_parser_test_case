from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.router import router as product_router

app = FastAPI()

app.include_router(product_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOW_ORIGINS,
    allow_methods=(
        'HEAD',
        'OPTIONS',
        'GET',
        'POST',
        'DELETE',
        'PATCH',
    ),
    allow_headers=('*'),
)
