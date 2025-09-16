CREATE DATABASE crop_db;
USE crop_db;

CREATE TABLE crop_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    N INT,
    P INT,
    K INT,
    temperature FLOAT,
    humidity FLOAT,
    ph FLOAT,
    rainfall FLOAT,
    predicted_crop VARCHAR(50),
    date DATETIME
);
select * from crop_predictions;