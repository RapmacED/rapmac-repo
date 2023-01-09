

# %%
import pandas as pd
import numpy as np


# %%
import streamlit as st
chart_data = pd.read_csv("listPadelsCleaned.csv")
chart_data['lon'] = chart_data['longitude'] 
chart_data['lat'] = chart_data['latitude']
chart_data.drop(columns=['longitude'])
chart_data.drop(columns=['latitude'])
#chart_data['temp']=chart_data['lon']
#chart_data.drop(columns=['lon'])
#chart_data['lon'] = chart_data['lat']
#chart_data.drop(columns=['lat'])
#chart_data['lat']=chart_data['temp']
#chart_data.drop(columns=['temp'])

# %%
st.title('Répartition des terrains de Padel en France par Rapmac')

# %%
st.map(chart_data, use_container_width=True)

# %%



