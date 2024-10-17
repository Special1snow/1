import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data with error handling
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        st.error("The file is empty.")
    except pd.errors.ParserError:
        st.error("There was an issue parsing the file. Check the format.")
    return None

# Process data with proper checks
def process_data(data):
    if data is None or data.empty:
        st.error("Data is not available or empty.")
        return None

    # Ensure necessary columns exist
    required_columns = ['Role', 'Year', 'Female_Ratio']
    if not all(column in data.columns for column in required_columns):
        st.error(f"Missing columns. Expected: {required_columns}")
        return None

    # Calculate female ratio (ensure no division by zero)
    try:
        female_ratio = data.groupby('Role')['Female_Ratio'].mean()
    except ZeroDivisionError:
        st.error("Error calculating female ratio: Division by zero.")
        return None

    return female_ratio

# File upload for user interaction
st.title("HR Dashboard")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    data = load_data(uploaded_file)
    female_ratio = process_data(data)

    if female_ratio is not None:
        st.line_chart(female_ratio)

        # Visualize with a pie chart if year 2024 data exists
        if 'Year' in data.columns and 2024 in data['Year'].values:
            year_2024_data = data[data['Year'] == 2024]
            st.pie_chart(year_2024_data['Female_Ratio'])
