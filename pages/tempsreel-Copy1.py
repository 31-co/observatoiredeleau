import streamlit as st
import pandas as pd
import requests
import os
import plotly.express as px
from datetime import datetime

################################################ TOOLBAR
hide_streamlit_style = """
    <style>
        /* Masquer l'en-tête et le menu de Streamlit */
        header {visibility: hidden;}
        /* Masquer une classe spécifique identifiée */
        .st-emotion-cache-uf99v8 {display: none;}
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown("""
    <style>
        .fake-navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 60px;
            background-color: #aad3df;
            color: white;
            display: flex;
            align-items: center;
            justify-content: flex-end; /* Aligner le texte à droite */
            font-size: 24px;
            font-weight: bold;
            z-index: 9999;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding-right: 20px; /* Un peu d'espace à droite */
        }
    </style>
""", unsafe_allow_html=True)

# HTML de la fausse navbar
st.markdown('<div class="fake-navbar">Observatoire de l\'eau</div>', unsafe_allow_html=True)

###################################################### DONNEES TITRE STYLE CONTENEUR

st.markdown("""
    <h1 style='text-align: center; color: inherit; margin: 0; padding: 0; margin-top: -50px;'>
        Données en temps réel
    </h1>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    .st-key-monconteneur {background-color: #e9ecef; padding: 20px; border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True)


######################################################## CONTENEUR
with st.container(key="monconteneur"):
    multi = '''**Plage de données max** : 30 derniers jours    
Débits et hauteurs d'eau en temps réel : possibilité d'intégrer plusieurs stations.
 
'''
    st.markdown(multi)



##############################
@st.cache_data
def load_data():
    data_path = os.path.join("data", "stations_simple.csv") 
    return pd.read_csv(data_path, sep=None, engine='python')

station_info_df = load_data()

##############################
tab1, tab2 = st.tabs(["Débits", "Hauteurs d'eau"])

with tab1:
    selected_stations = st.multiselect(
        "Sélectionner/écrire une ou plusieurs stations",
        station_info_df['libelle_station'],
        placeholder="Aucune option sélectionnée", max_selections=5, key="selectboxQ"
    )
    
    if selected_stations:
        all_data = []
    
        for station in selected_stations:
            station_code = station_info_df.loc[
                station_info_df['libelle_station'] == station, 'code_station'
            ].values[0]
    
            url = f"http://www.vigicrues.gouv.fr/services/observations.json?CdStationHydro={station_code}"
            params = {'GrdSerie': 'Q', 'FormatDate': 'iso'}
    
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
    
                observations = data.get("Serie", {}).get("ObssHydro", [])
                if not observations:
                    st.warning(f"Pas de données en débit pour la station : {station}")
                    continue
    
                df = pd.DataFrame(observations)
                df["DtObsHydro"] = pd.to_datetime(df["DtObsHydro"], errors="coerce")
                df["Débit (m³/s)"] = df["ResObsHydro"]
                df["Station"] = station
    
                all_data.append(df[["DtObsHydro", "Débit (m³/s)", "Station"]])
    
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors de la récupération des données pour {station} : {e}")
            except KeyError:
                st.warning(f"Données manquantes pour {station}.")
        
        if all_data:
            full_df = pd.concat(all_data, ignore_index=True)
    
            fig = px.line(
                full_df,
                x="DtObsHydro",
                y="Débit (m³/s)",
                color="Station",
                title="Évolution du débit (m³/s) - Stations sélectionnées"
            )
            fig.update_layout(
            xaxis_title="",
            yaxis_title="",
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True),
            dragmode=False,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.35,
                xanchor="left",
                x=0
                )
            )
    
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    selected_stations = st.multiselect(
        "Sélectionner/écrire une ou plusieurs stations",
        station_info_df['libelle_station'],
        placeholder="Aucune option sélectionnée", max_selections=5, key="selectboxH"
    )
    
    if selected_stations:
        all_data = []
    
        for station in selected_stations:
            station_code = station_info_df.loc[
                station_info_df['libelle_station'] == station, 'code_station'
            ].values[0]
    
            url = f"http://www.vigicrues.gouv.fr/services/observations.json?CdStationHydro={station_code}"
            params = {'GrdSerie': 'H', 'FormatDate': 'iso'}
    
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()
    
                observations = data.get("Serie", {}).get("ObssHydro", [])
                if not observations:
                    st.warning(f"Pas de données en hauteur pour la station : {station}")
                    continue
    
                df = pd.DataFrame(observations)
                df["DtObsHydro"] = pd.to_datetime(df["DtObsHydro"], errors="coerce")
                df["Hauteur"] = df["ResObsHydro"]
                df["Station"] = station
    
                all_data.append(df[["DtObsHydro", "Hauteur", "Station"]])
    
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors de la récupération des données pour {station} : {e}")
            except KeyError:
                st.warning(f"Données manquantes pour {station}.")
        
        if all_data:
            full_df = pd.concat(all_data, ignore_index=True)
    
            fig = px.line(
                full_df,
                x="DtObsHydro",
                y="Hauteur",
                color="Station",
                title="Hauteur d'eau (m) - Stations sélectionnées"
            )
            fig.update_layout(
            xaxis_title="",
            yaxis_title="",
            xaxis=dict(fixedrange=True),
            yaxis=dict(fixedrange=True),
            dragmode=False,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.35,
                xanchor="left",
                x=0
                )
            )
    
            st.plotly_chart(fig, use_container_width=True)
    
    