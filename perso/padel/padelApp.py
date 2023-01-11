

# %%
import pandas as pd
import numpy as np
import pydeck as pdk


# %%
import streamlit as st
chart_data = pd.read_csv("./listPadelsCleaned.csv")
chart_data['lon'] = chart_data['latitude'] 
chart_data['lat'] = chart_data['longitude']
chart_data.drop(columns=['longitude'])
chart_data.drop(columns=['latitude'])
#chart_data['temp']=chart_data['lon']
#chart_data.drop(columns=['lon'])
#chart_data['lon'] = chart_data['lat']
#chart_data.drop(columns=['lat'])
#chart_data['lat']=chart_data['temp']
#chart_data.drop(columns=['temp'])

# %%
st.title('Etude de marché du Padel en France')
st.title('Répartition des terrains de Padel en France')

# %%
st.map(chart_data, use_container_width=True)

# %%
st.title('Densité de terrains par habitants (5 kms)')
kms = st.radio(
    "Rayon de calcul du nombre de terrains par habitant",
    ('5 kms', '10 kms', '15 kms', '20 kms', '25 kms', '30 kms'))
chart_data2 = pd.read_csv("padelDensity.csv")
HEADER = ["lng", "lat", "weight"]
chart_data2['temp'] = chart_data2['lng']
chart_data2['lng']=chart_data2['lat']
chart_data2['lat']=chart_data2['temp']
chart_data2.drop(columns=['temp'])
kms = int(kms.split(' ')[0])
weight = []
if kms == 5:
    chart_data2['weight']=chart_data2['den5']
if kms == 10:
    chart_data2['weight']=chart_data2['den10']
if kms == 15:
    chart_data2['weight']=chart_data2['den15']
if kms == 20:
    chart_data2['weight']=chart_data2['den20']
if kms == 25:
    chart_data2['weight']=chart_data2['den25']
if kms == 30:
    chart_data2['weight']=chart_data2['den30']
for i in range(len(chart_data2)):
    if chart_data2.iloc[i]['PTOT'] == 0:
        weight.append(0)
    else:
        if kms == 5:
            weight.append(chart_data2.iloc[i]['den5']/chart_data2.iloc[i]['PTOT'])
        if kms == 10:
            weight.append(chart_data2.iloc[i]['den10']/chart_data2.iloc[i]['PTOT'])
        if kms == 15:
            weight.append(chart_data2.iloc[i]['den15']/chart_data2.iloc[i]['PTOT'])
        if kms == 20:
            weight.append(chart_data2.iloc[i]['den20']/chart_data2.iloc[i]['PTOT'])
        if kms == 25:
            weight.append(chart_data2.iloc[i]['den25']/chart_data2.iloc[i]['PTOT'])
        if kms == 30:
            weight.append(chart_data2.iloc[i]['den30']/chart_data2.iloc[i]['PTOT'])
chart_data2['weight']= weight

view = pdk.data_utils.compute_view(chart_data2[["lng", "lat"]])
view.zoom = 4
view.min_zoom = 4
view.max_zoom = 7

density = pdk.Layer(
    "HeatmapLayer",
    data=chart_data2,
    opacity=10,
    get_position=["lng", "lat"],
    aggregation=pdk.types.String("MEAN"),
    threshold=0.05,
    get_weight="weight",
    pickable=True,
    weightsTextureSize=1024,
)

r = pdk.Deck(
    layers=[density],
    initial_view_state=view,
    map_provider="mapbox",
    map_style="mapbox://styles/mapbox/light-v11",
    tooltip={"text": "Concentration in Padels"},
)


st.pydeck_chart(r,use_container_width=False)

st.title('Données utitlisées')
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.dataframe(chart_data2.drop(columns=['temp','weight','DEPCOM','COM','PMUN','PCAP','PTOT','lng','lat']))


