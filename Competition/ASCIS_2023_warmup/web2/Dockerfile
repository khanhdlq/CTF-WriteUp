FROM sectigo1/webbase:latest
LABEL MAINTAINER Sectigo <system@sectigo.one>
USER root
RUN mkdir -p /etc/nginx/ssl
COPY ssl/server* /etc/nginx/ssl/
EXPOSE 80 443
HEALTHCHECK CMD curl --fail -k https://localhost:443 || exit 1
CMD ["nginx", "-g", "daemon off;"]