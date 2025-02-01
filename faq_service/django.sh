#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# # Start Django server
# echo "Starting Django server..."
# exec "$@"
