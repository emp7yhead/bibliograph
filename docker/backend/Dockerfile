FROM python:3.11.3-alpine3.17

WORKDIR /app

RUN apk add --no-cache gcc \
    musl-dev \
    make \
    libffi-dev \
    openssl-dev

ADD requirements.lock ./

RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.lock

ADD . .

CMD ["uvicorn", "main:app", "--reload", "--host 0.0.0.0", "--port 5000"]
