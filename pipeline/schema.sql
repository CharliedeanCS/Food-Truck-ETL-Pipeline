-- This file should contain table definitions for the database.
SET search_path = 'charlie_schema';

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS trucks;
DROP TABLE IF EXISTS payment_type;

CREATE TABLE trucks(
    id INT PRIMARY KEY identity(1, 1),
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    card_reader BOOLEAN NOT NULL,
    rsa_rating INT NOT NULL
);

CREATE TABLE payment_type(
    id INT PRIMARY KEY identity(1, 1),
    payment_type_name TEXT NOT NULL
);

CREATE TABLE transactions(
    id INT PRIMARY KEY identity(1, 1),
    at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_price FLOAT NOT NULL,
    payment_type_id INT,
    FOREIGN KEY (payment_type_id)
        REFERENCES payment_type(id),
    truck_id INT,
    FOREIGN KEY (truck_id)
        REFERENCES trucks(id),
    UNIQUE(at,total_price,payment_type_id,truck_id)
); 


INSERT INTO 
    trucks(name,description,card_reader,rsa_rating)
VALUES
    (
        'Burrito Madness',
        'An authentic taste of Mexico.',
        TRUE,
        4
    ),
    (
        'Kings of Kebabs',
        'Locally-sourced meat cooked over a charcoal grill.',
        TRUE,
        2
    ),
    (
        'Cupcakes by Michelle',
        'Handcrafted cupcakes made with high-quality, organic ingredients.',
        TRUE,
        5
    ),
    (
        'Hartmanns Jellied Eels',
        'A taste of history with this classic English dish.',
        TRUE,
        4
    ),
    (
        'Yoghurt Heaven',
        'All the great tastes, but only some of the calories!',
        TRUE,
        4
    ),
    (
        'SuperSmoothie',
        'Pick any fruit or vegetable, and we will make you a delicious, healthy, multi-vitamin shake. Live well; live wild.',
        FALSE,
        3
    );

INSERT INTO payment_type(payment_type_name) VALUES ('Card'),('Cash');


COMMIT;