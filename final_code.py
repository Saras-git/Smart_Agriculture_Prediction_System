import streamlit as st
import pickle
import numpy as np
import mysql.connector
from mysql.connector import Error

# Load models
def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)

crop_yield_model = load_model("C:/Users/ramki/OneDrive/Desktop/mini/crop_yield.pkl")
plant_growth_model = load_model("C:/Users/ramki/OneDrive/Desktop/mini/plant_growth.pkl")
fertilizer_model = load_model("C:/Users/ramki/OneDrive/Desktop/mini/fertilizer.pkl")
crop_model = load_model("C:/Users/ramki/OneDrive/Desktop/mini/crop.pkl")

# Connect to MySQL database
def connect_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='smart_agriculture',
            user='root',
            password='Saraswathi99*'
        )
        return conn
    except Error as e:
        st.error(f"Database connection error: {e}")
        return None

# Convert numpy types to native Python types
def convert_np_types(val):
    if isinstance(val, (np.int64, np.int32)):
        return int(val)
    elif isinstance(val, (np.float64, np.float32)):
        return float(val)
    else:
        return val

# General insert function with conversion
def execute_insert(query, values):
    # Convert all numpy types in values to native Python types
    values = tuple(convert_np_types(v) for v in values)

    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
        except Error as e:
            st.error(f"Failed to insert into database: {e}")
        finally:
            conn.close()

# Streamlit App
st.title("🌱 Smart Agriculture Prediction System")

# Sidebar for selecting a model
model_choice = st.sidebar.radio("Select a Prediction Model", 
    ["Crop Yield Prediction", "Plant Growth Prediction", "Fertilizer Recommendation", "Crop Recommendation"])

