#!/bin/sh
set -e

# Only initialize database for local testing
if [ "$INIT_DB" = "true" ]; then
    echo "Initializing local database..."
    flask init-db || true
else
    echo "Skipping database initialization (expecting external database)"
fi

# Start Flask app
echo "Starting Flask app..."
exec flask run --host=0.0.0.0
