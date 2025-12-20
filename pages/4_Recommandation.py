import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate
from functions import utils as utils
from functions import  test as test
import joblib

# Assurez-vous que le fichier functions.py existe bien dans le dossier racine
try:
    from functions import movie_frame as mf
except ImportError:
    mf = None

st.set_page_config(page_title="Recommandation", layout="wide")

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
    # 1. Le Titre et la description
    st.title("FilmDataLab")
    st.write("Une application de recommandation de films basée sur la data et l'IA.")
    st.divider()

    # 2. La Navigation Manuelle Identique à l'accueil
    st.page_link("pages/1_Accueil.py", label="Accueil", icon="🏠")
    st.page_link("pages/3_Presentation.py", label="Presentation", icon="📊")
    st.page_link("pages/4_Recommandation.py", label="Recommandation", icon="🎬")
    st.page_link("pages/5_Recherche.py", label="Recherche", icon="🎞️")

    st.divider()

    # 3. Le bouton de déconnexion
    authenticator.logout("Déconnexion", "sidebar")


# réinitialisation pour l'affichage du df aléatoire de la page de recherche
st.session_state.has_searched = False
st.session_state.shuffled_index = None

# =========================================================
# CONTENU PAGE
# =========================================================
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

#st.markdown("<h1 style='text-align: center;'>Une application de recommandation de films basée sur la data et l'IA.</h1>", unsafe_allow_html=True)


st.header("Découvrir")
#st.title("Découvrir")
st.write("Entrez un film que vous aimez pour obtenir des recommandations.")

# Chargement
try:
    df = pd.read_csv("db/data_2.csv")
# Chargement des features (nécessaire pour le ML)
    X = pd.read_csv("db/Features.csv")
except:
    st.error("Fichier data introuvable")
    st.stop()

# définition de la fenetre pop-up
@st.dialog("Détails", width="medium")
def show_movie(id):
    if mf:
        mf.movie_frame(id)
    else:
        st.warning("Une erreur s'est produite. Veuillez réessayer.") #Module 'functions.movie_frame' introuvable.

# =========================================================
# Interface & Gestion de la pré-sélection
# =========================================================
movie_list = df['primaryTitle'].sort_values().values

# Variable pour stocker l'index du film à pré-sélectionner
index_selection = None

# Vérification : Si l'utilisateur vient de la page d'accueil avec un clic
if "selected_movie_id" in st.session_state and st.session_state.selected_movie_id is not None:
    try:
        # On s'assure que movieId est bien en string pour la comparaison
        search_id = str(st.session_state.selected_movie_id)
        # On cherche le film correspondant dans le dataframe
        row_found = df[df['movieId'].astype(str) == search_id]

        if not row_found.empty:
            title_found = row_found.iloc[0]['primaryTitle']
            # On cherche la position de ce titre dans la liste triée
            # On convertit en liste pour utiliser la méthode .index()
            index_selection = list(movie_list).index(title_found)

            # Optionnel : On peut nettoyer la variable de session après usage
            # pour éviter que la sélection ne reste bloquée si on recharge la page
            # del st.session_state.selected_movie_id
    except Exception as e:
        st.warning(f"Impossible de pré-charger le film : {e}")

# Affichage du Selectbox avec l'argument 'index' dynamique
chosen_movie = st.selectbox(
    "Sélectionnez un film",
    movie_list,
    index=index_selection, # C'est ici que la magie opère
    placeholder="Aucun film sélectionné"
)

id_details = None

if chosen_movie:
    try:
        # Récup data film choisi
        subset = df[df["primaryTitle"]==chosen_movie]
        chosen_poster = subset["poster_path"].iloc[0]
        index_chosen = subset.index[0]

        # import du ML
        recommandation = test.recuperation_index(index_chosen)
        

        # Simulation ML (Random)

        list_index = list(recommandation[1:7])
        rec_image = df["poster_path"].iloc[list_index].to_list()

        c1, c2 = st.columns([2, 3])
        c1.write("**Votre choix**")
        c2.write("**Recommandations**")

        col0, colA, colB, colC = st.columns([2, 1, 1, 1])

        # Film Choisi
        with col0:
            if pd.notna(chosen_poster):
                st.image(f"https://image.tmdb.org/t/p/w500{chosen_poster}", width="stretch")
            if st.button('Détails Principal', key="btn_main", width="stretch"):
                id_details = index_chosen

        # style des images pour qu'elles aient la même taille
        st.markdown("""
            <style>
            img {
                width: 100%;
                aspect-ratio: 3 / 4;
            }
            </style>
            """, unsafe_allow_html=True)
        
        
        # Recommandations (Grille 2x3)
        nb = 0
        for i in range(1,3):
            for col in [colA, colB, colC]:
                with col:
                    st.image(f"https://image.tmdb.org/t/p/w500{rec_image[nb]}", width="stretch")
                    if st.button(f'Détails {nb+1}', key=f"b{nb}", width="stretch"): id_details = list_index[nb]
                nb +=1
        

    except Exception as e:
        st.error(f"Erreur lors de la génération : {e}")
else:
    st.info("En attente de sélection...")

# Affichage des détails si cliqué
if id_details is not None:
    show_movie(id_details)

utils.background_header_image()