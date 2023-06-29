FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -U pip &&\
    pip install -r requirements.txt --no-cache-dir
COPY . .
CMD gunicorn -w 2 -b 0:8000 foodgram.wsgi --reload