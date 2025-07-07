# User Service

A self-contained microservice responsible for user management operations.

## Features

- User CRUD operations (Create, Read, Update, Delete)
- Email uniqueness validation
- PostgreSQL database with SQLAlchemy ORM
- Database migrations with Alembic
- gRPC server interface
- Independent configuration and deployment

## Configuration

Copy and configure the environment file:
```bash
cp .env.example .env
```

## Database Setup

Create the database:
```sql
CREATE DATABASE user_service;
```

## Running the Service

### Using Start Script
```bash
# Start the server
./start.sh

# Or with specific operations
./start.sh migrate <migration_name>     # Create new migration
./start.sh migrate-deploy               # Deploy migrations with backup
./start.sh restore-db <backup_file>      # Restore from backup
./start.sh reset-db                     # Reset database (destructive)
./start.sh migrate-history              # Show migration history
./start.sh migrate-current              # Show current migration
```

## Development

### Adding New Migrations
```bash
# Using the start script
./start.sh migrate "Description of changes"
./start.sh migrate-deploy
```

### Database Reset
```bash
# Using the start script
./start.sh reset-db
```

### Database Backup & Restore
```bash
# Backup is automatically created during migrate-deploy
./start.sh migrate-deploy

# Manual restore
./start.sh restore-db ./db_backups/backup_20250707_164231.dump
```
