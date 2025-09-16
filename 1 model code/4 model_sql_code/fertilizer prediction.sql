CREATE DATABASE IF NOT EXISTS agriculture_db;
USE agriculture_db;

CREATE TABLE IF NOT EXISTS fertilizer_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature FLOAT,
    humidity FLOAT,
    moisture FLOAT,
    soil_type VARCHAR(50),
    crop_type VARCHAR(50),
    nitrogen INT,
    potassium INT,
    phosphorous INT,
    prediction VARCHAR(50),
    date DATETIME
);
