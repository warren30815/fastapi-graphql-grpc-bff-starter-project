from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.graphql.context_factory import get_context
from app.restful.routes import router as api_router
from app.grpc.clients.base_client import BaseGrpcClient
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    yield
    await BaseGrpcClient.cleanup_all()

app = FastAPI(title="FastAPI GraphQL gRPC BFF", version="0.1.0", lifespan=lifespan)

# GraphQL endpoint
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

# REST API endpoints
app.include_router(api_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "FastAPI GraphQL gRPC BFF is running"}
