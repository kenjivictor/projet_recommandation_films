import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate
# On importe la nouvelle librairie
from st_clickable_images import clickable_images 
import base64

# Configuration de la page — DOIT être tout en haut
st.set_page_config(page_title="Authentification", layout="wide")

#on initialise la variable lesDonneesDesComptes ou sont stockées les infos des utilisateurs de l'appli
lesDonneesDesComptes = {
    'usernames': {
        'utilisateur': {
            'name': 'utilisateur',
            'password': 'utilisateurMDP',
            'email': 'utilisateur@gmail.com',
            'failed_login_attemps': 0,  # Sera géré automatiquement
            'logged_in': False,          # Sera géré automatiquement
            'role': 'utilisateur'
        },
        'root': {
            'name': 'root',
            'password': 'rootMDP',
            'email': 'admin@gmail.com',
            'failed_login_attemps': 0,  # Sera géré automatiquement
            'logged_in': False,          # Sera géré automatiquement
            'role': 'administrateur'
        }
    }
}
#avec authenticator on verifie que les données sont exactes grace au login avec authenticator.login()
authenticator = Authenticate(
    lesDonneesDesComptes,  # Les données des comptes
    "cookie name",         # Le nom du cookie, un str quelconque
    "cookie key",          # La clé du cookie, un str quelconque
    30,                    # Le nombre de jours avant que le cookie expire
)
authenticator.login()

#  avec la fonction si on verifie le authentication_status et si le status est True on affiche la page d'accueil
if st.session_state["authentication_status"] is None:
    st.warning('Les champs username et password doivent être remplie voici les codes username : utilisateur , password : utilisateurMDP')
#   st.image("./images/lock.png")
elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"]:
    # Initialisation des variables de session
    if 'selected_movie_id' not in st.session_state:
        st.session_state.selected_movie_id = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Accueil"
#creation du dataframe a partir du dataset data_2.csv
    df = pd.read_csv("db/data_2.csv") 
#initialisation de la sidebar avec le menu
    with st.sidebar:
        authenticator.logout("Déconnexion")# Le bouton de déconnexion
        st.title(f"🎬 Découvrez FilmDataLab")
        # Logique pour synchroniser le menu et la page actuelle
        default_index = 1 if st.session_state.current_page == "Fiche Film" else 0
        selection = option_menu(
            menu_title=None, 
            options=["Accueil", "Fiche Film"], 
            icons=["house", "film"], 
            default_index=default_index
        )
        
        if selection != st.session_state.current_page:
            st.session_state.current_page = selection
            st.rerun()

    # --- SECTION ACCUEIL ---
    if st.session_state.current_page == "Accueil":

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
# Bannière avec Streamlit
        st.markdown("""
        <h2 style='text-align: center;'>
        Une application de recommandation de films basée sur la data et l'IA, développée à Nantes.
        </h2>
        """, unsafe_allow_html=True)
        st.image("pages/images/banner.png", width='stretch')
#        st.markdown("""
#        <h3 style='text-align: center;'>
#        Une application de recommandation de films basée sur la data et l'IA, développée à Nantes.
#        </h3>
#        """, unsafe_allow_html=True)
# initialisation de df_sorted qui est df trié par année et note de film (ce sera nos 5 films a l'affiche)
        df_sorted = df.sort_values(['startYear', 'averageRating'], ascending=False).head(5)
        
# On prépare les listes nécessaires pour le composant clickable_images
        images_urls = []
        titles = []
        
        for url in df_sorted['poster_path']:
            images_urls.append(f"https://image.tmdb.org/t/p/w500{url}")
            
        for titre in df_sorted['primaryTitle']:
            titles.append(titre)

        st.subheader("Films à la une (Cliquez sur une affiche)")

# CRÉATION DE LA GALERIE CLIQUABLE
# Ce composant remplace st.columns et st.image
        clicked_index = clickable_images(
            images_urls, 
            titles=titles,
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"height": "450px", "width": "auto", "display": "block", "margin": "auto", "object-fit": "cover", "border-radius": "10px"},
        )

# LOGIQUE DU CLIC
# clickable_images retourne -1 si rien n'est cliqué, sinon l'index (0, 1, 2...)
        if clicked_index > -1:
            # On récupère l'ID du film correspondant à l'index cliqué
            film_id = df_sorted.iloc[clicked_index]['movieId']

            # On met à jour la session
            st.session_state.selected_movie_id = film_id
            st.session_state.current_page = "Fiche Film"
            
            # On recharge la page pour aller vers la fiche
            st.rerun()
# --- SECTION FICHE FILM ---
    elif st.session_state.current_page == "Fiche Film":

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
# Bannière avec Streamlit
        st.image("pages/images/banner.png", width='stretch')        
# mettre en string df['movieId'] sinon cela marche pas car on n'a pas le même type
        df['movieId'] = df['movieId'].astype(str)
        if st.session_state.selected_movie_id is None:
            film_choisi=st.selectbox("Veuillez sélectionner un film.",df['primaryTitle'],
        index=0)
# Si le film choisi est différent de l'actuel, on met à jour selected_movie_id et on rerun
#            film_id_choisi = df[df['primaryTitle'] == film_choisi].iloc[0]['movieId']
#            if st.session_state.selected_movie_id != film_id_choisi:
#                st.session_state.selected_movie_id = film_id_choisi
#                st.rerun()  # <- ceci force la page à se recharger avec le nouveau film
        else:
            st.session_state.selected_movie_id = str(st.session_state.selected_movie_id)

            # Recherche du film correspondant
            movie_data = df[df['movieId'] == st.session_state.selected_movie_id]

            # --- Vérification ---
            if movie_data.empty:
                st.error(f"Aucun film trouvé pour ID {st.session_state.selected_movie_id}")
            else:
                # --- Affichage des infos du film ---
                titre = movie_data.iloc[0]['primaryTitle']
                annee = movie_data.iloc[0]['startYear']
                affiche = movie_data.iloc[0]['poster_path']
                note = movie_data.iloc[0].get('averageRating', 'N/A')
                description = movie_data.iloc[0].get('overview', 'Description non disponible')
                col1,col2 = st.columns(2)
                with col1:
                    st.title(titre)
                    st.image(f"https://image.tmdb.org/t/p/w500{affiche}", width=800)
                with col2:
                    st.subheader(f"Année de sortie : {annee}")
                    st.write(f"⭐ Note moyenne : {note}")
                    st.write(description)

        # --- Bouton retour ---

            if st.button("Retour à l'accueil"):
                st.session_state.selected_movie_id = None  # On vide le film sélectionné
                st.session_state.current_page = "Accueil"
                st.rerun()