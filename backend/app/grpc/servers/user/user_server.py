import grpc
from concurrent import futures
import logging
from typing import Dict, List
import os

from generated import user_pb2
from generated import user_pb2_grpc
from app.grpc.servers.interceptors import LoggingInterceptor
from app.grpc.servers.graceful_server import GracefulGRPCServer
from .database.connection import get_user_db_session
from .database.models import User
from sqlalchemy.exc import IntegrityError


class UserServiceServicer(user_pb2_grpc.UserServiceServicer):
    def __init__(self):
        pass

    def GetUser(self, request, context):
        with get_user_db_session() as db:
            user = db.query(User).filter(User.id == request.id).first()
            if not user:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("User not found")
                return user_pb2.User()

            return user_pb2.User(
                id=user.id,
                name=user.name,
                email=user.email,
                is_active=user.is_active
            )

    def CreateUser(self, request, context):
        with get_user_db_session() as db:
            try:
                db_user = User(
                    name=request.name,
                    email=request.email,
                    is_active=True
                )
                db.add(db_user)
                db.flush()

                return user_pb2.User(
                    id=db_user.id,
                    name=db_user.name,
                    email=db_user.email,
                    is_active=db_user.is_active
                )
            except IntegrityError:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details("User with this email already exists")
                return user_pb2.User()

    def GetUsers(self, request, context):
        with get_user_db_session() as db:
            query = db.query(User)

            if request.limit > 0:
                query = query.offset(request.offset).limit(request.limit)

            users = query.all()

            pb_users = [
                user_pb2.User(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    is_active=user.is_active
                )
                for user in users
            ]

            return user_pb2.GetUsersResponse(users=pb_users)


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
