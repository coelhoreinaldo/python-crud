CREATE DATABASE IF NOT EXISTS the_office_db;

USE the_office_db;

CREATE TABLE IF NOT EXISTS people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    gender CHAR(1) NOT NULL
);

INSERT INTO people (name, age, gender) VALUES
    ('Michael Scott', 40, 'M'),
    ('Dwight Schrute', 38, 'M'),
    ('Jim Halpert', 30, 'M'),
    ('Pam Beesly', 30, 'F'),
    ('Angela Martin', 35, 'F');
