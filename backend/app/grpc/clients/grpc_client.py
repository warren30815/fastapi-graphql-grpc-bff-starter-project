from typing import AsyncGenerator
from app.grpc.clients.user_service_client import UserServiceClient
from app.grpc.clients.product_service_client import ProductServiceClient
from app.grpc.config.grpc_config import GrpcServicesConfig

# Singleton clients (created once per process)
config = GrpcServicesConfig()
user_client = UserServiceClient(config.user_service_host, config.user_service_port)
product_client = ProductServiceClient(config.product_service_host, config.product_service_port)

async def get_user_service_client_dependency() -> AsyncGenerator[UserServiceClient, None]:
    yield user_client

async def get_product_service_client_dependency() -> AsyncGenerator[ProductServiceClient, None]:
    yield product_client
