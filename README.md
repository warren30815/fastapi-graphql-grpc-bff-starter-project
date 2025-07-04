# FastAPI GraphQL gRPC Full Stack Project

A full-stack project with a Backend for Frontend (BFF) service built with FastAPI that provides both REST and GraphQL endpoints, with gRPC integration for microservice communication.

## Project Structure

```
├── backend/           # Backend API service
│   ├── app/          # FastAPI application
│   │   ├── api/      # REST API endpoints
│   │   ├── graphql/  # GraphQL schema and resolvers
│   │   ├── grpc/     # gRPC clients and servers
│   │   │   ├── clients/   # gRPC client implementations
│   │   │   ├── servers/   # gRPC server implementations
│   │   │   └── config/    # gRPC configuration
│   │   └── models/   # Data models
│   ├── main.py       # FastAPI server entry point
│   ├── generated/    # Generated protobuf files
│   └── protos/       # Protocol buffer definitions
├── frontend/          # Frontend application (coming soon)
└── README.md         # This file
```

## Features

- **FastAPI** REST endpoints
- **GraphQL** endpoint using Strawberry
- **gRPC** client for microservice communication
- **Async** support throughout
- **UV** package management

## Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
uv sync
```

3. Generate gRPC proto files:
```bash
uv run python scripts/generate_protos.py
```

4. Copy environment variables:
```bash
cp .env.example .env
```

5. Start the User Service gRPC server (in one terminal):
```bash
uv run python app/grpc/servers/user_server.py
```

6. Start the Product Service gRPC server (in another terminal):
```bash
uv run python app/grpc/servers/product_server.py
```

7. Start the FastAPI server (in a third terminal):
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Endpoints

### REST API
- `GET /` - Health check
- `GET /api/users/{user_id}` - Get user by ID
- `POST /api/users` - Create new user
- `GET /api/health` - Health check

### GraphQL
- `POST /graphql` - GraphQL endpoint
- `GET /graphql` - GraphQL playground

## gRPC Client Connection Management

- The BFF (REST and GraphQL) uses **singleton gRPC client instances** for each service. These clients are created once at startup and shared across all requests, both REST and GraphQL.
- All gRPC clients are closed gracefully on FastAPI shutdown via the lifespan handler, ensuring no connection leaks and optimal resource usage. Each client manages its own connection lifecycle and will connect automatically when first used.
- **No per-request gRPC channel creation/teardown**: This design leverages gRPC's built-in HTTP/2 multiplexing, allowing high concurrency and performance with a single channel per service.

## Example GraphQL Queries

```graphql
# Get user
query {
  user(id: 1) {
    id
    name
    email
    isActive
  }
}

# Create user
mutation {
  createUser(userInput: {name: "John Doe", email: "john@example.com"}) {
    id
    name
    email
    isActive
  }
}
```

## Microservices

### User Service (Port 5001)
- Handles user-related operations
- Provides gRPC endpoints for user management
- Default port: 5001 (configurable via `USER_SERVICE_PORT`)

### Product Service (Port 5002)
- Handles product-related operations
- Provides gRPC endpoints for product management
- Default port: 5002 (configurable via `PRODUCT_SERVICE_PORT`)

### BFF Service (Port 8000)
- Backend for Frontend service
- Aggregates microservices via gRPC
- Provides REST and GraphQL endpoints
- Runs on port 8000

## Architecture

- **FastAPI**: Main web framework
- **Strawberry**: GraphQL implementation
- **gRPC**: Microservice communication
- **Pydantic**: Data validation
- **UV**: Package management
