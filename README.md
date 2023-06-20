# bibliograph

[![codecov](https://codecov.io/gh/emp7yhead/bibliograph/branch/main/graph/badge.svg?token=uV2RgGcNwq)](https://codecov.io/gh/emp7yhead/bibliograph)
[![Maintainability](https://api.codeclimate.com/v1/badges/c77cfa99ba81ed1d3c33/maintainability)](https://codeclimate.com/github/emp7yhead/bibliograph/maintainability)
[![Check and Build](https://github.com/emp7yhead/bibliograph/actions/workflows/CI.yml/badge.svg)](https://github.com/emp7yhead/bibliograph/actions/workflows/CI.yml)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/emptyhead/bibliograph/47122f2)

App for organizing book collection.

[Deployed app on railway](https://bibliograph-production.up.railway.app/)

[API documentation can be found here](https://bibliograph-production.up.railway.app/docs)

## Functionality

- Create, read, update, delete users
- JWT Authentification
- Create, read, update, delete bookshelves that stores you book collection
- And of course you can add books by title in your collection, track number of readed pages in book

## Requirements

- Mac / Linux
- Docker version 23.0.5
- Docker Compose version v2.17.3
- GNU Make

## Main Dependencies

- python = "^3.11"
- fastapi = "^0.97.0"
- aiohttp = "^3.8.4"
- alembic = "^1.11.1"
- SQLAlchemy = "^2.0.16"
- uvicorn = "^0.22.0"

## Installation

- Clone repository

    ```bash
    git clone git@github.com:emp7yhead/bibliograph.git
    ```

- Fill the `.env.example` file. You need to specify:

  - `SECRET_KEY` - secret key. That's it.
  - `POSTGRES_SERVER` - host and port of database. If you use docker compose set value to `database`
  - `POSTGRES_DB` - database name
  - `POSTGRES_USER` - database user
  - `POSTGRES_PASSWORD` - password to database for specified user

- Install all dependencies, run migrations and start server by executing command:

    ```bash
    make run
    ```

- Go to 0.0.0.0:5000

### Docker

You always can use docker image for:

- installation

  ```bash
  docker pull emptyhead/bibliograph --platform linux/x86_64
  ```

- applying migration

  ```bash
  docker run -ti -p 5000:5000 emptyhead/bibliograph make migrate
  ```

- run app

  ```bash
  docker run -ti -p 5000:5000 emptyhead/bibliograph
  ```

But don't forget about environment variables when using docker.
