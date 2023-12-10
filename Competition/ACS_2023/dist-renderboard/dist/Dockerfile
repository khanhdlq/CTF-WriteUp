FROM node:16-alpine

WORKDIR /app

# COPY package*.json /app
COPY renderboard /app
COPY create.sql /app
COPY flag.txt /

RUN apk add --no-cache mysql-client
RUN apk add vim
RUN apk add curl
RUN npm install --silent
RUN npm install express-session session-file-store
RUN npm install mysql
RUN npm install ejs@3.1.6
RUN chmod o+w /app/sessions

#CREATE A NEW USER
RUN adduser -D acsuser
USER acsuser

#COPY create.sql .
ENV PATH /app/node_modules/.bin:$PATH

WORKDIR /home/acsuser
CMD ["sh", "-c", "sleep 10 && mysql -h db -u root -p1324 < /app/create.sql && node /app/main.js"]