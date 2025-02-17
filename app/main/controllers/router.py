from fastapi import APIRouter
from .migration_controller import router as migration
from .user_controller import router as user
from .address_controller import router as address
from .storage_controller import router as storage

api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(user)
api_router.include_router(address)
api_router.include_router(storage)