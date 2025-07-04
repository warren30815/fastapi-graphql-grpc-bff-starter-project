import strawberry
from .types import UserType, UserInput
from app.grpc.clients.user_service_client import UserServiceClient
from strawberry.types import Info

@strawberry.type
class UserMutations:
    @strawberry.field
    async def create_user(self, user_input: UserInput, info: Info) -> UserType:
        client: UserServiceClient = info.context["user_service_client"]
        user = await client.create_user_from_input(user_input)
        return UserType(
            id=user.id,
            name=user.name,
            email=user.email,
            is_active=user.is_active
        )
