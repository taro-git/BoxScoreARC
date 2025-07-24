#!/bin/bash
set -e

echo "Wait for PostgreSQL to become available..."
python /app/box_score_arc/wait_for_postgres.py

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn server..."
exec python manage.py runserver 0.0.0.0:8000
