-- Drop the database if it exists (for a fresh start)
DROP DATABASE IF EXISTS rental_system;
CREATE DATABASE rental_system;
USE rental_system;

-- Admin Table
DROP TABLE IF EXISTS admin;
CREATE TABLE admin (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Users Table
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15),
    password VARCHAR(255) NOT NULL
);

-- Vehicles Table with photo_url column
DROP TABLE IF EXISTS vehicles;
CREATE TABLE vehicles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model VARCHAR(100),
    brand VARCHAR(100),
    price_per_day DECIMAL(10,2),
    availability BOOLEAN DEFAULT TRUE,
    photo_url VARCHAR(255)
);

-- Insert sample vehicles (replace example URLs with actual image URLs)
INSERT INTO vehicles (model, brand, price_per_day, availability, photo_url)
VALUES 
('Model X', 'Tesla', 5000, TRUE, 'https://example.com/tesla_model_x.jpg'),
('Civic', 'Honda', 3000, TRUE, 'https://example.com/honda_civic.jpg'),
('Corolla', 'Toyota', 5000, TRUE, 'https://example.com/toyota_corolla.jpg'),
('Mustang', 'Ford', 4500, TRUE, 'https://example.com/ford_mustang.jpg'),
('Camry', 'Toyota', 3500, TRUE, 'https://example.com/toyota_camry.jpg');

-- Bookings Table
DROP TABLE IF EXISTS bookings;
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    vehicle_id INT,
    rent_date DATE,
    return_date DATE,
    total_price DECIMAL(10,2),
    status ENUM('Pending', 'Approved', 'Completed', 'Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);

-- Payments Table
DROP TABLE IF EXISTS payments;
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT,
    user_id INT,
    amount DECIMAL(10,2),
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending', 'Completed', 'Failed') DEFAULT 'Pending',
    FOREIGN KEY (booking_id) REFERENCES bookings(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
INSERT INTO admin (name, email, password) 
VALUES ('Admin', 'admin@example.com', '$fGLvbcRlzd3Uff7b$6f3fe783d744ca79c427d96e4a108d798e3b0ffc6c1d8db41cfe644a98f8ac497450dbbc52fe8848b6d3a023c70168c697310543704316bbf0cde88b6c83e35a');
