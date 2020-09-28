#!/bin/bash
	source /home/mamzin/code/tm_project_django/venv/bin/activate
	exec gunicorn  -c "/home/mamzin/code/tm_project_django/gunicorn_config.py" tm_project_django.wsgi

