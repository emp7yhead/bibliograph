FROM python:3.11-alpine AS builder

WORKDIR /code

RUN apk add --no-cache gcc \
    musl-dev \
    make \
    libffi-dev \
    openssl-dev

ADD pyproject.toml poetry.lock /code/

RUN pip install poetry

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# ---

FROM python:3.11-alpine

WORKDIR /app

COPY --from=builder /code/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN adduser -D user && chown -R user:user ./

USER user

COPY --chown=user:user ./ ./

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
