# crop_recommendation_app.py

import streamlit as st
import numpy as np
import pickle as pkl
import datetime
import mysql.connector

# Load trained model and label encoder
model = pkl.load(open('C:/Users/ramki/OneDrive/Desktop/machine learning/model/crop.pkl', 'rb'))
le = pkl.load(open('label_encoder.pkl', 'rb'))  # Save label encoder separately during training

# Streamlit App
st.title("🌾 Crop Recommendation System")
st.sidebar.header("🚜 Enter Soil and Weather Details")

# User Inputs
N = st.sidebar.number_input("Nitrogen (N)", min_value=0, max_value=200, value=90)
P = st.sidebar.number_input("Phosphorus (P)", min_value=0, max_value=200, value=42)
K = st.sidebar.number_input("Potassium (K)", min_value=0, max_value=200, value=43)
temperature = st.sidebar.slider("Temperature (°C)", 0.0, 50.0, 25.0)
humidity = st.sidebar.slider("Humidity (%)", 0.0, 100.0, 80.0)
ph = st.sidebar.slider("Soil pH", 0.0, 14.0, 6.5)
rainfall = st.sidebar.slider("Rainfall (mm)", 0.0, 300.0, 100.0)

if st.sidebar.button("🌱 Recommend Crop"):
    user_input = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    prediction = model.predict(user_input)
    crop_name = le.inverse_transform(prediction)[0]
    st.success(f"✅ Recommended Crop: **{crop_name}**")

    # Optional: Store prediction in MySQL
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saraswathi99*",
            database="crop_db"  # Replace with your DB name
        )
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO crop_predictions (N, P, K, temperature, humidity, ph, rainfall, predicted_crop, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (N, P, K, temperature, humidity, ph, rainfall, crop_name, datetime.datetime.now())
        cursor.execute(insert_query, values)
        conn.commit()
        st.info("Prediction saved in the database.")
    except Exception as e:
        st.error(f"Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
