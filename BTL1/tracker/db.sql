DROP DATABASE IF EXISTS computer_network;
CREATE DATABASE computer_network;
USE computer_network;

CREATE TABLE login (
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    hostname VARCHAR(255) NOT NULL,
    PRIMARY KEY (email, hostname)
);

CREATE TABLE magnet (
    IP VARCHAR(255),
    port VARCHAR(255),
    email VARCHAR(255),
    hostname VARCHAR(255),
    file_name VARCHAR(255),
    piece_hash VARCHAR(255),
    part VARCHAR(255),
    FOREIGN KEY (email, hostname) REFERENCES login(email, hostname)
);

INSERT INTO login (email, password, hostname) VALUES
("myemail", "mypassword", "myhostname");