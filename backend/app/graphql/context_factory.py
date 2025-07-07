from app.grpc.clients.user_service_client import UserServiceClient
from app.grpc.config.grpc_config import GrpcServicesConfig

# Singleton clients (created once per process)
config = GrpcServicesConfig()
user_client = UserServiceClient(config.user_service_host, config.user_service_port)

async def get_context():
    return {
        "user_service_client": user_client
    }
