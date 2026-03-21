from fastapi import APIRouter
from app.api.v1.endpoints import word
from app.api.v1.endpoints import auth

api_router = APIRouter()

api_router.include_router(word.router, tags=["Word"])

api_router.include_router(auth.router, tags=["Auth"])