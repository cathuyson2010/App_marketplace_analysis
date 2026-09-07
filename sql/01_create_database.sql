-- MySQL 8.0+. Does not delete existing data.
CREATE DATABASE IF NOT EXISTS app_marketplace CHARACTER SET utf8mb4;
USE app_marketplace;
CREATE TABLE IF NOT EXISTS apps (
 app_id INT AUTO_INCREMENT PRIMARY KEY,
 app_name VARCHAR(255) NOT NULL,
 category VARCHAR(100),
 rating DECIMAL(3,2),
 reviews BIGINT,
 size VARCHAR(50),
 installs BIGINT,
 app_type VARCHAR(20),
 price DECIMAL(10,2),
 content_rating VARCHAR(50),
 genres VARCHAR(255),
 last_updated VARCHAR(50),
 current_version VARCHAR(100),
 android_version VARCHAR(100)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
