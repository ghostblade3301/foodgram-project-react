FROM python:3.9-slim
RUN apt update &&\
    apt upgrade -y &&\
    apt install -y libpq-dev gcc netcat
WORKDIR /app
COPY requirements.txt .
RUN pip install -U pip &&\
    pip install -r requirements.txt --no-cache-dir
COPY . .
RUN chmod +x run_app.sh
ENTRYPOINT [ "/app/run_app.sh" ]