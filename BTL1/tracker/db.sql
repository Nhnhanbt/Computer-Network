DROP DATABASE IF EXISTS computer_network;
CREATE DATABASE computer_network;
USE computer_network;

CREATE TABLE login (
    email VARCHAR(255) NOT NULL PRIMARY KEY,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE peers (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    IP VARCHAR(255),
    port VARCHAR(255),
    hostname VARCHAR(255),
    file_name VARCHAR(255),
    file_size VARCHAR(255),
    piece_hash VARCHAR(255),
    piece_size VARCHAR(255),
    piece_order VARCHAR(255)
    FOREIGN KEY (hostname) REFERENCES login(email)
);
-- CREATE TABLE peers (
--     ID INT AUTO_INCREMENT PRIMARY KEY,
--     IP VARCHAR(255),
--     port VARCHAR(255),
--     hostname VARCHAR(255),
--     file_name VARCHAR(255),
--     file_size VARCHAR(255),
--     piece_hash VARCHAR(255),
--     piece_size VARCHAR(255),
--     piece_order VARCHAR(255),
--     public_key VARCHAR(255)
--     FOREIGN KEY (hostname) REFERENCES login(email)
-- );

INSERT INTO login (email, password) VALUES
("myemail", "mypassword");