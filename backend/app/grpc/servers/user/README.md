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
./start.sh migrate-deploy               # Deploy migrations
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

### Database Backup and Restore
```bash
# Create a database backup
./backup.sh backup

# List available backups
./backup.sh list

# Restore from a backup
./backup.sh restore ./db_backups/backup_20250806_085512.dump
```
