FROM python:3.11.3-alpine3.17

WORKDIR /app

RUN apk add --no-cache gcc \
    musl-dev \
    make \
    libffi-dev \
    openssl-dev

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --no-root

COPY . .

CMD ["make", "serve"]
