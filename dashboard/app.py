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

st.title("GetAround Dashboard :green[_Analysis_] 🚗")

st.markdown("""
This app is a dashboard for the GetAround project. 
""")

with st.expander("Watch this video to understand the concept of GetAround  📺"):
    st.video("https://www.youtube.com/watch?v=3LyzwpGSfzE")

@st.cache_data
def load_data(nrows):
    data = pd.read_json(DATA_URL)
    return data.head(nrows)

st.subheader("GetaRound Data Analysis")
st.markdown("_This dataset contains information about the GetAround project_")
data = load_data(5000)
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)