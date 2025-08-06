#!/bin/bash
# Database backup utility for User service

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
  backup)
    echo "🧰 Creating database backup..."

    TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
    BACKUP_DIR="./db_backups"
    BACKUP_FILE="$BACKUP_DIR/backup_${TIMESTAMP}.dump"

    mkdir -p "$BACKUP_DIR"

    echo "🧰 Backing up database to $BACKUP_FILE..."
    PGPASSWORD="$USER_DB_PASSWORD" pg_dump -U "$USER_DB_USER" -h "$USER_DB_HOST" -p "$USER_DB_PORT" -d "$USER_DB_NAME" -F c -f "$BACKUP_FILE"

    if [ $? -ne 0 ]; then
      echo "❌ Database backup failed."
      exit 1
    fi

    echo "✅ Database backup completed: $BACKUP_FILE"
    ;;

  restore)
    echo "♻️  Restoring database from backup..."

    if [ -z "$2" ]; then
      echo "Usage: ./backup.sh restore <backup_file.dump>"
      exit 1
    fi

    BACKUP_FILE="$2"

    if [ ! -f "$BACKUP_FILE" ]; then
      echo "❌ Backup file not found: $BACKUP_FILE"
      exit 1
    fi

    echo "🧨 Dropping and recreating database '$USER_DB_NAME'..."
    PGPASSWORD="$USER_DB_PASSWORD" dropdb -U "$USER_DB_USER" -h "$USER_DB_HOST" -p "$USER_DB_PORT" "$USER_DB_NAME"
    if [ $? -ne 0 ]; then
      echo "❌ Failed to drop database. Aborting restore."
      exit 1
    fi

    PGPASSWORD="$USER_DB_PASSWORD" createdb -U "$USER_DB_USER" -h "$USER_DB_HOST" -p "$USER_DB_PORT" "$USER_DB_NAME"
    if [ $? -ne 0 ]; then
      echo "❌ Failed to create database. Aborting restore."
      exit 1
    fi

    echo "🔁 Restoring from $BACKUP_FILE..."
    PGPASSWORD="$USER_DB_PASSWORD" pg_restore -U "$USER_DB_USER" -h "$USER_DB_HOST" -p "$USER_DB_PORT" -d "$USER_DB_NAME" "$BACKUP_FILE"

    if [ $? -ne 0 ]; then
      echo "❌ Database restore failed."
      exit 1
    fi

    echo "✅ Restore complete."
    ;;

  list)
    echo "📋 Available backups:"
    BACKUP_DIR="./db_backups"
    if [ -d "$BACKUP_DIR" ]; then
      ls -la "$BACKUP_DIR"/*.dump 2>/dev/null || echo "No backup files found."
    else
      echo "No backup directory found."
    fi
    ;;

  *)
    echo "Database Backup Utility for User Service"
    echo ""
    echo "Usage: ./backup.sh <command> [options]"
    echo ""
    echo "Commands:"
    echo "  backup                    Create a database backup"
    echo "  restore <backup_file>     Restore from a backup file"
    echo "  list                      List available backup files"
    echo ""
    echo "Examples:"
    echo "  ./backup.sh backup                              # Create backup"
    echo "  ./backup.sh restore ./db_backups/backup_*.dump  # Restore from backup"
    echo "  ./backup.sh list                                # List backups"
    ;;
esac
