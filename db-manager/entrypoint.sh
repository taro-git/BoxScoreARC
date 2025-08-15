#!/bin/bash
set -e

echo "Waiting for server initialization..."
while [ ! -f /tmp/app_server_ready ]; do
  echo "Waiting for /tmp/app_server_ready..."
  sleep 1
done

echo "Delete flag (/tmp/app_server_ready) file to wait for server initialization"
rm /tmp/app_server_ready

echo "Starting Gunicorn server..."
exec gunicorn box_score_arc.wsgi:application -w 1 --bind 0.0.0.0:8000
