import pickle
import numpy as np
import pandas as pd
import streamlit as st
import os
import zipfile
import warnings
warnings.filterwarnings('ignore')

import zipfile
import os
import pickle

def load_pickle(file):
    base_dir = os.path.dirname(__file__)  # same directory as script
    file_path = os.path.join(base_dir, file)

    if file.endswith(".zip"):
        with zipfile.ZipFile(file_path, "r") as zip_ref:
            zip_ref.extractall(base_dir)
            for name in zip_ref.namelist():
                if name.endswith(".pkl"):
                    pkl_path = os.path.join(base_dir, name)
                    with open(pkl_path, "rb") as f:
                        obj = pickle.load(f)
                    os.remove(pkl_path)
                    return obj
    else:
        with open(file_path, "rb") as f:
            return pickle.load(f)

model = load_pickle("best_model.zip")
scaler = load_pickle("scaler.pkl")
mappings = load_pickle("mapping.pkl")

meal_map = mappings.get('type_of_meal_plan', {})
room_map = mappings.get('room_type_reserved', {})
market_map = mappings.get('market_segment_type', {})
print("Mappings loaded:", meal_map, room_map, market_map)
default_map = mappings.get('default', {})
numerical_cols = mappings.get('numerical_cols', {})
print(numerical_cols)
expected_columns = [
    'no_of_adults', 'no_of_children', 'no_of_weekend_nights', 'no_of_week_nights','type_of_meal_plan',
    'required_car_parking_space','room_type_reserved','lead_time','arrival_year','arrival_month','arrival_date',
    'market_segment_type','repeated_guest','no_of_previous_cancellations','no_of_previous_bookings_not_canceled','avg_price_per_room','no_of_special_requests'
    ]

st.title("Hotel Booking Cancellation Predictor")
st.write("Enter the details below to predict hotel booking cancellation. Use realistic values for accurate results.")
st.write("With this application, you can predict if your hotel booking will be canceled or not and save your time!")

no_of_adults = st.number_input("Number of Adults", min_value=1, value=1)
no_of_children = st.number_input("Number of Children", min_value=0, value=0)
no_of_weekend_nights = st.number_input("Number of Weekend Nights", min_value=0, value=0)
no_of_week_nights = st.number_input("Number of Week Nights", min_value=0, value=0)
type_of_meal_plan = st.selectbox("Meal Plan", list(meal_map.keys()))
required_car_parking_space = st.number_input("Car Parking Space Required", min_value=0, value=0)
room_type_reserved = st.selectbox("Room Type Reserved", list(room_map.keys()))
lead_time = st.number_input("Lead Time (Days)", min_value=0, value=0)
arrival_year = st.number_input("Arrival Year", min_value=2000, value=2025)
arrival_month = st.number_input("Arrival Month", min_value=1, max_value=12, value=1)
arrival_date = st.number_input("Arrival Date", min_value=1, max_value=31, value=1)
market_segment_type = st.selectbox("Market Segment Type", list(market_map.keys()))
repeated_guest = st.number_input("Repeated Guest", min_value=0, value=0)
no_of_previous_cancellations = st.number_input("Previous Cancellations", min_value=0, value=0)
no_of_previous_bookings_not_canceled = st.number_input("Previous Bookings Not Canceled", min_value=0, value=0)
avg_price_per_room = st.number_input("Average Price per Room", min_value=0.0, value=0.0)
no_of_special_requests = st.number_input("Special Requests", min_value=0, value=0)

if st.button("Predict Cancellation"):
    # Create a dictionary of input values
    input_data = {
        'no_of_adults': no_of_adults,
        'no_of_children': no_of_children,
        'no_of_weekend_nights': no_of_weekend_nights,
        'no_of_week_nights': no_of_week_nights,
        'type_of_meal_plan': meal_map.get(type_of_meal_plan, default_map.get('type_of_meal_plan', 0)),
        'required_car_parking_space': required_car_parking_space,
        'room_type_reserved': room_map.get(room_type_reserved, default_map.get('room_type_reserved', 0)),
        'lead_time': lead_time,
        'arrival_year': arrival_year,
        'arrival_month': arrival_month,
        'arrival_date': arrival_date,
        'market_segment_type': market_map.get(market_segment_type, default_map.get('market_segment_type', 0)),
        'repeated_guest': repeated_guest,
        'no_of_previous_cancellations': no_of_previous_cancellations,
        'no_of_previous_bookings_not_canceled': no_of_previous_bookings_not_canceled,
        'avg_price_per_room': avg_price_per_room,
        'no_of_special_requests': no_of_special_requests
    }

    # Convert input data to a DataFrame
    input_df = pd.DataFrame([input_data], columns=expected_columns)

    # Scale numerical columns
    input_df[numerical_cols] = scaler.transform(input_df[numerical_cols])

    # Make prediction
    prediction = model.predict(input_df)[0]
    prediction_proba = model.predict_proba(input_df)[0][1]
    # Display result
    if prediction == 1:
        st.error(f"The booking is likely to be canceled, with a prediction probability of {prediction_proba:.2f}.")
    else:
        st.success(f"The booking is not likely to be canceled, with a prediction probability of {prediction_proba:.2f}.")
