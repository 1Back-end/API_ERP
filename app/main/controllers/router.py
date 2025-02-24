from fastapi import APIRouter
from .migration_controller import router as migration
from .authentification_controller import router as authentication
from .user_controller import router as user
from .address_controller import router as address
from .storage_controller import router as storage
from .owners_controller import router as owners
from .company_controller import router as company
from .type_abonnement_controller import router as type_abonnement

api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(authentication)
api_router.include_router(user)
api_router.include_router(address)
api_router.include_router(storage)
api_router.include_router(owners)
api_router.include_router(company)
api_router.include_router(type_abonnement)