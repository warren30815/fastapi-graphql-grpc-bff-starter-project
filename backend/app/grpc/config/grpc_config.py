from dataclasses import dataclass
import os

@dataclass
class GrpcServicesConfig:
    user_service_host: str = os.getenv("USER_SERVICE_HOST", "localhost")
    user_service_port: int = int(os.getenv("USER_SERVICE_PORT", "5001"))
    product_service_host: str = os.getenv("PRODUCT_SERVICE_HOST", "localhost")
    product_service_port: int = int(os.getenv("PRODUCT_SERVICE_PORT", "5002"))
