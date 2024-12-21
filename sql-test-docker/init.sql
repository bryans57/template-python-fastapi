CREATE TABLE person
(
    id             SERIAL PRIMARY KEY,
    identification VARCHAR(50)  NOT NULL UNIQUE,
    first_name     VARCHAR(100) NOT NULL,
    last_name      VARCHAR(100) NOT NULL,
    weight         DECIMAL(5, 2),
    height         DECIMAL(5, 2),
    age            INT CHECK (age >= 0),
    city           VARCHAR(100),
    country        VARCHAR(100),
    email          VARCHAR(255) UNIQUE,
    phone          VARCHAR(15),
    address        TEXT,
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO person (identification, first_name, last_name, weight, height, age, city, country, email, phone, address)
VALUES ('123456789', 'John', 'Doe', 70.5, 1.75, 30, 'New York', 'USA',
        'john@mail.com', '3452359621', '123 Main St, New York, NY 10030'),
       ('987654321', 'Jane', 'Doe', 60.5, 1.65, 25, 'Los Angeles', 'USA',
        'jane@mail.com', '3452359622', '123 Main St, Los Angeles, CA 90030');
