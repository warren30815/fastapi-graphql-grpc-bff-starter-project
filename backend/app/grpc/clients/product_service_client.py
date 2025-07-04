from typing import List, Optional
from generated import product_pb2
from generated import product_pb2_grpc
from app.models.product import Product, ProductCreate, ProductUpdate
from app.grpc.clients.base_client import BaseGrpcClient


class ProductServiceClient(BaseGrpcClient):
    @property
    def stub_class(self):
        return product_pb2_grpc.ProductServiceStub

    def protobuf_to_model(self, proto: product_pb2.Product) -> Product:
        """Convert single product protobuf to domain model"""
        return Product(
            id=proto.id,
            name=proto.name,
            description=proto.description,
            price=proto.price,
            stock=proto.stock,
            category=proto.category,
            is_active=proto.is_active
        )

    def protobuf_to_model_list(self, protos: List[product_pb2.Product]) -> List[Product]:
        return [self.protobuf_to_model(product) for product in protos]

    def _create_product_request(self, product_data: ProductCreate) -> product_pb2.CreateProductRequest:
        return product_pb2.CreateProductRequest(
            name=product_data.name,
            description=product_data.description or "",
            price=product_data.price,
            stock=product_data.stock,
            category=product_data.category or ""
        )

    def _update_product_request(self, product_id: int, product_data: ProductUpdate) -> product_pb2.UpdateProductRequest:
        return product_pb2.UpdateProductRequest(
            id=product_id,
            name=product_data.name or "",
            description=product_data.description or "",
            price=product_data.price or 0.0,
            stock=product_data.stock or 0,
            category=product_data.category or ""
        )

    async def get_product(self, product_id: int, timeout: Optional[float] = None) -> Product:
        request = product_pb2.GetProductRequest(id=product_id)
        return await self.call_with_model("GetProduct", request, timeout=timeout)

    async def create_product(self, product_data: ProductCreate, timeout: Optional[float] = None) -> Product:
        request = self._create_product_request(product_data)
        return await self.call_with_model("CreateProduct", request, timeout=timeout)

    async def update_product(self, product_id: int, product_data: ProductUpdate, timeout: Optional[float] = None) -> Product:
        request = self._update_product_request(product_id, product_data)
        return await self.call_with_model("UpdateProduct", request, timeout=timeout)

    async def delete_product(self, product_id: int, timeout: Optional[float] = None) -> bool:
        request = product_pb2.DeleteProductRequest(id=product_id)
        response = await self.call_raw("DeleteProduct", request, timeout=timeout)
        return response.success

    async def get_products(
        self,
        limit: int = 10,
        offset: int = 0,
        category: Optional[str] = None,
        timeout: Optional[float] = None
    ) -> List[Product]:
        request = product_pb2.GetProductsRequest(
            limit=limit,
            offset=offset,
            category=category or ""
        )
        response = await self.call_raw("GetProducts", request, timeout=timeout)
        return self.protobuf_to_model_list(response.products)
