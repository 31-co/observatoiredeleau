import streamlit as st
import os
import time

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
carte1_path = os.path.join("data", "carte_crues_absolue.html")
carte2_path = os.path.join("data", "carte_crues_indic_moy.html")

st.markdown("""
    <h1 style='text-align: center; color: inherit; margin: 0; padding: 0; margin-top: -50px;'>
        La carte des crues
    </h1>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    .st-key-monconteneur {background-color: #e9ecef; padding: 20px; border-radius: 10px;}
    </style>
    """,
    unsafe_allow_html=True)


######################################################## CONTENU
with st.container(key="monconteneur"):
    multi = '''**Plage de données max** : 1950-2025   
*Certaines stations ne disposent pas d'une plage de données aussi étendue.*  
Plus d'informations sous la carte ! 
'''
    st.markdown(multi)

tab1, tab2 = st.tabs(["Valeurs", "Ratio max/moyenne"])

# Onglet 1 : Crue absolue
with tab1:
    with open(carte1_path, "r", encoding="utf-8") as f:
        html_content1 = f.read()
    st.components.v1.html(html_content1, height=600, scrolling=True)

# Onglet 2 : Indicateur
with tab2:
    with open(carte2_path, "r", encoding="utf-8") as f:
        html_content2 = f.read()
    st.components.v1.html(html_content2, height=600, scrolling=True)

################################################### INFOS+
with st.expander("**Détails**"):
    st.write('''
        L'onglet valeur montre le débit maximum exprimé en m3/s pour chaque station. Il mettra naturellement en avant les principaux fleuves français. La valeur maximale enregistrée est 10861 m3/s, enregistré le 12/03/2002 sur le Rhône à Tarascon.
        L'onglet ratio correspond quant à lui au rapport débit max enregistré/débit moyen de la station. Il met en avant les stations où l'intensité des crues est élevée. Le ratio max enregistrés est 905,2 sur la Loire à Cros-De-Georand (Ardèche) : 362 m3/s enregistrés le 17/10/2024 pour cette station dont le débit moyen est de à 0,4 m3/s !
    ''')
    st.write('''
        La date ayant enregistré le plus de record de crue (débit max) est la date du 15/02/1990. Ce jour-là, 39 stations ont enregistré leur débit max, sur une zone géographique très vaste allant du Lot jusqu'au Haut-Rhin ! 
    ''')