# FastAPI GraphQL gRPC Microservices Project

A microservices architecture project with a Backend for Frontend (BFF) service built with FastAPI that provides both REST and GraphQL endpoints, with gRPC communication between independent microservices.

## Architecture

### Tech Stack
- **FastAPI**: Main BFF web framework
- **Strawberry**: GraphQL implementation
- **gRPC**: Microservice communication protocol
- **PostgreSQL**: Database for each microservice
- **SQLAlchemy**: ORM with separate databases per service
- **Alembic**: Database migrations per service
- **Pydantic**: Data validation
- **UV**: Package management

### Microservices Design
Each microservice is completely self-contained with:
- Independent database and schema
- Own migration system (Alembic)
- Separate configuration and environment variables
- Individual deployment capability
- Internal database implementation hidden from clients

## Database Setup

Each microservice requires its own PostgreSQL database:

```sql
-- Create databases for each service
CREATE DATABASE user_service;

-- Optional: Create separate users for each service
CREATE USER user_service_user WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE user_service TO user_service_user;
```

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

4. Configure each microservice:
```bash
# Copy environment files for each service
cp app/grpc/servers/user/.env.example app/grpc/servers/user/.env

# Edit the .env files with your database credentials
```

5. Run database migrations for each service:
```bash
# User service migrations
cd app/grpc/servers/user
# sync db schema
sh ./start.sh sync
```

6. Start the microservices:
```bash
# Terminal 1: User Service
cd app/grpc/servers/user
sh ./start.sh

# Terminal 2: BFF Service (from backend directory)
sh ./start.sh {dev|prod}
```

## Swagger API Docs

Visit `/docs`

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
- **Purpose**: Handles user-related operations
- **Database**: Independent PostgreSQL database (`user_service`)
- **Port**: 5001 (configurable via `USER_SERVICE_PORT`)
- **Location**: `app/grpc/servers/user/`
- **Features**:
  - User CRUD operations
  - Email uniqueness validation
  - Separate Alembic migrations
  - Independent database schema
  - Self-contained configuration

### BFF Service (Port 8000)
- **Purpose**: Backend for Frontend service
- **Responsibilities**: Aggregates microservices via gRPC
- **Endpoints**: REST and GraphQL APIs
- **Port**: 8000
- **Features**:
  - Service orchestration
  - API gateway functionality
  - Singleton gRPC client management
  - Request/response transformation
