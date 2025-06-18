import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime, timedelta
from io import StringIO
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
        Historique des débits
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
Hitorique des débits sur 50 ans max et statistiques correspondant à la période. Choisissez votre station !
'''
    st.markdown(multi)

#####################################################
# --------- CHARGEMENT DES DONNÉES
@st.cache_data
def load_station_info():
    path = os.path.join("data", "stations_simple.csv")
    return pd.read_csv(path, sep=None, engine='python')
    
station_info_df = load_station_info()

# Sélection de la station
selected_station = st.selectbox("", station_info_df['libelle_station'])

# Si aucune station n'est sélectionnée, arrêter ici
if selected_station == "Sélectionner/écrire le nom de la station":
    st.write("Aucune station sélectionnée.")
    st.stop()

# Récupérer le code de la station sélectionnée
station_code = station_info_df[station_info_df['libelle_station'] == selected_station]['code_station'].values[0]

# Définir les dates pour les filtres
now = datetime.now().astimezone()
date_debut_all = "1975-01-01"
date_debut_10years = (now - timedelta(days=3650)).strftime("%Y-%m-%d")
date_debut_year = (now - timedelta(days=365)).strftime("%Y-%m-%d")

# Filtres de période
st.subheader("Filtrer par période (1 an par défaut)")
col1, col2, col3 = st.columns(3)

with col1:
    last_year = st.button("1 an")
with col2:
    last_10years = st.button("10 ans")
with col3:
    all_time = st.button("Tout afficher")

# Déterminer la période en fonction du filtre sélectionné
if last_year:
    date_debut = date_debut_year
elif last_10years:
    date_debut = date_debut_10years
elif all_time:
    date_debut = date_debut_all
else:
    date_debut = date_debut_year  # Par défaut, 1 an

# Définir la taille maximale des résultats pour accélérer les requêtes
size_limit = 2000 if date_debut == date_debut_year else 10000 if date_debut == date_debut_10years else 20000

# Fonction pour récupérer les données avec mise en cache
@st.cache_data(ttl=600)  # Cache les données pendant 10 minutes
def get_hydro_data(station_code, date_debut, size_limit):
    url = "https://hubeau.eaufrance.fr/api/v2/hydrometrie/obs_elab.csv"
    params = {
        "code_entite": station_code,
        "date_debut_obs_elab": date_debut,
        "grandeur_hydro_elab": "QmnJ",
        "size": size_limit
    }
    headers = {"accept": "text/csv"}
    
    response = requests.get(url, params=params, headers=headers)
    if response.status_code not in (200, 206):
        raise requests.exceptions.RequestException(f"Erreur {response.status_code}: {response.text}")

    try:
        df = pd.read_csv(StringIO(response.text), sep=";")
        if df.empty:
            raise pd.errors.EmptyDataError("Le fichier CSV est vide.")
        df = df[["date_obs_elab", "resultat_obs_elab"]].rename(columns={"resultat_obs_elab": "debit"})
        df["debit"] = df["debit"] / 1000  # Conversion l/s en m³/s
        df["date_obs_elab"] = pd.to_datetime(df["date_obs_elab"], errors="coerce")
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError("Pas de donnée en débit pour cette station.")
    except KeyError:
        raise KeyError("Les colonnes attendues sont manquantes dans le fichier CSV.")
    
    return df

try:
    # Charger les données avec cache
    df = get_hydro_data(station_code, date_debut, size_limit)

    # Vérifier si les données existent
    if df.empty:
        st.warning("Aucune donnée disponible pour cette période.")
        st.stop()

    # Calcul des statistiques optimisé
    stats = df["debit"].agg(["min", "max", "mean"])
    min_debit, max_debit, annual_mean = stats["min"], stats["max"], stats["mean"]

    # Dates associées aux min/max
    min_debit_date = df.loc[df["debit"].idxmin(), "date_obs_elab"].strftime('%d/%m/%Y')
    max_debit_date = df.loc[df["debit"].idxmax(), "date_obs_elab"].strftime('%d/%m/%Y')

    # Ajout de la colonne mois pour la moyenne mensuelle
    df["month"] = df["date_obs_elab"].dt.month
    monthly_mean = df.groupby("month")["debit"].mean()

    # Création du graphique principal
    fig = px.line(
        df, x="date_obs_elab", y="debit",
        title=f"Historique des débits, station : {selected_station} ({station_code})",
        labels={"date_obs_elab", "debit"}
    )
    fig.update_layout(
    xaxis=dict(fixedrange=True),  # Désactive le zoom sur l'axe X
    yaxis=dict(fixedrange=True),  # Désactive le zoom sur l'axe Y
    dragmode=False,               # Désactive le drag
    hovermode=False               # Désactive le hover
    )
    st.plotly_chart(fig, use_container_width=True)

    # Affichage des statistiques
    st.subheader("Statistiques sur la période")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Moyenne", f"{annual_mean:.2f} m³/s")
    with col2:
        st.metric("Débit minimum", f"{min_debit:.2f} m³/s", f"Date: {min_debit_date}", delta_color="inverse")
    with col3:
        st.metric("Débit maximum", f"{max_debit:.2f} m³/s", f"Date: {max_debit_date}")

except pd.errors.EmptyDataError as e:
    st.error(f"{e} Veuillez sélectionner une autre station.")
    st.stop()
except KeyError as e:
    st.error("Pas de donnée en débit pour cette station. Veuillez sélectionner une autre station.")
    st.stop()
except requests.exceptions.RequestException as e:
    st.error(f"Erreur lors de la récupération des données : {e}")
    st.stop()
except Exception as e:
    st.error(f"Une erreur inattendue s'est produite : {e}")
    st.stop()
