#!/bin/bash
set -e

echo "Wait for PostgreSQL to become available..."
python /app/box_score_arc/wait_for_postgres.py

echo "Creating super user"
python create_superuser.py

echo "Removing old migrations"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
echo "Making migrations"
python manage.py migrate --fake data_collector zero
python manage.py migrate --fake rest_api zero
python manage.py makemigrations

echo "Applying database migrations..."
python manage.py migrate --noinput

if [ -d "/app/staticfiles" ]; then
    echo "Removing old staticfiles directory..."
    rm -rf /app/staticfiles
fi
echo "Collecting static files"
python manage.py collectstatic

echo "Starting Gunicorn server..."
exec python manage.py runserver 0.0.0.0:8000
