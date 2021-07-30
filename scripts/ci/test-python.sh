#!/bin/sh

mkdir ./logs
venv/bin/python manage.py makemigrations
venv/bin/python manage.py migrate
venv/bin/python manage.py test