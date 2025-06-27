#!/bin/bash
gunicorn project_box_score_arc.wsgi:application -w 4 --bind 0.0.0.0:8000
