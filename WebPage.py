import streamlit as st
import pandas as pd
from webscrape import scrape_data
import os

file_path = 'output.csv'

# Set the page configuration
st.set_page_config(layout="wide")

def display_table():
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Add a header text box
    st.header("Consett Warriors Scheduled Fixtures (2024 to 2025)")

    # Create a styled HTML table
    styled_table = df.to_html(index=False, classes='styled-table')

    # Define custom CSS for the table
    custom_css = """
    <style>
    .styled-table th {
        font-size: 16px;
        font-weight: bold;
        color: Black;
        background-color: lightgrey;
        text-align: left;
    }
    .styled-table td {
        font-size: 14px;
    }
    </style>
    """

    # Display the custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Display the styled table in Streamlit
    st.markdown(styled_table, unsafe_allow_html=True)

if os.path.exists(file_path):
    display_table()
    # Add a refresh button
    if st.button("Refresh"):
        scrape_data()
        st.rerun()
else:
    scrape_data()
    st.rerun()