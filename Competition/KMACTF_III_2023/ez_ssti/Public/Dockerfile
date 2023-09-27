From openjdk:8u232-slim

RUN sed -i 's/deb.debian.org/mirror.sjtu.edu.cn/g' /etc/apt/sources.list \
    && sed -i 's/security.debian.org/mirror.sjtu.edu.cn/g' /etc/apt/sources.list \
    && useradd ctf \
    && mkdir /opt/app

RUN apt-get update
RUN apt-get install -y curl

COPY Server.jar /opt/app
COPY flag /flag

WORKDIR /opt/app

USER ctf
EXPOSE 8090
CMD ["java", "-jar", "/opt/app/Server.jar"]