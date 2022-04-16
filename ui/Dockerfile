FROM node:16.2-alpine

RUN mkdir -p /home/ui
WORKDIR /home/ui

COPY yarn.lock /home/ui

RUN yarn install
