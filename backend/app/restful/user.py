from fastapi import APIRouter, Depends
from app.grpc.clients.grpc_client import get_user_service_client_dependency
from app.models.user import User, UserCreate
from app.grpc.clients.user_service_client import UserServiceClient

router = APIRouter()

@router.get("/{user_id}")
async def get_user(user_id: int, client: UserServiceClient = Depends(get_user_service_client_dependency)) -> User:
    return await client.get_user(user_id)

@router.post("")
async def create_user(user: UserCreate, client: UserServiceClient = Depends(get_user_service_client_dependency)) -> User:
    return await client.create_user(user)
