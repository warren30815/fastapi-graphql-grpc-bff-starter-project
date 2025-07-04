import strawberry
from app.graphql.user.queries import UserQueries
from app.graphql.user.mutations import UserMutations
from app.graphql.product.queries import ProductQueries
from app.graphql.product.mutations import ProductMutations

@strawberry.type
class Query(UserQueries, ProductQueries):
    pass

@strawberry.type
class Mutation(UserMutations, ProductMutations):
    pass

schema = strawberry.Schema(query=Query, mutation=Mutation)
