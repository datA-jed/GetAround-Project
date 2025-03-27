import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np


### Config
st.set_page_config(
    page_title="GetAround Dashboard",
    page_icon="🚗",
    layout="wide"
)

DATA_URL = "https://raw.githubusercontent.com/datA-jed/GetAround-Project/refs/heads/main/dashboard/processed_data.json"

st.title(":green[_Analysis_] of late checkout impact 🚗")

st.subheader("Context")
st.markdown("""
:blue[_GetAround is a car-sharing service that allows you to rent cars from people nearby. It's like the Airbnb of cars.
            When renting a car, users have to complete checkin flow at the beginning of the rental and a checkout flow at the end of the rental.
            The checkin and checkout can be done with distinct flows like the mobile app, connected car or paper form._]
""")


with st.expander("Video is better than a lot of words  📺"):
    st.video("https://www.youtube.com/watch?v=3LyzwpGSfzE")


st.subheader("Goal of this analysis")
st.markdown("""
:blue[What is the goal of this dashboard analysis?
            When using GetAround, drivers book a car for a specific period, from an hour to a few days long.
            They are suppose to bring back the car on time but it happens that they are late.
        Late returns are a problem for GetAround because it can impact the next driver who booked the car and also the car owner.]
""")



@st.cache_data
def load_data(nrows):
    data = pd.read_json(DATA_URL)
    return data.head(nrows)

st.subheader("Let's start by loading the data")
st.markdown("""
    _This dataset is a sample of 5000 rentals but the whole analysis is made with 21 310 rentals.
    The data are completly processed for this analysis_
    """)

data = load_data(21310)
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)



st.subheader("Interesting Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Number of cars", data["car_id"].nunique())
col2.metric("Number of rentals", data["rental_id"].nunique())
col3.metric("Number of Connect Checkin", (data["checkin_type"]=='connect').sum())