from fastapi import APIRouter

from .user import router as user_router

router = APIRouter()
router.include_router(user_router, prefix="/users")

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
