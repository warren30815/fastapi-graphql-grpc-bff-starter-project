import grpc
from concurrent import futures
import logging
from typing import Dict, List
import os

from generated import product_pb2
from generated import product_pb2_grpc
from app.grpc.servers.interceptors import LoggingInterceptor
from app.grpc.servers.graceful_server import GracefulGRPCServer


class ProductServiceServicer(product_pb2_grpc.ProductServiceServicer):
    def __init__(self):
        self.products: Dict[int, product_pb2.Product] = {
            1: product_pb2.Product(
                id=1,
                name="Laptop",
                description="High-performance laptop",
                price=999.99,
                stock=10,
                category="Electronics",
                is_active=True
            ),
            2: product_pb2.Product(
                id=2,
                name="Coffee Mug",
                description="Ceramic coffee mug",
                price=15.99,
                stock=50,
                category="Home",
                is_active=True
            ),
        }
        self.next_id = 3

    def GetProduct(self, request, context):
        product = self.products.get(request.id)
        if not product:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.Product()
        return product

    def CreateProduct(self, request, context):
        product = product_pb2.Product(
            id=self.next_id,
            name=request.name,
            description=request.description,
            price=request.price,
            stock=request.stock,
            category=request.category,
            is_active=True
        )
        self.products[self.next_id] = product
        self.next_id += 1
        return product

    def UpdateProduct(self, request, context):
        product = self.products.get(request.id)
        if not product:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Product not found")
            return product_pb2.Product()

        # Update only provided fields
        if request.name:
            product.name = request.name
        if request.description:
            product.description = request.description
        if request.price > 0:
            product.price = request.price
        if request.stock >= 0:
            product.stock = request.stock
        if request.category:
            product.category = request.category

        return product

    def DeleteProduct(self, request, context):
        if request.id in self.products:
            del self.products[request.id]
            return product_pb2.DeleteProductResponse(success=True, message="Product deleted successfully")
        else:
            return product_pb2.DeleteProductResponse(success=False, message="Product not found")

    def GetProducts(self, request, context):
        products = list(self.products.values())

        # Filter by category if provided
        if request.category:
            products = [p for p in products if p.category == request.category]

        # Apply pagination
        if request.limit > 0:
            products = products[request.offset:request.offset + request.limit]

        return product_pb2.GetProductsResponse(products=products)


def serve():
    port = int(os.getenv("PRODUCT_SERVICE_PORT", "5002"))
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[LoggingInterceptor()]
    )
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductServiceServicer(), server)
    listen_addr = f'[::]:{port}'
    server.add_insecure_port(listen_addr)

    logging.info(f"Starting Product gRPC server on {listen_addr}")
    GracefulGRPCServer(server, name="Product gRPC server").start_and_wait()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
