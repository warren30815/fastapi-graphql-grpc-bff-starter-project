from typing import AsyncGenerator
from app.grpc.clients.user_service_client import UserServiceClient
from app.grpc.config.grpc_config import GrpcServicesConfig

# Singleton clients (created once per process)
config = GrpcServicesConfig()
user_client = UserServiceClient(config.user_service_host, config.user_service_port)

async def get_user_service_client_dependency() -> AsyncGenerator[UserServiceClient, None]:
    yield user_client
