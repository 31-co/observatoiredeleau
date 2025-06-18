import streamlit as st
import os
import base64

logo_path = "static/goutte.png"
st.set_page_config(page_title="Suivi Hydro", page_icon=logo_path, layout="wide")

##############
with st.sidebar:
    # Crée un espace vertical avec plusieurs st.write vides
    st.write("")
    st.write("")
    
    # Charge l'image
    with open(logo_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode()
    
    # Centre l'image dans la sidebar avec CSS
    st.markdown(
        f"""
        <style>
        .sidebar-logo {{
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }}
        .sidebar-logo img {{
            width: 70px;
        }}
        </style>
        <div class="sidebar-logo">
            <img src="data:image/png;base64,{img_base64}">
        </div>
        """,
        unsafe_allow_html=True
    )
    
######## AUTRES ####### page_icon=":material/water_drop:"
st.write("")
st.title("BIENVENUE")

st.title("À propos")

st.write("""
Les données sont exprimées en débit afin de permettre des comparaisons entre stations. Toutefois, certaines stations ne disposent pas de relevés de débit et ne seront donc pas accessibles dans ce programme.
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

