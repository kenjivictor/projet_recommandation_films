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

st.header("Filtrer les films")

st.write("Choisissez vos critères")

# Chargement
df = utils.load_data()
df_filtered = pd.DataFrame([])

id_details = None

#initialisation des filtres

st.session_state.setdefault("filtres", {
    "submitted" : False,
    "afficher_decenie": False,
    "decenie_selected": 2000,
    "genres_selected": [],
    "actors_selected": [],
    "pays_selected": [],
    "titre_selected": "",
})

#initialisation de la page en cours
st.session_state.setdefault("current_page", 1)
st.session_state.setdefault("page_size", 20)

    
    
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
    
    
    
    afficher_decenie = st.toggle("Recherche par décénie", value=st.session_state.filtres["afficher_decenie"])
    df["Decenie"] = (df["startYear"] // 10) * 10
    
    
    with st.form("formulaire_filtres"):
        if afficher_decenie:
            decenie_selected = st.select_slider(
                "Décénie",
                df['Decenie'].explode().value_counts().reset_index()['Decenie'].sort_values().to_list(),
                value=st.session_state.filtres["decenie_selected"],
            )
        else:
            decenie_selected = None
        genres_selected = st.multiselect(
            "Genres",
            df['genres'].explode().value_counts().reset_index()['genres'].to_list(),
            default=st.session_state.filtres["genres_selected"]
        )
        actors_selected = st.multiselect(
            "Acteurs",
            df['actors'].explode().value_counts().reset_index()['actors'].to_list(),
            default=st.session_state.filtres["actors_selected"]
        )
        pays_selected = st.multiselect(
            "Pays d'origine",
            df['production_countries'].explode().value_counts().reset_index()['production_countries'].to_list(),
            default=st.session_state.filtres["pays_selected"]
        )
        #recherche dnas le titre ou par mot clef
        titre_selected = st.text_input("Recherche par mots dans le titre", value=st.session_state.filtres["titre_selected"])

        submit = st.form_submit_button("Lancer la recherche")

    if submit:
        
        #on enregistre les filtres
        st.session_state.filtres = {
            "submitted" : True,
            "afficher_decenie": afficher_decenie,
            "decenie_selected": decenie_selected,
            "genres_selected": genres_selected,
            "actors_selected": actors_selected,
            "pays_selected": pays_selected,
            "titre_selected": titre_selected,
        }
        st.session_state.current_page = 1





    #on crée une série vide à True qui a les mêmes index que notre dataframe
    mask = pd.Series(True, index=df.index)

    if afficher_decenie and decenie_selected is not None:
        mask &= df["startYear"].between(decenie_selected, decenie_selected+9)


    if genres_selected:
        mask &= df["genres"].apply(lambda x: any(t in x for t in genres_selected))

    if actors_selected:
        mask &= df["actors"].apply(lambda x: any(t in x for t in actors_selected))

    if pays_selected:
        mask &= df["production_countries"].apply(lambda x: any(t in x for t in pays_selected))

    # recherche par titre (recherche partielle, insensible à la casse)
    if titre_selected:
        #split par mot pour créer un filtre avec regex
        pattern = '|'.join(re.findall(r'\w+', titre_selected))
        
        #on choisit les colonnes sur lesquelles chercher
        mask &= df[['primaryTitle', 'originalTitle']].astype(str).agg(" ".join, axis=1).str.contains(pattern, case=False, regex=True)


    df_filtered = df[mask]

    if len(df_filtered) ==0:
        st.write("Aucun résultat trouvé. Veuillez modifier vos critères.")




if len(df_filtered) >0:
    
    #si on vient tout juste d'arriver sur la page (le formulaire n'a pas été envoyé), on affiche tous les films
    if st.session_state.filtres["submitted"] == False:
        # ici, on va "mélanger" les lignes du dataframe (pour ne pas avoir toujours les mêmes films en arrivant sur la page)
        # ce code fait un sample pur chaque ligne (frac=1) et les retourne dans un ordre différent
        df_filtered = df_filtered.sample(frac=1).reset_index(drop=True)
    
    
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
    nb_ligne = (len(data) + nb_cols - 1) // nb_cols
    nb_ligne = max(1, nb_cols)
    nb = 0
    for i in range(nb_ligne):
        for col in cols:
            with col:
                if nb < len(data):
                    st.image(f"https://image.tmdb.org/t/p/w500{data.iloc[nb]['poster_path']}", width="stretch")
                    if st.button(f'Détails {nb+1}', key=f"b{nb}", width="stretch"): id_details = data.iloc[[nb]].index[0]
            nb +=1
    
# Affichage des détails si cliqué
if id_details is not None:
    show_movie(id_details)


utils.background_header_image()