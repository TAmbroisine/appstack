#!/bin/sh
set -e

# Initialize database if flag is set
if [ "$INIT_DB" = "true" ]; then
    echo "Initializing database..."
    flask init-db || true
else
    echo "Skipping database initialization"
fi

# Start Flask app
echo "Starting Flask app..."
exec flask run --host=0.0.0.0
