import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
        Saisonnalité des débits
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
    multi = '''**Plage de données max** : 1975-2025   
*Certaines stations ne disposent pas d'une plage de données aussi étendue.*  
Rend compte du débit moyen observé en fonction du mois. Possibilité de comparer 2 stations.
 
'''
    st.markdown(multi)

####################################
# --------- CHARGEMENT DES DONNÉES
@st.cache_data
def load_station_info():
    path = os.path.join("data", "stations_simple.csv")
    return pd.read_csv(path, sep=None, engine='python')

@st.cache_data
def get_available_columns():
    path = os.path.join("data", "hydro3.csv")
    return pd.read_csv(path, nrows=0).columns.tolist()

station_info_df = load_station_info()
available_columns = get_available_columns()

##########################
col1, col2 = st.columns(2)

with col1:
    options = ["---"] + station_info_df['libelle_station'].tolist()
    station_season = st.selectbox(
        "Choisir une station pour l’analyse saisonnière",
        options,
        index=0, key = "saison1"
    )

    if station_season != "---":
        station_code = station_info_df.loc[
            station_info_df['libelle_station'] == station_season, 'code_station'
        ].values[0]

        if station_code not in available_columns:
            st.warning(f"Pas de données pour la station : {station_season}")
        else:
            hydro_path = os.path.join("data", "hydro3.csv")
            df = pd.read_csv(hydro_path, usecols=["date_obs_elab", station_code])
            df["date_obs_elab"] = pd.to_datetime(df["date_obs_elab"], errors="coerce")
            df.rename(columns={station_code: "Débit (m³/s)"}, inplace=True)
            df.dropna(subset=["Débit (m³/s)"], inplace=True)

            df["month"] = df["date_obs_elab"].dt.month

            monthly_stats = df.groupby("month")["Débit (m³/s)"].agg([
                "median", 
                lambda x: x.quantile(0.05), 
                lambda x: x.quantile(0.25), 
                lambda x: x.quantile(0.75), 
                lambda x: x.quantile(0.95)
            ]).reset_index()
            
            monthly_stats.columns = ["month", "median", "low_whisker", "q1", "q3", "high_whisker"]

            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=monthly_stats["month"],
                open=monthly_stats["q1"],
                close=monthly_stats["q3"],
                low=monthly_stats["low_whisker"],
                high=monthly_stats["high_whisker"],
                increasing_line_color='blue',
                decreasing_line_color='blue'
            ))

            fig.update_layout(
                title=f"{station_season}",
                xaxis=dict(
                    tickmode="array", 
                    tickvals=list(range(1, 13)), 
                    ticktext=["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
                ),
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Veuillez sélectionner une station pour afficher l'analyse saisonnière.")

with col2:
    options = ["---"] + station_info_df['libelle_station'].tolist()
    station_season = st.selectbox(
        "Choisir une station pour l’analyse saisonnière",
        options,
        index=0, key = "saison2"
    )

    if station_season != "---":
        station_code = station_info_df.loc[
            station_info_df['libelle_station'] == station_season, 'code_station'
        ].values[0]

        if station_code not in available_columns:
            st.warning(f"{station_season}")
        else:
            hydro_path = os.path.join("data", "hydro3.csv")
            df = pd.read_csv(hydro_path, usecols=["date_obs_elab", station_code])
            df["date_obs_elab"] = pd.to_datetime(df["date_obs_elab"], errors="coerce")
            df.rename(columns={station_code: "Débit (m³/s)"}, inplace=True)
            df.dropna(subset=["Débit (m³/s)"], inplace=True)

            df["month"] = df["date_obs_elab"].dt.month

            monthly_stats = df.groupby("month")["Débit (m³/s)"].agg([
                "median", 
                lambda x: x.quantile(0.05), 
                lambda x: x.quantile(0.25), 
                lambda x: x.quantile(0.75), 
                lambda x: x.quantile(0.95)
            ]).reset_index()
            
            monthly_stats.columns = ["month", "median", "low_whisker", "q1", "q3", "high_whisker"]

            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=monthly_stats["month"],
                open=monthly_stats["q1"],
                close=monthly_stats["q3"],
                low=monthly_stats["low_whisker"],
                high=monthly_stats["high_whisker"],
                increasing_line_color='blue',
                decreasing_line_color='blue'
            ))

            fig.update_layout(
                title=f"{station_season}",
                xaxis=dict(
                    tickmode="array", 
                    tickvals=list(range(1, 13)), 
                    ticktext=["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Août", "Sep", "Oct", "Nov", "Déc"]
                ),
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Veuillez sélectionner une station pour afficher l'analyse saisonnière.")
