# pull official base image
FROM python:3.12-alpine

# set work directory
WORKDIR /usr/src/backend

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# just testing purpose
ENV DATABASE_URL=postgresql://company_manager:company_manager@db/company_manager_dev

# copy requirements file
COPY ./requirements.txt /usr/src/backend/requirements.txt

# install dependencies
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
    openssl-dev libffi-dev gcc musl-dev python3-dev \
    postgresql-dev bash \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /usr/src/backend/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY . /usr/src/backend/

EXPOSE 8002

CMD ["uvicorn", "api.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "8002"]