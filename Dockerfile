FROM python:3.13.0-alpine3.20 as base

ENV DIR=/app
WORKDIR $DIR


# DEVELOPMENT
FROM base as dev

ENV PYTHON_ENV=development

RUN apk update && apk upgrade
COPY requirements.txt .
COPY requirements-dev.txt .

RUN pip install -r requirements-dev.txt && pip install -r requirements.txt
COPY . .

EXPOSE $PORT
CMD ["fastapi", "run", "app/main.py"]


# PRODUCTION
FROM base as production

ENV PYTHON_ENV=production

RUN apk update && apk upgrade
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE $PORT
CMD ["fastapi", "run", "app/main.py"]
