import streamlit as st
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import numpy as np

DATA_URL = "https://raw.githubusercontent.com/datA-jed/GetAround-Project/refs/heads/main/processed_data.json"

def load_data(nrows):
    data = pd.read_json(DATA_URL)
    return data.head(nrows)

data = load_data(5000)

st.write(data)