import streamlit as st
import pandas as pd
from st_clickable_images import clickable_images 
from streamlit_authenticator import Authenticate

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

with st.sidebar:
    st.title("Menu")
    st.write("🎬 Découvrez FilmDataLab")
    st.divider()
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

# AFFICHAGE

#initialisation de la bannière et du message d'accueil
#format de la bannnière

st.markdown("""
    <style>
        /* Cible le conteneur principal de la page */
        .block-container {
            /* Met la marge intérieure haute à 0 */
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Une application de recommandation de films basée sur la data et l'IA.</h1>", unsafe_allow_html=True)
        
try:
    st.image("pages/images/banner.png",  width='stretch')
except:
    st.warning("Image bannière introuvable")
st.subheader("Films à la une (Cliquez sur une affiche pour voir les détails)")

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
    st.switch_page("pages/2_Fiche_Film.py")