# User Service

A self-contained microservice responsible for user management operations.

## Features

- User CRUD operations (Create, Read, Update, Delete)
- Email uniqueness validation
- PostgreSQL database with SQLAlchemy ORM
- Database migrations with Alembic
- gRPC server interface
- Independent configuration and deployment

## Database Schema

### User Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE ON UPDATE CURRENT_TIMESTAMP
);
```

## Configuration

Copy and configure the environment file:
```bash
cp .env.example .env
```

## Database Setup

1. Create the database:
```sql
CREATE DATABASE user_service;
```

2. Run migrations:
```bash
alembic -c alembic_user_service.ini revision --autogenerate -m "Initial migration"
alembic -c alembic_user_service.ini upgrade head
```

3. Seed data (optional):
```bash
python seed_user_data.py
```

## Running the Service

```bash
# From the user service directory
python user_server.py

# Or from the backend root
uv run python app/grpc/servers/user/user_server.py
```

## Development

### Adding New Migrations
```bash
dotenv -f .env -- alembic -c alembic_user_service.ini revision --autogenerate -m "Description of changes"
dotenv -f .env -- alembic -c alembic_user_service.ini upgrade head
```

### Database Reset
```bash
# Drop and recreate database
dotenv -f .env -- alembic -c alembic_user_service.ini downgrade base
dotenv -f .env -- alembic -c alembic_user_service.ini upgrade head
```

## Deployment

This service can be deployed independently as a Docker container or standalone process. It only requires:
- PostgreSQL database connection
- Environment configuration
- Network access on the configured port
