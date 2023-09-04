FROM node:20-alpine

WORKDIR /frontend

COPY ./frontend/package.json ./frontend/yarn.lock ./

RUN yarn install --trace-warnings

COPY /frontend ./

CMD ["yarn", "dev"]
