from fastapi import APIRouter
from app.routers.user import user_router
from app.routers.auth import auth_router

router = APIRouter(prefix="/api/v1")
router.include_router(user_router)
router.include_router(auth_router)