# Crop Yield Prediction
if model_choice == "Crop Yield Prediction":
    st.subheader("🌾 Crop Yield Prediction")
    countries = ['Albania', 'India', 'Brazil', 'France', 'USA']  # simplified for demo
    crops = ['Maize', 'Wheat', 'Rice, paddy']
    
    country = st.selectbox("🌍 Select Country", countries)
    crop = st.selectbox("🌽 Select Crop", crops)
    year = st.number_input("📅 Year", 1900, 2100, 2025)
    rainfall = st.number_input("🌧️ Rainfall (mm/year)", format="%.2f")
    pesticides = st.number_input("🧪 Pesticides Used (tonnes)", format="%.2f")
    temperature = st.number_input("🌡️ Temperature (°C)", format="%.2f")

    if st.button("🚀 Predict Yield"):
        features = np.array([[countries.index(country), crops.index(crop), year, rainfall, pesticides, temperature]])
        prediction = crop_yield_model.predict(features)[0]
        st.success(f"🌾 **Predicted Yield (hg/ha):** {prediction:.2f}")

        query = """INSERT INTO crop_yield_predictions (country, crop, year, rainfall, pesticides, temperature, predicted_yield)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        execute_insert(query, (country, crop, int(year), float(rainfall), float(pesticides), float(temperature), float(prediction)))

# Plant Growth Prediction
elif model_choice == "Plant Growth Prediction":
    st.subheader("🌿 Plant Growth Prediction")

    # Define mappings for categorical variables
    soil_mapping = {'Loamy': 0, 'Sandy': 1, 'Clay': 2}
    fertilizer_mapping = {'NPK': 0, 'Urea': 1, 'Compost': 2}
    water_mapping = {'Daily': 1, 'Weekly': 7, 'Biweekly': 14, 'Monthly': 30}  # Example water frequency mapping

    # Sidebar inputs with mapping keys for selections
    soil_type = st.sidebar.selectbox("🌱 Soil Type", list(soil_mapping.keys()))
    sunlight_hours = st.sidebar.slider("☀️ Sunlight Hours", 0.0, 24.0, 12.0, format="%.2f")
    water_frequency_label = st.sidebar.selectbox("💧 Water Frequency", list(water_mapping.keys()))
    fertilizer_type = st.sidebar.selectbox("🌾 Fertilizer Type", list(fertilizer_mapping.keys()))
    temperature = st.sidebar.slider("🌡️ Temperature (°C)", 0.0, 50.0, 25.0, format="%.2f")
    humidity = st.sidebar.slider("💧 Humidity (%)", 0.0, 100.0, 60.0, format="%.2f")

    if st.sidebar.button("🚀 Predict Growth Status"):
        # Map categorical inputs to numerical values for the model
        soil = soil_mapping[soil_type]
        fertilizer = fertilizer_mapping[fertilizer_type]
        water_frequency = water_mapping[water_frequency_label]

        features = np.array([[soil, sunlight_hours, water_frequency, fertilizer, temperature, humidity]])
        growth_pred = plant_growth_model.predict(features)[0]

        # Friendly output string
        growth_status = "Grow 🌱" if growth_pred == 1 else "Not Grow ❌"
        st.success(f"🌿 **Growth Status:** {growth_status}")

        # Insert original labels and values into DB
        query = """INSERT INTO plant_growth_predictions 
                   (soil_type, sunlight_hours, water_frequency, fertilizer_type, temperature, humidity, growth_status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        execute_insert(query, (soil_type, float(sunlight_hours), water_frequency_label, fertilizer_type, float(temperature), float(humidity), growth_status))


# Fertilizer Recommendation
elif model_choice == "Fertilizer Recommendation":
    st.subheader("💧 Fertilizer Recommendation System")
    
    # Load label_encoders inside this block with correct indentation
    with open('C:/Users/ramki/OneDrive/Desktop/mini/label_encoders.pkl', 'rb') as f:
        label_encoders = pickle.load(f)
    
    # Your categories (should match training categories exactly)
    soil_types = ['Loamy', 'Sandy', 'Clay']
    crop_types = ['Maize', 'Rice', 'Wheat']

    # Input widgets
    temperature = st.number_input("🌡️ Temperature (°C)", format="%.2f", value=25.0)
    humidity = st.number_input("💧 Humidity (%)", format="%.2f", value=50.0)
    moisture = st.number_input("💦 Moisture (%)", format="%.2f", value=30.0)
    soil_type = st.selectbox("🌱 Soil Type", soil_types)
    crop_type = st.selectbox("🌾 Crop Type", crop_types)
    nitrogen = st.number_input("⚡ Nitrogen (%)", format="%.2f", value=50.0)
    potassium = st.number_input("⚡ Potassium (%)", format="%.2f", value=50.0)
    phosphorus = st.number_input("⚡ Phosphorus (%)", format="%.2f", value=50.0)

    if st.button("🚀 Recommend Fertilizer"):
        # Encode categorical variables using label_encoders
        soil_encoded = label_encoders["Soil_Type"].transform([soil_type])[0]
        crop_encoded = label_encoders["Crop_Type"].transform([crop_type])[0]

        # Prepare features array for model input
        features = np.array([[temperature, humidity, moisture,
                              soil_encoded, crop_encoded,
                              nitrogen, potassium, phosphorus]])

        # Predict encoded fertilizer label
        prediction_encoded = fertilizer_model.predict(features)[0]

        # Decode predicted label to fertilizer name
        recommended_fertilizer = label_encoders["Fertilizer"].inverse_transform([prediction_encoded])[0]

        # Show the decoded fertilizer name
        st.success(f"💧 **Recommended Fertilizer:** {recommended_fertilizer}")

        # Insert into database
        query = """INSERT INTO fertilizer_recommendation
                   (temperature, humidity, moisture, soil_type, crop_type,
                    nitrogen, potassium, phosphorus, recommended_fertilizer)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        execute_insert(query, (float(temperature), float(humidity), float(moisture),
                              soil_type, crop_type, float(nitrogen), float(potassium),
                              float(phosphorus), recommended_fertilizer))




# Crop Recommendation
elif model_choice == "Crop Recommendation":
    st.subheader("🌾 Crop Recommendation")

    # Load label encoder (make sure the file exists and is accessible)
    with open("C:/Users/ramki/OneDrive/Desktop/mini/label_encoder.pkl", 'rb') as f:
        le = pickle.load(f)

    nitrogen = st.number_input("⚡ Nitrogen (%)", format="%.2f")
    phosphorus = st.number_input("⚡ Phosphorus (%)", format="%.2f")
    potassium = st.number_input("⚡ Potassium (%)", format="%.2f")
    temperature = st.number_input("🌡️ Temperature (°C)", format="%.2f")
    humidity = st.number_input("💧 Humidity (%)", format="%.2f")
    ph = st.number_input("🔬 pH Level", format="%.2f")
    rainfall = st.number_input("🌧️ Rainfall (mm)", format="%.2f")

    if st.button("🚀 Recommend Crop"):
        features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        
        # Predict encoded crop label
        prediction_encoded = crop_model.predict(features)[0]
        
        # Decode label to crop name
        recommended_crop = le.inverse_transform([prediction_encoded])[0]
        
        st.success(f"🌾 **Recommended Crop:** {recommended_crop}")

        # Insert into database
        query = """INSERT INTO crop_recommendations 
                   (nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall, recommended_crop)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        execute_insert(query, (
            float(nitrogen), float(phosphorus), float(potassium),
            float(temperature), float(humidity), float(ph), float(rainfall),
            str(recommended_crop)
        ))
