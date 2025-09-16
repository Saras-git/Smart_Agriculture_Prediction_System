CREATE DATABASE IF NOT EXISTS crop_db;

USE crop_db;

CREATE TABLE IF NOT EXISTS yield_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    area_name VARCHAR(100),
    item_name VARCHAR(100),
    year INT,
    rainfall FLOAT,
    pesticides FLOAT,
    temperature FLOAT,
    predicted_yield FLOAT,
    prediction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
