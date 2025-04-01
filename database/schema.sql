-- Create the database and use it
CREATE DATABASE IF NOT EXISTS vehicle_rental;
USE vehicle_rental;

-- Table for users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

-- Table for admins
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

-- Table for vehicles
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(100),
    brand VARCHAR(100),
    price DECIMAL(10,2),
    available BOOLEAN DEFAULT TRUE
);

-- Table for bookings
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    vehicle_id INT,
    status ENUM('Booked', 'Cancelled') DEFAULT 'Booked',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);
INSERT INTO admins (email, password)
VALUES ('admin@example.com', 'adminpass');
USE vehicle_rental;

INSERT INTO vehicles (model, brand, price, available) VALUES ('Civic', 'Honda', 150.00, 1);
INSERT INTO vehicles (model, brand, price, available) VALUES ('Corolla', 'Toyota', 180.00, 1);
INSERT INTO vehicles (model, brand, price, available) VALUES ('F-150', 'Ford', 200.00, 1)