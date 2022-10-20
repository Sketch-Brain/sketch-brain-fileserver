FROM hhlee7175/sketchbrain-file-server-base:v1.0

RUN mkdir /app
WORKDIR /app

COPY . .

CMD gunicorn -k uvicorn.workers.UvicornWorker -c gunicorn_config.py main:app
