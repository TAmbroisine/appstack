#!/bin/sh
set -e

# Use provided VITE_API_URL or default to backend-service for Kubernetes
API_URL="${VITE_API_URL:-http://backend-service:5000}"

echo "Setting API URL to: $API_URL"

# Inject API URL into index.html by adding a script tag
sed -i "s|</head>|<script>window.VITE_API_URL='$API_URL';</script></head>|g" /app/dist/index.html

# Start the server
echo "Starting frontend server..."
exec serve -s dist -l 3000
