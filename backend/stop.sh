#!/bin/bash
# Stop running processes

echo "🔍 Looking for running processes..."

# Find and kill uvicorn processes
UVICORN_PIDS=$(pgrep -f "uvicorn.*main:app" 2>/dev/null)
if [ -n "$UVICORN_PIDS" ]; then
  echo "🔴 Stopping uvicorn processes: $UVICORN_PIDS"
  echo "$UVICORN_PIDS" | xargs kill -TERM 2>/dev/null
  sleep 2

  # Force kill if still running
  REMAINING_PIDS=$(pgrep -f "uvicorn.*main:app" 2>/dev/null)
  if [ -n "$REMAINING_PIDS" ]; then
    echo "🔴 Force killing remaining processes: $REMAINING_PIDS"
    echo "$REMAINING_PIDS" | xargs kill -KILL 2>/dev/null
  fi
else
  echo "✅ No uvicorn processes found."
fi

echo "✅ Cleanup completed."
