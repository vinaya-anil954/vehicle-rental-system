CREATE DATABASE IF NOT EXISTS vehicle_rental;
USE vehicle_rental;

-- Users Table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Admins Table
CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Vehicles Table
CREATE TABLE IF NOT EXISTS vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(100) NOT NULL,
    brand VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

-- Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE
);

-- Payments Table
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    user_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
INSERT INTO admins (email, password) VALUES ('admin@example.com', 'admin');  
INSERT INTO vehicles (model, brand, price, available) VALUES ('Civic', 'Honda', 150.00, 1);
INSERT INTO vehicles (model, brand, price, available) VALUES ('Corolla', 'Toyota', 180.00, 1);
INSERT INTO vehicles (model, brand, price, available) VALUES ('F-150', 'Ford', 200.00, 1);

ALTER TABLE bookings
ADD COLUMN from_date DATE NOT NULL,
ADD COLUMN total_days INT NOT NULL;

ALTER TABLE bookings
ADD COLUMN to_date DATE NOT NULL;
-- Add drivers table
CREATE TABLE IF NOT EXISTS drivers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    license_number VARCHAR(50) NOT NULL UNIQUE,
    contact_number VARCHAR(20) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);
-- Add sample drivers
INSERT INTO drivers (name, license_number, contact_number) VALUES
('John Smith', 'DL123456', '+1 555-0101'),
('Sarah Johnson', 'DL789012', '+1 555-0102'),
('Michael Brown', 'DL345678', '+1 555-0103'),
('Emily Davis', 'DL901234', '+1 555-0104'),
('David Wilson', 'DL567890', '+1 555-0105');
ALTER TABLE bookings ADD COLUMN total_price DECIMAL(10,2) DEFAULT 0.00;
ALTER TABLE bookings
ADD COLUMN needs_driver BOOLEAN DEFAULT FALSE,
ADD COLUMN driver_id INT NULL,
ADD COLUMN total_price DECIMAL(10,2) DEFAULT 0.00,
ADD FOREIGN KEY (driver_id) REFERENCES drivers(id);