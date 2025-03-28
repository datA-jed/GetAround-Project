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

st.title(":green[_Analysis_] of late checkout impact :watch:")

st.subheader("Context  :car:")
st.markdown("""
:blue[_GetAround is a car-sharing service that allows you to rent cars from people nearby. It's like the Airbnb of cars.
            When renting a car, users have to complete checkin flow at the beginning of the rental and a checkout flow at the end of the rental.
            The checkin and checkout can be done with distinct flows like the mobile app, connected car or paper form._]
""")


with st.expander("Video is better than words :movie_camera:"):
    st.video("https://www.youtube.com/watch?v=3LyzwpGSfzE")


st.subheader("Goal of this analysis :dart:")
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

st.subheader("Let's start by loading the data :open_file_folder:")
st.markdown("""
    _This dataset is a sample of 21 310 rentals.
    The data are completly processed for this analysis_
    """)

data = load_data(21310)
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)



# Identifier les voitures avec au moins une location ayant une valeur dans previous_ended_rental_id
cars_with_previous_rentals = data[~data['previous_ended_rental_id'].isna()]['car_id'].unique()
# Nombre de voitures avec des locations précédentes
num_cars_with_previous_rentals = len(cars_with_previous_rentals)
# Nombre total de voitures uniques
total_unique_cars = data['car_id'].nunique()
# Calculer le pourcentage
percentage = round((num_cars_with_previous_rentals / total_unique_cars) * 100, 2)


st.subheader("Interesting Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total of unique cars", total_unique_cars, border=True)
col2.metric("Total of rentals", data["rental_id"].nunique(), border=True)
col3.metric("% of rented car more than 1 time  ", percentage, border=True)


col1, col2, col3 = st.columns(3)
col1.metric("Max time delta between two rentals (min)", (data["time_delta_with_previous_rental_in_minutes"].max()), border=True)
col2.metric("Mean time delta between two rentals (min)", (round(data["time_delta_with_previous_rental_in_minutes"].mean(), 2)), border=True)
col3.metric("Min time delta between two rentals (min)", (data["time_delta_with_previous_rental_in_minutes"].min()), border=True)
            
col1, col2 = st.columns(2)
col1.metric("Number of mobile Checkin", (data["checkin_type"]=='mobile').sum(), border=True)
col2.metric("Number of Connect Checkin", (data["checkin_type"]=='connect').sum(), border=True)


color_state_map = {
    'On Time Checkout': '#00CC96',    
    'Canceled': '#EF553B',         
    'Delayed Checkout': '#FFA15A',  
    'Unknown State': '#636EFA',   
    
}
col1, col2 = st.columns(2)
with col1:
    fig = px.pie(data, names='state', title='Checkout rental state', color='state', color_discrete_map=color_state_map)
    st.plotly_chart(fig)

with col2:
    fig = px.pie(data, names='checkin_type', title='Checkin type', color='checkin_type')
    st.plotly_chart(fig)    


color_impact_map = {
    'No Impact': '#00CC96',    
    'Canceletion': '#EF553B',         
    'Impacted': '#FFA15A',  
       
    
}
col1, col2 = st.columns(2)
with col1:
    fig = px.pie(data[data["impact_of_previous_rental_delay"]!="No previous rental informations"]
                 , names='impact_of_previous_rental_delay', title='Impact of previous rental delay', 
                 color='impact_of_previous_rental_delay', color_discrete_map=color_impact_map)
    st.plotly_chart(fig)

with col2:
    col2.metric("Average delay of previous rental (min)", (round(data["previous_rental_checkout_delay_in_minutes"].mean(), 2)), border=True)