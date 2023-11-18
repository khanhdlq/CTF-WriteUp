FROM node:16.13.1-bullseye-slim

RUN apt-get update && apt-get -y install gcc
RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY ./src/ .

RUN npm install

ENV JWT_SECRET_KEY="[REDACTED]"

RUN echo "NightwolfCTF{chu_be_dan_nop_flag}" > /flag
RUN chmod 0400 /flag
COPY ./getFlag.c /getFlag.c
RUN gcc /getFlag.c -o /getFlag
RUN chmod 4755 /getFlag

EXPOSE 3000

CMD [ "node", "index.js" ]