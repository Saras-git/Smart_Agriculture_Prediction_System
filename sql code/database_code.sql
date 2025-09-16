
CREATE DATABASE smart_agriculture;

-- Use the created database
USE smart_agriculture;

-- Create a table for crop yield prediction results
CREATE TABLE crop_yield_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country VARCHAR(255),
    crop VARCHAR(255),
    year INT,
    rainfall DECIMAL(10, 2),
    pesticides DECIMAL(10, 2),
    temperature DECIMAL(5, 2),
    predicted_yield DECIMAL(10, 2),
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from crop_yield_predictions;

-- Create a table for plant growth prediction results
CREATE TABLE plant_growth_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    soil_type VARCHAR(255),
    sunlight_hours INT,
    water_frequency VARCHAR(255),
    fertilizer_type VARCHAR(255),
    temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    growth_status VARCHAR(255),
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a table for fertilizer recommendations
CREATE TABLE fertilizer_recommendation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    temperature INT,
    humidity INT
    moisture INT,
    soil_type VARCHAR(255),
    crop_type VARCHAR(255),
    nitrogen INT,
    potassium INT,
    phosphorus INT,
    recommended_fertilizer VARCHAR(255),  -- Keeps as VARCHAR for storing fertilizer as a string
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Create a table for crop recommendations
CREATE TABLE crop_recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nitrogen DECIMAL(5, 2),
    phosphorus DECIMAL(5, 2),
    potassium DECIMAL(5, 2),
    temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    ph DECIMAL(5, 2),
    rainfall DECIMAL(5, 2),
    recommended_crop VARCHAR(255),
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from crop_yield_predictions;
select * from plant_growth_predictions;
select * from crop_recommendations;
select * from fertilizer_recommendation;