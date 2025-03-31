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

-- Modify the vehicles table to include image URLs
ALTER TABLE vehicles
ADD COLUMN image_url VARCHAR(255);

-- Insert 20 vehicles with images
INSERT INTO vehicles (model, brand, price, available, image_url) VALUES 

('Camry', 'Toyota', 170.00, 1, 'https://www.toyota.com/imgix/responsive/images/mlp/colorizer/2023/camry/4T3/1.png'),
('Accord', 'Honda', 160.00, 1, 'https://cdn.motor1.com/images/mgl/6ZX4Z/s1/2023-honda-accord-touring.jpg'),
('Mustang', 'Ford', 250.00, 1, 'https://www.ford.com/cmslibs/content/dam/vdm_ford/live/en_us/ford/nameplate/mustang/2023/collections/3-2/23_FRD_MST_34098.jpg'),
('Model 3', 'Tesla', 300.00, 1, 'https://www.tesla.com/sites/default/files/models3-new/social/model-3-hero-social.jpg'),
('Silverado', 'Chevrolet', 220.00, 1, 'https://www.chevrolet.com/content/dam/chevrolet/na/us/english/index/vehicles/2023/trucks/silverado/01-images/2023-silverado-ld-mh1.jpg'),
('RAV4', 'Toyota', 190.00, 1, 'https://www.toyota.com/imgix/responsive/images/mlp/colorizer/2023/rav4/3T3/1.png'),
('CX-5', 'Mazda', 175.00, 1, 'https://www.mazdausa.com/siteassets/vehicles/2023/cx-5/gallery/exterior/2023-mazda-cx-5-gallery-exterior-01.jpg'),
('Wrangler', 'Jeep', 230.00, 1, 'https://www.jeep.com/content/dam/fca-brands/na/jeep/en_us/2023/wrangler/gallery/exterior/2023-jeep-wrangler-gallery-exterior-01.jpg'),
('Outback', 'Subaru', 185.00, 1, 'https://www.subaru.com/content/dam/subaru/vehicles/outback/2023/gallery/exterior/2023-outback-gallery-exterior-01.jpg'),
('Tucson', 'Hyundai', 165.00, 1, 'https://www.hyundai.com/content/dam/hyundai/au/en/models/tucson/tucson-highlander-2022/overview/design/exterior/01-desktop/Highlander_Ext_LakeSideBlue.jpg'),
('Altima', 'Nissan', 155.00, 1, 'https://www.nissanusa.com/content/dam/nissan/vehicles/2023/altima/overview/2023-nissan-altima-2-0-sr-vlp-hero-desktop.jpg'),
('Sorento', 'Kia', 195.00, 1, 'https://www.kia.com/content/dam/kia/us/en/vehicles/sorento/2023/gallery/exterior/2023-sorento-gallery-exterior-01.jpg'),
('Explorer', 'Ford', 210.00, 1, 'https://www.ford.com/cmslibs/content/dam/vdm_ford/live/en_us/ford/nameplate/explorer/2023/collections/3-2/23_FRD_EXP_34050.jpg'),
('Grand Cherokee', 'Jeep', 240.00, 1, 'https://www.jeep.com/content/dam/fca-brands/na/jeep/en_us/2023/grand-cherokee/gallery/exterior/2023-jeep-grand-cherokee-gallery-exterior-01.jpg'),
('Model Y', 'Tesla', 320.00, 1, 'https://www.tesla.com/sites/default/files/modelsx-new/social/model-y-social.jpg'),
('Tahoe', 'Chevrolet', 260.00, 1, 'https://www.chevrolet.com/content/dam/chevrolet/na/us/english/index/vehicles/2023/suvs/tahoe/01-images/2023-tahoe-mh1.jpg'),
('Highlander', 'Toyota', 225.00, 1, 'https://www.toyota.com/imgix/responsive/images/mlp/colorizer/2023/highlander/8X3/1.png'),
('Palisade', 'Hyundai', 235.00, 1, 'https://www.hyundai.com/content/dam/hyundai/au/en/models/palisade/highlander-2022/overview/design/exterior/01-desktop/Highlander_Ext_White.jpg'); 
ALTER TABLE vehicles DROP COLUMN image_url;