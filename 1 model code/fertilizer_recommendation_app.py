import streamlit as st
import numpy as np
import pandas as pd
import pickle as pkl
from sklearn.preprocessing import StandardScaler
import datetime
import mysql.connector

# Load the trained model and encoders
model = pkl.load(open('model/fertilizer.pkl', 'rb'))
scaler = pkl.load(open('scaler.pkl', 'rb'))
label_encoders = pkl.load(open('label_encoders.pkl', 'rb'))

# Mappings for UI
valid_soil_types = ['Clayey', 'Loamy', 'Red', 'Black', 'Sandy']
valid_crop_types = ['rice', 'Wheat', 'Tobacco', 'Sugarcane', 'Pulses', 'pomegranate',
                    'Paddy', 'Oil seeds', 'Millets', 'Maize', 'Ground Nuts', 'Cotton',
                    'coffee', 'watermelon', 'Barley', 'kidneybeans', 'orange']

# Title
st.title("🌾 Fertilizer Recommendation System")

# Sidebar inputs
st.sidebar.header("📥 Enter Crop Details")

temp = st.sidebar.slider("Temperature (°C)", 0.0, 50.0, 25.0)
humidity = st.sidebar.slider("Humidity (%)", 0.0, 100.0, 50.0)
moisture = st.sidebar.slider("Moisture (%)", 0.0, 100.0, 30.0)

soil_type = st.sidebar.selectbox("Soil Type", valid_soil_types)
crop_type = st.sidebar.selectbox("Crop Type", valid_crop_types)

nitrogen = st.sidebar.number_input("Nitrogen Level", min_value=0, max_value=100, value=50)
potassium = st.sidebar.number_input("Potassium Level", min_value=0, max_value=100, value=50)
phosphorous = st.sidebar.number_input("Phosphorous Level", min_value=0, max_value=100, value=50)

if st.sidebar.button("🌿 Recommend Fertilizer"):
    try:
        # Encode categorical data
        soil_encoded = label_encoders["Soil_Type"].transform([soil_type])[0]
        crop_encoded = label_encoders["Crop_Type"].transform([crop_type])[0]

        # Prepare input
        input_data = pd.DataFrame([[temp, humidity, moisture, soil_encoded, crop_encoded,
                                    nitrogen, potassium, phosphorous]],
                                  columns=["Temparature", "Humidity", "Moisture", "Soil_Type", "Crop_Type",
                                           "Nitrogen", "Potassium", "Phosphorous"])

        # Scale input
        input_scaled = scaler.transform(input_data)

        # Predict
        prediction_encoded = model.predict(input_scaled)[0]
        fertilizer_name = label_encoders["Fertilizer"].inverse_transform([prediction_encoded])[0]

        # Output
        st.success(f"🌱 **Recommended Fertilizer:** {fertilizer_name}")

        # Optional: Store to MySQL
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Saraswathi99*",
                database="agriculture_db"
            )
            cursor = conn.cursor()
            insert_query = """
            INSERT INTO fertilizer_predictions (temperature, humidity, moisture, soil_type, crop_type,
                                                nitrogen, potassium, phosphorous, prediction, date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (temp, humidity, moisture, soil_type, crop_type,
                      nitrogen, potassium, phosphorous, fertilizer_name, datetime.datetime.now())
            cursor.execute(insert_query, values)
            conn.commit()
            st.info("✅ Prediction stored in database.")
        except Exception as db_err:
            st.warning(f"⚠️ Could not save to database: {db_err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    except Exception as e:
        st.error(f"❌ Error: {e}")
