#!/bin/bash
gunicorn api_project.wsgi:application -w 4 --bind 0.0.0.0:8000
