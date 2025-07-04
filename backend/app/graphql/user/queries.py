import strawberry
from typing import List
from .types import UserType
from app.grpc.clients.user_service_client import UserServiceClient
from strawberry.types import Info

@strawberry.type
class UserQueries:
    @strawberry.field
    async def user(self, id: int, info: Info) -> UserType:
        client: UserServiceClient = info.context["user_service_client"]
        try:
            user = await client.get_user(id)
        except Exception:
            raise strawberry.exceptions.GraphQLError("User not found")
        if not user:
            raise strawberry.exceptions.GraphQLError("User not found")
        return UserType(
            id=user.id,
            name=user.name,
            email=user.email,
            is_active=user.is_active
        )

    @strawberry.field
    async def users(self, info: Info) -> List[UserType]:
        client: UserServiceClient = info.context["user_service_client"]
        users = await client.get_users()
        return [
            UserType(
                id=user.id,
                name=user.name,
                email=user.email,
                is_active=user.is_active
            )
            for user in users
        ]
