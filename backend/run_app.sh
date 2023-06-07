#!/bin/sh
./manage.py migrate;
./manage.py collectstatic --noinput;
gunicorn -b 0:8000 foodgram.wsgi