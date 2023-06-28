#!/bin/sh
./manage.py makemigrations;
./manage.py migrate;
./manage.py collectstatic --noinput;
gunicorn -w 2 -b 0:8000 foodgram.wsgi --reload