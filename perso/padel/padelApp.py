

# %%
import pandas as pd
import numpy as np
import pydeck as pdk
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd
import streamlit as st

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)

conn = connect(credentials=credentials)

def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

sheet_url_padelList = st.secrets["private_gsheets_url_padelList"]
padelList = run_query(f'SELECT * FROM "{sheet_url_padelList}"') 

sheet_url_padelDensity = st.secrets["private_gsheets_url_padelDensity"]
densityPadel = run_query(f'SELECT * FROM "{sheet_url_padelDensity}"')

sheet_url_communes = st.secrets["private_gsheets_url_communes"]
communes = run_query(f'SELECT * FROM "{sheet_url_communes}"')

len(densityPadel)
DEPCOM = []
COM = []
PMUN = []
PCAP = []
PTOT = []
Nom_commune = []
Code_postal = []
coordonnees_gps = []
lng = []
lat = []
den5 = []
den10 = []
den15 = []
den20 = []
den25 = []
den30 = []
nb5 = []
nb10 = []
nb15 = []
nb20 = []
nb25 = []
nb30 = []
for i in range(len(densityPadel)):
    DEPCOM.append(densityPadel[i][0])
    COM.append(densityPadel[i][1])
    PMUN.append(densityPadel[i][2])
    PCAP.append(densityPadel[i][3])
    PTOT.append(int(densityPadel[i][4]))
    Nom_commune.append(densityPadel[i][5])
    Code_postal.append(densityPadel[i][6])
    coordonnees_gps.append(densityPadel[i][7])
    lng.append(float(densityPadel[i][8]))
    lat.append(float(densityPadel[i][9]))
    den5.append(float(densityPadel[i][10]))
    den10.append(float(densityPadel[i][11]))
    den15.append(float(densityPadel[i][12]))
    den20.append(float(densityPadel[i][13]))
    den25.append(float(densityPadel[i][14]))
    den30.append(float(densityPadel[i][15]))
    nb5.append(int(densityPadel[i][16]))
    nb10.append(int(densityPadel[i][17]))
    nb15.append(int(densityPadel[i][18]))
    nb20.append(int(densityPadel[i][19]))
    nb25.append(int(densityPadel[i][20]))
    nb30.append(int(densityPadel[i][21]))
dfDensity = pd.DataFrame(DEPCOM, columns=['DEPCOM'])
dfDensity['COM'] = COM
dfDensity['PMUN'] = PMUN
dfDensity['PCAP'] = PCAP
dfDensity['PTOT'] = PTOT
dfDensity['Nom_commune'] = Nom_commune 
dfDensity['Code_postal'] = Code_postal
dfDensity['coordonnees_gps'] = coordonnees_gps
dfDensity['lng'] = lng
dfDensity['lat'] = lat
dfDensity['den5'] = den5
dfDensity['den10'] = den10
dfDensity['den15'] = den15
dfDensity['den20'] = den20
dfDensity['den25'] = den25 
dfDensity['den30'] = den30
dfDensity['nb5'] = nb5
dfDensity['nb10'] = nb10
dfDensity['nb15'] = nb15
dfDensity['nb20'] = nb20
dfDensity['nb25'] = nb25
dfDensity['nb30'] = nb30

Name = []
address = []
business_status = []
latitude = []
longitude = []
coordonnees_gps = []
for i in range(len(padelList)):
    Name.append(padelList[i][0])
    address.append(padelList[i][1])
    business_status.append(padelList[i][2])
    latitude.append(float(padelList[i][3]))
    longitude.append(float(padelList[i][4]))
    coordonnees_gps.append(padelList[i][5])
dfPadelList = pd.DataFrame(Name, columns=['Name'])
dfPadelList['address'] = address
dfPadelList['business_status'] = business_status
dfPadelList['lat'] = longitude
dfPadelList['lon'] = latitude
dfPadelList['coordonnees_gps'] = coordonnees_gps

Niveau_de_vie_Commune = []
Niveau_de_vie_Departement = []
PTOT = []
Nom_commune = []
Code_postal = []
coordonnees_gps = []
lng = []
lat = []
for i in range(len(communes)):
    Niveau_de_vie_Commune.append(float(communes[i][0]))
    Niveau_de_vie_Departement.append(float(communes[i][1]))
    PTOT.append(int(float(communes[i][2])))
    Nom_commune.append(communes[i][3])
    Code_postal.append(int(float(communes[i][4])))
    coordonnees_gps.append(communes[i][5])
    lng.append(float(communes[i][6]))
    lat.append(float(communes[i][7]))
dfCommunes = pd.DataFrame(Niveau_de_vie_Commune, columns=['Niveau_de_vie_Commune'])
dfCommunes['Niveau_de_vie_Departement'] = Niveau_de_vie_Departement
dfCommunes['PTOT'] = PTOT
dfCommunes['Nom_commune'] = Nom_commune
dfCommunes['Code_postal'] = Code_postal
dfCommunes['coordonnees_gps'] = coordonnees_gps
dfCommunes['lng'] = lng
dfCommunes['lat'] = lat

# %%

chart_data = dfPadelList
#chart_data['lat'] = chart_data['latitude'] 
#chart_data['lon'] = chart_data['longitude']
#chart_data.drop(columns=['longitude'])
#chart_data.drop(columns=['latitude'])
#chart_data['temp']=chart_data['lon']
#chart_data.drop(columns=['lon'])
#chart_data['lon'] = chart_data['lat']
#chart_data.drop(columns=['lat'])
#chart_data['lat']=chart_data['temp']
#chart_data.drop(columns=['temp'])

# %%
st.title('Etude de marché du Padel en France')
st.title('Carte des terrains de Padel en France')

# %%
st.map(chart_data, use_container_width=True)

# %%
st.title('Densité de terrains par habitants')
kms = st.radio(
    "Rayon de calcul du nombre de terrains par habitant",
    ('5 kms', '10 kms', '15 kms', '20 kms', '25 kms', '30 kms'))
chart_data2 = dfDensity
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
    weightsTextureSize=4096,
)

r = pdk.Deck(
    layers=[density],
    initial_view_state=view,
    map_provider="mapbox",
    map_style="mapbox://styles/mapbox/light-v11",
    tooltip={"text": "Concentration in Padels"},
)


st.pydeck_chart(r,use_container_width=False)

st.title('Données densité')
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """
# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.dataframe(chart_data2.drop(columns=['temp','weight','DEPCOM','COM','PMUN','PCAP','lng','lat']))

st.title('Données communes')
st.markdown('Le revenu disponible par unité de consommation (UC), également appelé \"niveau de vie\", est le revenu disponible par \"équivalent adulte\". Il est calculé en rapportant le revenu disponible du ménage au nombre d\'unités de consommation qui le composent. Toutes les personnes rattachées au même ménage fiscal ont le même revenu disponible par UC (ou niveau de vie)')
st.dataframe(dfCommunes.drop(columns=['coordonnees_gps','lng','lat']))

