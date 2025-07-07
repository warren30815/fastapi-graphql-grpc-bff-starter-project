from fastapi import APIRouter, Depends, HTTPException
from app.grpc.clients.grpc_client import get_user_service_client_dependency
from app.models.user import User, UserCreate
from app.grpc.clients.user_service_client import UserServiceClient
import grpc

router = APIRouter()

@router.get("/{user_id}")
async def get_user(user_id: int, client: UserServiceClient = Depends(get_user_service_client_dependency)) -> User:
    try:
        return await client.get_user(user_id)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.code().name} - {e.details()}")

@router.post("")
async def create_user(user: UserCreate, client: UserServiceClient = Depends(get_user_service_client_dependency)) -> User:
    try:
        return await client.create_user(user)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.code().name} - {e.details()}")

@router.get("")
async def get_users(limit: int = 10, offset: int = 0, client: UserServiceClient = Depends(get_user_service_client_dependency)) -> list[User]:
    try:
        return await client.get_users(limit=limit, offset=offset)
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"gRPC error: {e.code().name} - {e.details()}")
