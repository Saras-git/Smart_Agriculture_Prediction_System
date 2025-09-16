import streamlit as st
import numpy as np
import pickle as pkl
import mysql.connector
import datetime

# Load the trained model
model = pkl.load(open('model\plant_growth.pkl', 'rb'))

# Categorical Mappings
soil_mapping = {"loam": 0, "sandy": 1, "clay": 2}
water_mapping = {"weekly": 1, "bi-weekly": 0, "daily": 2}
fertilizer_mapping = {"none": 0, "organic": 1, "chemical": 2}

# Streamlit App
st.title("🌱 Plant Growth Prediction App")

st.sidebar.header("🌿 Enter Plant Details")

# User Inputs
soil_type = st.sidebar.selectbox("Soil Type", list(soil_mapping.keys()))
sunlight_hours = st.sidebar.slider("Sunlight Hours", 0.0, 24.0, 6.0)
water_freq = st.sidebar.selectbox("Water Frequency", list(water_mapping.keys()))
fertilizer_type = st.sidebar.selectbox("Fertilizer Type", list(fertilizer_mapping.keys()))
temperature = st.sidebar.slider("Temperature (°C)", 0.0, 50.0, 25.0)
humidity = st.sidebar.slider("Humidity (%)", 0.0, 100.0, 50.0)

if st.sidebar.button("Predict Growth"):
    # Encode categorical inputs
    soil = soil_mapping[soil_type]
    water = water_mapping[water_freq]
    fertilizer = fertilizer_mapping[fertilizer_type]

    # Prepare input
    user_input = np.array([[soil, sunlight_hours, water, fertilizer, temperature, humidity]])

    # Predict
    prediction = model.predict(user_input)[0]
    result = "Grow 🌱" if prediction == 1 else "Not Grow ❌"

    # Display result
    st.success(f"Prediction: The plant will **{result}**")

    # Connect to MySQL and insert data
    try:
        conn = mysql.connector.connect(
            host="localhost",  # or your DB host
            user="root",
            password="Saraswathi99*",
            database=""
        )
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO plant_predictions (soil_type, sunlight_hours, water_frequency, fertilizer_type, temperature, humidity, prediction, date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (soil_type, sunlight_hours, water_freq, fertilizer_type, temperature, humidity, result, datetime.datetime.now())
        cursor.execute(insert_query, values)
        conn.commit()
        st.info("Prediction stored in database.")
    except Exception as e:
        st.error(f"Database Error: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
