# Smart Agriculture System 🌱

A machine learning–based smart agriculture system that helps farmers make data-driven decisions for crop selection, fertilizer usage, and yield prediction.

## Overview
This project uses machine learning models to analyze agricultural data and provide intelligent recommendations related to:
- Crop Recommendation
- Crop yield prediction
- Fertilizer recommendation
- Plant growth analysis

It aims to improve productivity and reduce risks in farming by leveraging data and ML techniques.

## Features
- Crop recommendation using trained ML models
- Crop yield prediction
- Fertilizer suggestion system
- Plant growth prediction
- Dataset-based training and evaluation
- SQL integration for data storage
- Pre-trained models saved using `.pkl` files

## Tech Stack
- **Programming Language:** Python
- **Machine Learning:** Scikit-learn
- **Data Handling:** Pandas, NumPy
- **Database:** SQL
- **Model Storage:** Pickle (`.pkl`)
- **Dataset:** CSV-based agricultural datasets

## Project Structure
- `model/` – Machine learning models
- `datasets/` – Training and testing datasets
- `sql code/` – SQL queries and database logic
- `final_code.py` – Main execution file
- `crop.pkl` – Crop recommendation model
- `crop_yield.pkl` – Crop yield prediction model
- `fertilizer.pkl` – Fertilizer recommendation model
- `plant_growth.pkl` – Plant growth prediction model
- `label_encoder.pkl`, `label_encoders.pkl` – Encoders used in preprocessing
- `final output/` – Output results and predictions

## How to Run
```bash
pip install -r requirements.txt
python final_code.py
