import grpc
from concurrent import futures
import logging
from typing import Dict, List
import os

from generated import user_pb2
from generated import user_pb2_grpc
from app.grpc.servers.interceptors import LoggingInterceptor
from app.grpc.servers.graceful_server import GracefulGRPCServer


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.users: Dict[int, user_pb2.User] = {
            1: user_pb2.User(id=1, name="John Doe", email="john@example.com", is_active=True),
            2: user_pb2.User(id=2, name="Jane Smith", email="jane@example.com", is_active=True),
        }
        self.next_id = 3

    def GetUser(self, request, context):
        user = self.users.get(request.id)
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return user_pb2.User()
        return user

    def CreateUser(self, request, context):
        user = user_pb2.User(
            id=self.next_id,
            name=request.name,
            email=request.email,
            is_active=True
        )
        self.users[self.next_id] = user
        self.next_id += 1
        return user

    def GetUsers(self, request, context):
        users = list(self.users.values())
        if request.limit > 0:
            users = users[request.offset:request.offset + request.limit]
        return user_pb2.GetUsersResponse(users=users)


def serve():
    port = int(os.getenv("USER_SERVICE_PORT", "5001"))
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[LoggingInterceptor()]
    )
    user_pb2_grpc.add_UserServiceServicer_to_server(UserServiceServicer(), server)
    listen_addr = f'[::]:{port}'
    server.add_insecure_port(listen_addr)

    logging.info(f"Starting User gRPC server on {listen_addr}")
    GracefulGRPCServer(server, name="User gRPC server").start_and_wait()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
