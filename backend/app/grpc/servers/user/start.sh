#!/bin/bash
# Start User gRPC server

# Load environment variables if .env file exists
if [ -f .env ]; then
  set -a
  . .env
  set +a
elif [ -f .env.example ]; then
  set -a
  . .env.example
  set +a
fi

# Main logic
case "$1" in
  migrate)
    echo "🔄 Creating database migration..."
    if [ -z "$2" ]; then
      echo "Usage: ./start.sh migrate <migration_name>"
      echo "Example: ./start.sh migrate initial_schema"
      exit 1
    fi
    alembic revision --autogenerate -m "$2"
    echo "✅ Database migration '$2' created."
    ;;

  migrate-deploy)
    echo "🔄 Deploying pending migrations to production..."
    alembic upgrade head
    echo "✅ Production migrations deployed."
    ;;

  reset-db)
    echo "⚠️  Resetting database and applying all migrations..."
    read -p "This will DELETE ALL DATA. Continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      PGPASSWORD="$USER_DB_PASSWORD" dropdb -U "$USER_DB_USER" -h "$USER_DB_HOST" -p "$USER_DB_PORT" "$USER_DB_NAME"
      if [ $? -ne 0 ]; then
        echo "❌ Failed to drop database. Aborting reset."
        exit 1
      fi
      PGPASSWORD="$USER_DB_PASSWORD" createdb -U "$USER_DB_USER" -h "$USER_DB_HOST" -p "$USER_DB_PORT" "$USER_DB_NAME"
      if [ $? -ne 0 ]; then
        echo "❌ Failed to create database. Aborting reset."
        exit 1
      fi
      alembic upgrade head
      echo "✅ Database reset completed."
    else
      echo "❌ Migration reset cancelled."
    fi
    ;;

  migrate-history)
    echo "📜 Showing migration history..."
    alembic history --verbose
    ;;

  migrate-current)
    echo "📍 Showing current migration..."
    alembic current
    ;;

  sync)
    echo "🔄 Syncing database schema (alembic upgrade head)..."
    alembic upgrade head
    echo "✅ Database schema synced."
    ;;

  *)
    echo "🚀 Starting User gRPC server..."
    uv run python user_server.py &
    USER_GRPC_PID=$!
    echo "🚀 User gRPC Server started with PID: $USER_GRPC_PID"
    echo "Server listening on port ${USER_SERVICE_PORT:-5001}"
    wait "$USER_GRPC_PID"
    ;;
esac
