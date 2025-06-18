import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

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
        Statistiques des débits
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
    multi = '''**Plage de données max** : 1950-2025   
*Certaines stations ne disposent pas d'une plage de données aussi étendue.*  
En un clic, retrouvez les statistiques (mini, max, moyenne, médiane) des stations de débits françaises ! 
3 onglets possibles : la carte, le tableau de données et comparaisons sous forme de diagramme en boîte.
Pour des raisons d'hébergement, seules les stations du département de la Corrèze sont présentes dans le tableau de données et dans les comparaisons. 
'''
    st.markdown(multi)

################################################ CONTENU
carte1_path = os.path.join("data", "carte_stats_cluster.html")

# Filtres
st.sidebar.header("Filtres")

# Onglets
tab1, tab2, tab3 = st.tabs(["Carte", "Tableau de données", "Comparaisons"])

# Onglet 1: Carte
with tab1:
    with open(carte1_path, "r", encoding="utf-8") as f:
        html_content1 = f.read()
    st.components.v1.html(html_content1, height=600, scrolling=True)

# Onglet 2: Tableau
with tab2:
    # Fonction pour charger les données avec le cache Streamlit
    @st.cache_data
    def load_data():
        data_path = os.path.join("data", "stats_hydro3_correze.csv")
        return pd.read_csv(data_path, sep=None, engine='python')

    # Chargement des données
    df = load_data()

    st.write(df)

#################################
# --------- ONGLET 3 : COMPARAISON PAR STATION (BOXPLOT STYLE PX)
with tab3:
    st.subheader("Comparaison des débits par station (boxplot synthétique)")

    # Sélection de stations
    selected_stations = st.multiselect(
        "Sélectionner une ou plusieurs stations",
        options=df["station"],
        placeholder="Aucune station sélectionnée",
        max_selections=5
    )

    if selected_stations:
        import plotly.express as px
        import pandas as pd

        selected_data = df[df["station"].isin(selected_stations)]

        # Préparation des données pour px.box : on "déplie" les quantiles
        melted_data = pd.melt(
            selected_data,
            id_vars=["station", "riviere"],
            value_vars=["0.05", "0.25", "mediane", "0.75", "0.95"],
            var_name="Quantile",
            value_name="Débit (m³/s)"
        )

        fig = px.box(
            melted_data,
            x="station",
            y="Débit (m³/s)",
            color="station",  # <- ici on met "station" à la place de "riviere"
            points=False,
            labels={
                "station": "Station",
                "riviere": "Rivière",
                "Débit (m³/s)": "Débit (m³/s)"
            },
            title="Distribution synthétique des débits par station"
        )

        fig.update_layout(
            xaxis=dict(title="", fixedrange=True),
            yaxis=dict(fixedrange=True),
            dragmode=False,
            hovermode=False,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="left",
                x=0.5
            )
        )

        fig.update_traces(quartilemethod="inclusive")
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Veuillez sélectionner au moins une station pour afficher le graphique.")

