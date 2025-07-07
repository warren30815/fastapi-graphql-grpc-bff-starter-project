#!/bin/bash
# Start API server or development mode

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

# Cleanup function
cleanup() {
  echo "Cleaning up..."
  [[ -n "$SERVER_PID" ]] && kill "$SERVER_PID" 2>/dev/null && echo "🔴 API Server (PID: $SERVER_PID) stopped."
  wait "$SERVER_PID" 2>/dev/null
  echo "✅ Cleanup done."
  exit 0
}

# Trap signals
trap cleanup SIGINT SIGTERM SIGHUP

# Main logic
case "$1" in
  docker)
    docker-compose up -d
    echo "Started Docker services. Monitor logs with 'docker-compose logs -f'"
    ;;

  dev)
    echo "🚀 Starting API server in development mode with hot reload..."
    uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
    SERVER_PID=$!
    echo "🚀 Dev API Server (PID: $SERVER_PID) started."
    wait
    ;;

  prod)
    echo "🚀 Starting API server..."
    uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1 --limit-concurrency 1000 &
    SERVER_PID=$!
    echo "🚀 Prod API Server (PID: $SERVER_PID) started."
    wait
    ;;

  *)
    echo "Usage: ./start.sh [dev|prod|docker]"
    echo "  dev    - Start API server in development mode (hot reload)"
    echo "  prod   - Start API server in production mode"
    echo "  docker - Start Docker services via docker-compose"
    exit 1
    ;;
esac
