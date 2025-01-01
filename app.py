import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load the model and dataset
model = pickle.load(open('price_prediction.pkl', 'rb'))
dataset = pickle.load(open('dataset.pkl', 'rb'))

# Extract location columns and clean location names
location_columns = dataset.columns[dataset.columns.str.startswith('location_')]
locations = location_columns.str.replace('location_', '')

# Streamlit UI
st.title("House Price Prediction")

# UI elements
location = st.selectbox('Location', locations)

# Set default sqft values based on BHK
def get_default_sqft(bhk):
    if bhk == 1:
        return 500.0
    elif bhk == 2:
        return 1000.0
    elif bhk == 3:
        return 1500.0
    elif bhk == 4:
        return 2000.0
    elif bhk == 5:
        return 2500.0
    else:
        return 3000.0

# UI elements with dynamic sqft default
bhk = st.number_input('Enter BHK (e.g., 1, 2, 3...)', min_value=1, max_value=6, value=2)
sqft = st.number_input('Total Square Foot', min_value=0.0, value=get_default_sqft(bhk), step=100.0)

# Adjust sqft value based on bhk input
def update_sqft_based_on_bhk():
    st.session_state.sqft = get_default_sqft(st.session_state.bhk)

st.session_state.bhk = bhk
st.session_state.sqft = sqft

# Prediction
if st.button('Predict'):
    input_data = pd.DataFrame([[bhk, sqft] + [0] * len(location_columns)], 
                              columns=['bhk', 'sqft'] + list(location_columns))
    input_data['location_' + location] = 1
    prediction = model.predict(input_data)[0]
    st.write(f"The predicted price is {prediction:.2f} lakhs")
