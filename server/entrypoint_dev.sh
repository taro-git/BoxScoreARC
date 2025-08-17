#!/bin/bash
set -e

echo "Wait for PostgreSQL to become available..."
python /app/box_score_arc/wait_for_postgres.py

echo "Making migrations"
python manage.py makemigrations --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Creating super user"
python create_superuser.py

if [ -d "/app/staticfiles" ]; then
    echo "Removing old staticfiles directory..."
    rm -rf /app/staticfiles
fi
echo "Collecting static files"
python manage.py collectstatic

echo "done" > /tmp/app_server_ready

echo "Starting Gunicorn server..."
export START_EPOCH=$(date +%s)
exec python manage.py runserver 0.0.0.0:8000
