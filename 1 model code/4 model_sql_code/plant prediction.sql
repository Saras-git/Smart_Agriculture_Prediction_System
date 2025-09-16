CREATE DATABASE IF NOT EXISTS plant_db;
USE plant_db;

CREATE TABLE IF NOT EXISTS plant_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    soil_type VARCHAR(20),
    sunlight_hours FLOAT,
    water_frequency VARCHAR(20),
    fertilizer_type VARCHAR(20),
    temperature FLOAT,
    humidity FLOAT,
    prediction VARCHAR(20),
    date DATETIME
);
select * from plant_predictions;