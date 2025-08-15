#!/bin/bash
set -e

echo "Wait for PostgreSQL to become available..."
python /app/box_score_arc/wait_for_postgres.py

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "done" > /tmp/app_server_ready

echo "Starting Gunicorn server..."
export START_EPOCH=$(date +%s)
exec gunicorn box_score_arc.wsgi:application -w 4 --bind 0.0.0.0:8000
