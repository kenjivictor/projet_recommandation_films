import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate
import functions.utils as utils
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

    st.divider()

    # 3. Le bouton de déconnexion
    authenticator.logout("Déconnexion", "sidebar")

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
except:
    st.error("Fichier data introuvable")
    st.stop()

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

        # Simulation ML (Random)
        sample = df.sample(6)
        list_index = list(sample.index)
        rec_image = list(sample["poster_path"])

        c1, c2 = st.columns([2, 3])
        c1.write("**Votre choix**")
        c2.write("**Recommandations**")

        col0, colA, colB, colC = st.columns([2, 1, 1, 1])

        # Film Choisi
        with col0:
            if pd.notna(chosen_poster):
                st.image(f"https://image.tmdb.org/t/p/w500{chosen_poster}", use_container_width=True)
            if st.button('Détails Principal', key="btn_main"):
                id_details = index_chosen

        # Recommandations (Grille 2x3)
        with colA:
            st.image(f"https://image.tmdb.org/t/p/w500{rec_image[0]}", use_container_width=True)
            if st.button('Détails 1', key="b1"): id_details = list_index[0]

            st.image(f"https://image.tmdb.org/t/p/w500{rec_image[3]}", use_container_width=True)
            if st.button('Détails 4', key="b4"): id_details = list_index[3]

        with colB:
            st.image(f"https://image.tmdb.org/t/p/w500{rec_image[1]}", use_container_width=True)
            if st.button('Détails 2', key="b2"): id_details = list_index[1]

            st.image(f"https://image.tmdb.org/t/p/w500{rec_image[4]}", use_container_width=True)
            if st.button('Détails 5', key="b5"): id_details = list_index[4]

        with colC:
            st.image(f"https://image.tmdb.org/t/p/w500{rec_image[2]}", use_container_width=True)
            if st.button('Détails 3', key="b3"): id_details = list_index[2]

            st.image(f"https://image.tmdb.org/t/p/w500{rec_image[5]}", use_container_width=True)
            if st.button('Détails 6', key="b6"): id_details = list_index[5]

    except Exception as e:
        st.error(f"Erreur lors de la génération : {e}")
else:
    st.info("En attente de sélection...")

# Affichage des détails si cliqué
if id_details is not None:
    st.divider()
    if mf:
        mf.movie_frame(id_details)
    else:
        st.warning("Module 'functions.movie_frame' introuvable.")

utils.background_header_image()