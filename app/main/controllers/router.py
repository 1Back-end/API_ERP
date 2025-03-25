from fastapi import APIRouter
from .migration_controller import router as migration
from .address_controller import router as address
from .authentification_controller import router as auth
from .user_controller import router as user
from .owners_controller import router as owners
from .storage_controller import router as storage
from .company_controller import router as company
from .type_abonnement_controller import router as type_abonnement
from .feature_controller import router as feature
from .abonnement_controller import router as abonnement
# from .renouvellement_controller import router as renouvellement
api_router = APIRouter()

api_router.include_router(migration)
api_router.include_router(auth)
api_router.include_router(address)
api_router.include_router(user)
api_router.include_router(owners)
api_router.include_router(storage)
api_router.include_router(company)
api_router.include_router(type_abonnement)
api_router.include_router(feature)
api_router.include_router(abonnement)
# api_router. include_router(renouvellement)

