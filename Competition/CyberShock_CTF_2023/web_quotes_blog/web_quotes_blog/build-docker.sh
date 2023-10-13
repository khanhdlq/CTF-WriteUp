#!/bin/bash
docker rm -f web_quotes_blog
docker build -t web_quotes_blog .
docker run --name=web_quotes_blog --rm -p1337:1337 -it web_quotes_blog
