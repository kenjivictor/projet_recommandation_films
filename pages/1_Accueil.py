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

    st.divider()

    # 3. Le bouton de déconnexion en DERNIER
    authenticator.logout("Déconnexion", "sidebar")

# LOGIQUE & DONNÉES
# Nettoyage systématique dès qu'on navigue ailleurs que sur Recommandation
if "selected_movie_id" in st.session_state and st.session_state.selected_movie_id is not None:
    # On ne nettoie que si on n'est pas en train de cliquer sur une image à cet instant précis
    if st.session_state.get("une", -1) == -1 and st.session_state.get("sample", -1) == -1:
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

st.title("🚀 Films à la une !")
st.subheader("Cliquez sur une affiche pour voir les détails")
# Films à la une
#######################
df_sorted = df.sort_values(['startYear', 'averageRating'], ascending=False).head(5)
images_urls = [f"https://image.tmdb.org/t/p/w500{url}" for url in df_sorted['poster_path']]
titles = [t for t in df_sorted['primaryTitle']]

clicked_index = clickable_images(
    images_urls,
    titles=titles,
    div_style={"display": "flex", "justify-content": "space-between", "flex-wrap": "nowrap","overflow-x": "auto","width": "100%"},
    img_style={"height": "auto", "width": "18%","max-width": "400px", "display": "block", "margin": "5px", "object-fit": "cover", "border-radius": "10px", "cursor": "pointer"},
    key="une"
)
#flex-wrap: nowrap interdit au navigateur de déplacer les images sur une deuxième ligne, peu importe la largeur du navigateur.
#width: 18%: En utilisant un pourcentage au lieu d'une taille fixe en pixels, les images vont rétrécir ou s'agrandir proportionnellement à la taille de la fenêtre de l'utilisateur.
#overflow-x: auto : Si l'utilisateur regarde l'application sur un téléphone très étroit, cela permettra de faire défiler les affiches horizontalement avec le doigt au lieu de casser la mise en page.
#height: auto : En changeant la hauteur de 450px à auto, on évite que les images ne soient écrasées ou étirées lorsque leur largeur change.
if clicked_index > -1:
    film_id = df_sorted.iloc[clicked_index]['movieId']
    st.session_state.selected_movie_id = film_id
    # Redirection vers la page de recommandation
    st.switch_page("pages/4_Recommandation.py")

#Films sample
#######################
st.header('''📽️Les classiques qu’on ne se lasse jamais de revoir.''')
# --- LOGIQUE DE GÉNÉRATION DU SAMPLE ET NETTOYAGE ---

# 1. Sécurité pour éviter l'erreur de comparaison
une_val = st.session_state.get("une")
sample_val = st.session_state.get("sample")
has_clicked_any = (une_val is not None and une_val > -1) or (sample_val is not None and sample_val > -1)

# 2. Nettoyage du film sélectionné si on ne vient pas de cliquer
if not has_clicked_any:
    st.session_state.selected_movie_id = None

# 3. Tirage aléatoire si nouveau chargement
if not has_clicked_any or 'df_sample_accueil' not in st.session_state:
    st.session_state.df_sample_accueil = df.sample(5)

df_sample = st.session_state.df_sample_accueil
images_urls_sample = [f"https://image.tmdb.org/t/p/w500{url}" for url in df_sample['poster_path']]
titles_sample = [t for t in df_sample['primaryTitle']]

clicked_index_sample = clickable_images(
    images_urls_sample,
    titles=titles_sample,
    div_style={"display": "flex", "justify-content": "space-between", "flex-wrap": "nowrap","overflow-x": "auto","width": "100%"},
    img_style={"height": "auto", "width": "18%","max-width": "400px", "display": "block", "margin": "5px", "object-fit": "cover", "border-radius": "10px", "cursor": "pointer"},
    key="sample"
)

if clicked_index_sample > -1:
    film_id = df_sample.iloc[clicked_index_sample]['movieId']
    st.session_state.selected_movie_id = film_id
    # Redirection vers la page de recommandation
    st.switch_page("pages/4_Recommandation.py")

utils.background_header_image()