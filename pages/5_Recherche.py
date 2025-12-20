import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate
import functions.utils as utils
import re
# Assurez-vous que le fichier functions.py existe bien dans le dossier racine
try:
    from functions import movie_frame as mf
except ImportError:
    mf = None

st.set_page_config(page_title="Recherche de films", layout="wide")

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

# =========================================================
# INITIALISATIONS
# =========================================================

# Nettoyage systématique dès qu'on navigue ailleurs que sur Recommandation
if "selected_movie_id" in st.session_state and st.session_state.selected_movie_id is not None:
    # On ne nettoie que si on n'est pas en train de cliquer sur une image à cet instant précis
    if st.session_state.get("une", -1) == -1 and st.session_state.get("sample", -1) == -1:
        st.session_state.selected_movie_id = None

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

st.header("Filtrer les films")

st.write("Choisissez vos critères")

# Chargement
df = utils.load_data()
df_filtered = pd.DataFrame([])

# valeurs par defaut pour le formulaire et la pagination
DEFAULTS = {
        # filtres du formulaire
        "afficher_decenie": False,
        "decenie_selected": 2000,
        "genres_selected": [],
        "actors_selected": [],
        "pays_selected": [],
        "titre_selected": "",
        
        # pagination
        "current_page": 1,
        "page_size": 20,
        
        # movieId pour la redirection vers la page de recommandation
        "selected_movie_id": None,
        
        # pour le "mélange" du dataframe lorsque l'utilisateur arrive sur la page
        "has_searched": False,
        "shuffled_index": None,
    }


# enregistrement des valeurs par defaut (filtres + pagination) dans le session_state
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)


#fonction pour effacer les données du formulaire sauvagardées dans le session_state
def reset_form():
    for k in DEFAULTS: 
        st.session_state.pop(k, None)


# définition de la fenetre pop-up
@st.dialog("Détails", width="medium")
def show_movie(id):
    if mf:
        mf.movie_frame(id)
    else:
        st.warning("Une erreur s'est produite. Veuillez réessayer.") #Module 'functions.movie_frame' introuvable.


# =========================================================
# Formulaire
# =========================================================



if df is not False:
    
    #si on vient tout juste d'arriver sur la page (le formulaire n'a pas été envoyé), on affiche tous les films dans un ordre aléatoire
    if not st.session_state.has_searched:
        if st.session_state.shuffled_index is None:
            # ici, on va "mélanger" les lignes du dataframe (pour ne pas avoir toujours les mêmes films en arrivant sur la page)
            # ce code fait un sample pur chaque ligne (frac=1) et les retourne les index
            st.session_state.shuffled_index = (df.sample(frac=1).index.to_list())
    
        df = df.loc[st.session_state.shuffled_index]
    
    #calcul des décénies dans le df
    df["Decenie"] = (df["startYear"] // 10) * 10
        
    # affichage du boouton de réinitialisation
    if st.button("🔄 Réinitialiser"):
        reset_form()
        st.rerun()
    
    
    
    # **** affichage des éléments de formulaire *****
    st.toggle("Recherche par décénie", key="afficher_decenie")
    
    
    with st.form("formulaire_filtres"):

        cols = st.columns(3)
        
        with cols[0]:
            st.text_input("Recherche par mots dans le titre", key="titre_selected")
            if st.session_state.afficher_decenie:
                st.select_slider(
                    "Décénie",
                    df['Decenie'].explode().value_counts().reset_index()['Decenie'].sort_values().to_list(),
                    key="decenie_selected",
                )
            
        with cols[1]:
        
            st.multiselect(
                "Genres",
                df['genres'].explode().value_counts().reset_index()['genres'].to_list(),
                key="genres_selected",
            )
            st.multiselect(
                "Acteurs",
                df['actors'].explode().value_counts().reset_index()['actors'].to_list(),
                key="actors_selected",
            )
        
        with cols[2]:
            st.multiselect(
                "Pays d'origine",
                df['production_countries'].explode().value_counts().reset_index()['production_countries'].to_list(),
                key="pays_selected",
            )
            
        

        submit = st.form_submit_button("🔎 Lancer la recherche", width="stretch")
        

    if submit:
        #on enregistre la page courante
        st.session_state.current_page = 1
        
        #on enregistre le fait qu'une recherche a été lancée
        st.session_state.has_searched = True





    #on crée une série vide à True qui a les mêmes index que notre dataframe
    mask = pd.Series(True, index=df.index)

    if st.session_state.afficher_decenie and st.session_state.decenie_selected is not None:
        mask &= df["startYear"].between(st.session_state.decenie_selected, st.session_state.decenie_selected+9)


    if st.session_state.genres_selected:
        mask &= df["genres"].apply(lambda x: any(t in x for t in st.session_state.genres_selected))

    if st.session_state.actors_selected:
        mask &= df["actors"].apply(lambda x: any(t in x for t in st.session_state.actors_selected))

    if st.session_state.pays_selected:
        mask &= df["production_countries"].apply(lambda x: any(t in x for t in st.session_state.pays_selected))

    # recherche par titre (recherche partielle, insensible à la casse)
    if st.session_state.titre_selected:
        #split par mot pour créer un filtre avec regex
        pattern = '|'.join(re.findall(r'\w+', st.session_state.titre_selected))
        
        #on choisit les colonnes sur lesquelles chercher
        mask &= df[['primaryTitle', 'originalTitle']].astype(str).agg(" ".join, axis=1).str.contains(pattern, case=False, regex=True)


    df_filtered = df[mask]

    if len(df_filtered) ==0:
        st.write("Aucun résultat trouvé. Veuillez modifier vos critères.")


# =========================================================
# Affichage des résultats
# =========================================================

if len(df_filtered) >0:
    
    
    #affichage de la pagination
    pagination_cols = st.columns((3, 1, 1))
    with pagination_cols[2]:
        page_size = st.selectbox("Page Size", options=[20, 50, 100])
        if page_size:
            st.session_state.page_size = page_size
    with pagination_cols[1]:
        total_pages = (len(df_filtered) + page_size - 1) // page_size
        total_pages = max(1, total_pages)
        
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
        if current_page:
            st.session_state.current_page = current_page
    with pagination_cols[0]:
        st.markdown(f"**{len(df_filtered)}** élément(s) trouvé(s)")
        st.markdown(f"Page **{current_page}** sur **{total_pages}**")
    
    
    # on fractionne le dataframe pour afficher les éléments par pages
    start = (current_page - 1) * page_size
    end = start + page_size
    data = df_filtered.iloc[start:end]
    
    
    # style des images pour qu'elles aient la même taille
    st.markdown("""
        <style>
        img {
            width: 100%;
            aspect-ratio: 3 / 4;
        }
        </style>
        """, unsafe_allow_html=True)
    
    
    #affichage de toutes les images (par lignes de 5)
    nb_cols = 5
    cols = st.columns(nb_cols)
    
    for i, row in enumerate(data.itertuples()):
        
        with cols[i % nb_cols]:
            
            st.image(f"https://image.tmdb.org/t/p/w500{row.poster_path}", width="stretch")
            
            col_img_btn = st.columns(2)
            
            with col_img_btn[0]:
                if st.button(f'Détails', key=f"d{i}", width="stretch"):
                    show_movie(row.Index)
            
            with col_img_btn[1]:
                if st.button(f'Recommander', key=f"r{i}", width="stretch"):
                    st.session_state.selected_movie_id = row.movieId
                    st.switch_page("pages/4_Recommandation.py")


utils.background_header_image()