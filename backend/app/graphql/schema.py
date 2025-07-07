import strawberry
from app.graphql.user.queries import UserQueries
from app.graphql.user.mutations import UserMutations

@strawberry.type
class Query(UserQueries):
    pass

@strawberry.type
class Mutation(UserMutations):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
