import streamlit as st
import os
import base64

logo_path = "static/goutte.png"
st.set_page_config(page_title="Observatoire de l'eau", page_icon=logo_path, layout="wide")

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
        Accueil
    </h1>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    .st-key-monconteneur {background-color: #e9ecef; padding: 20px; border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True)
    
######## AUTRES ####### page_icon=":material/water_drop:"

st.write("""
L'observatoire de l'eau vous permettra d'analyser les débits des rivières françaises !
Les données sont exprimées en m3/s afin de permettre des comparaisons entre stations. Toutefois, certaines stations ne disposent pas de relevés de débit et ne seront donc pas accessibles dans ce programme.
L'historique des débits est limité à 30 ans afin d'optimiser le chargement des données. Certaines stations peuvent ne pas disposer d’un historique aussi étendu.

**Outils utilisés :**
- Langage : Python
- Bibliothèques : Streamlit, Pandas, Requests, Plotly  
*(L’interactivité de certains graphiques Plotly a été désactivée pour une meilleure fluidité, notamment sur smartphone.)*
""")

st.write("""
**Sources des données** :
- Vigicrues : [https://www.vigicrues.gouv.fr/](https://www.vigicrues.gouv.fr/)
- Hubeau : [https://hubeau.eaufrance.fr/](https://hubeau.eaufrance.fr/)
- Météo-France : [https://meteofrance.com/](https://meteofrance.com/)
""")

st.write("""
**Avertissement** :
Aucune vérification de la plausibilité des données n'a été effectuée. Toute responsabilité quant à leur utilisation est déclinée.
""")      


st.write("""
**Pour plus d'informations :**
[LinkedIn](https://www.linkedin.com/in/yohan-germain-068320346/)
""")

