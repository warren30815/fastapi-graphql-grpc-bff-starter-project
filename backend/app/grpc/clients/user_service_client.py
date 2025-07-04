from typing import List, Optional, Union
from generated import user_pb2
from generated import user_pb2_grpc
from app.models.user import User, UserCreate, UserInput
from app.grpc.clients.base_client import BaseGrpcClient


class UserServiceClient(BaseGrpcClient):
    @property
    def stub_class(self):
        return user_pb2_grpc.UserServiceStub

    def protobuf_to_model(self, proto: user_pb2.User) -> User:
        """Convert single user protobuf to domain model"""
        return User(
            id=proto.id,
            name=proto.name,
            email=proto.email,
            is_active=proto.is_active
        )

    def protobuf_to_model_list(self, protos: List[user_pb2.User]) -> List[User]:
        return [self.protobuf_to_model(user) for user in protos]

    def _create_user_request(self, user_data: Union[UserCreate, UserInput]) -> user_pb2.CreateUserRequest:
        """Helper to create user request from different input types"""
        return user_pb2.CreateUserRequest(
            name=user_data.name,
            email=user_data.email
        )

    async def get_user(self, user_id: int, timeout: Optional[float] = None) -> User:
        request = user_pb2.GetUserRequest(id=user_id)
        return await self.call_with_model("GetUser", request, timeout=timeout)

    async def create_user(self, user_data: UserCreate, timeout: Optional[float] = None) -> User:
        request = self._create_user_request(user_data)
        return await self.call_with_model("CreateUser", request, timeout=timeout)

    async def create_user_from_input(self, user_input: UserInput, timeout: Optional[float] = None) -> User:
        request = self._create_user_request(user_input)
        return await self.call_with_model("CreateUser", request, timeout=timeout)

    async def get_users(
        self,
        limit: int = 10,
        offset: int = 0,
        timeout: Optional[float] = None
    ) -> List[User]:
        request = user_pb2.GetUsersRequest(limit=limit, offset=offset)
        response = await self.call_raw("GetUsers", request, timeout=timeout)
        return self.protobuf_to_model_list(response.users)
