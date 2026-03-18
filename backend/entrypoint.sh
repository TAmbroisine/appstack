#!/bin/sh
set -e

# Only initialize database for local testing with SQLite
if [ "$INIT_DB" = "true" ] && [ -z "$DB_HOST" ]; then
    echo "Initializing SQLite database..."
    flask init-db || true
elif [ "$INIT_DB" = "true" ] && [ ! -z "$DB_HOST" ]; then
    echo "Skipping init-db for PostgreSQL (use migrations instead)"
else
    echo "Skipping database initialization"
fi

# Start Flask app
echo "Starting Flask app..."
exec flask run --host=0.0.0.0
