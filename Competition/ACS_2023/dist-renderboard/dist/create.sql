GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY '1324';
FLUSH PRIVILEGES;

USE acs_data;

DROP TABLE IF EXISTS user;
CREATE TABLE user(
        redacted0 int not null auto_increment primary key,
        redacted1 varchar(30),
        redacted2 varchar(50),
        redacted3 varchar(100),
        is_admin int default 0
        );

INSERT INTO user(redacted1, redacted2, redacted3, is_admin) values('test1', 'test1', 'test1@acs.com', 1);
INSERT INTO user(redacted1, redacted2, redacted3, is_admin) values('test2', 'test2', 'test2@acs.com', 0);
INSERT INTO user(redacted1, redacted2, redacted3, is_admin) values('test3', 'test3', 'test3@acs.com', 0);

DROP TABLE IF EXISTS admin_notice;
CREATE TABLE admin_notice(
        no int not null auto_increment primary key,
        title varchar(50),
        content text,
        author varchar(50)
        );

DROP TABLE IF EXISTS boards;
CREATE TABLE boards(
        no int not null auto_increment primary key,
        title varchar(50),
        content text,
        author varchar(50)
        );

