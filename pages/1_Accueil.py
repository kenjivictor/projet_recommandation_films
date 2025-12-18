import streamlit as st
import pandas as pd
from st_clickable_images import clickable_images 
from streamlit_authenticator import Authenticate
import functions.utils as utils

st.set_page_config(page_title="Accueil", layout="wide")

# =========================================================
# AUTHENTIFICATION & SÉCURITÉ
# =========================================================
lesDonneesDesComptes = {
    'usernames': {
        'utilisateur': {'name':'utilisateur', 'password':'utilisateurMDP', 'email':'user@gmail.com', 'role':'user'},
        'root': {'name':'root', 'password':'rootMDP', 'email':'admin@gmail.com', 'role':'admin'}
    }
}

authenticator = Authenticate(lesDonneesDesComptes, "cookie_name", "cookie_key", 30)

if st.session_state.get("authentication_status") is not True:
    st.switch_page("main.py")


# BARRE LATÉRALE (SIDEBAR) PERSONNALISÉE

with st.sidebar:
    # 1. Le Titre et la description en PREMIER
    st.title("FilmDataLab")
    st.write("Une application de recommandation de films basée sur la data et l'IA.")
    st.divider()
    
    # 2. La Navigation Manuelle (C'est ici qu'on définit l'ordre)
    # Note: On ne met pas main.py ici, donc il reste caché.
    st.page_link("pages/1_Accueil.py", label="Accueil", icon="🏠")
    st.page_link("pages/3_Presentation.py", label="Presentation", icon="📊")
    st.page_link("pages/4_Recommandation.py", label="Recommandation", icon="🎬")
    st.page_link("pages/5_Recherche.py", label="Recherche", icon="🎞️")
    
    st.divider()
    
    # 3. Le bouton de déconnexion en DERNIER
    authenticator.logout("Déconnexion", "sidebar")

# LOGIQUE & DONNÉES

# On réinitialise le film choisi car on est sur l'accueil
st.session_state.selected_movie_id = None

@st.cache_data
def load_data():
    # Ajustez le chemin si nécessaire (ex: "../db/data_2.csv")
    df = pd.read_csv("db/data_2.csv")
    df['movieId'] = df['movieId'].astype(str)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Erreur : Fichier 'db/data_2.csv' introuvable.")
    st.stop()

# AFFICHAGE CONTENU PRINCIPAL

st.markdown("""
    <style>
        /* Cible le conteneur principal de la page pour remonter le contenu */
        .block-container {
            /* Met la marge intérieure haute à 0 */
            padding-top: 0rem !important; 
            padding-bottom: 0rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

st.header("Films à la une (Cliquez sur une affiche pour voir les détails)")

# Films à la une
df_sorted = df.sort_values(['startYear', 'averageRating'], ascending=False).head(5)
images_urls = [f"https://image.tmdb.org/t/p/w500{url}" for url in df_sorted['poster_path']]
titles = [t for t in df_sorted['primaryTitle']]

clicked_index = clickable_images(
    images_urls, 
    titles=titles,
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"height": "450px", "width": "auto", "display": "block", "margin": "auto", "object-fit": "cover", "border-radius": "10px", "cursor": "pointer"},
)

if clicked_index > -1:
    film_id = df_sorted.iloc[clicked_index]['movieId']
    st.session_state.selected_movie_id = film_id
    # Redirection vers la page de recommandation
    st.switch_page("pages/4_Recommandation.py")

utils.background_header_image()