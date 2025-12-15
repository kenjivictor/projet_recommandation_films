import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate
from st_clickable_images import clickable_images 
import base64

# --- CONFIGURATION (DOIT ÊTRE AU DÉBUT) ---
st.set_page_config(page_title="Authentification", layout="wide")

# --- DONNÉES UTILISATEURS ---
lesDonneesDesComptes = {
    'usernames': {
        'utilisateur': {
            'name': 'utilisateur',
            'password': 'utilisateurMDP',
            'email': 'utilisateur@gmail.com',
            'failed_login_attemps': 0,
            'logged_in': False,
            'role': 'utilisateur'
        },
        'root': {
            'name': 'root',
            'password': 'rootMDP',
            'email': 'admin@gmail.com',
            'failed_login_attemps': 0,
            'logged_in': False,
            'role': 'administrateur'
        }
    }
}

# --- AUTHENTIFICATION ---
authenticator = Authenticate(
    lesDonneesDesComptes,
    "cookie_name",
    "cookie_key",
    30,
)
authenticator.login()

# --- GESTION DES ÉTATS DE CONNEXION ---
if st.session_state["authentication_status"] is None:
    st.warning('Les champs username et password doivent être remplis. Test: utilisateur / utilisateurMDP')

elif st.session_state["authentication_status"] is False:
    st.error("Username ou password incorrect")

elif st.session_state["authentication_status"]:
    
    # 1. INITIALISATION DES VARIABLES DE SESSION
    if 'selected_movie_id' not in st.session_state:
        st.session_state.selected_movie_id = None
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Accueil"

    # 2. CHARGEMENT DES DONNÉES
    try:
        df = pd.read_csv("db/data_2.csv") 
        # IMPORTANT : On convertit tout de suite les IDs en texte
        df['movieId'] = df['movieId'].astype(str)
    except FileNotFoundError:
        st.error("Le fichier 'db/data_2.csv' est introuvable.")
        st.stop()

    # 3. SIDEBAR (MENU)
    with st.sidebar:
        authenticator.logout("Déconnexion")
        st.title(f"🎬 Découvrez FilmDataLab")
        
        # Synchronisation du menu avec la page actuelle
        default_index = 1 if st.session_state.current_page == "Fiche Film" else 0
        
        selection = option_menu(
            menu_title=None, 
            options=["Accueil", "Fiche Film"], 
            icons=["house", "film"], 
            default_index=default_index
        )
        
        # LOGIQUE DE CHANGEMENT DE PAGE
        if selection != st.session_state.current_page:
            # C'EST ICI LA CORRECTION : Si on va sur Fiche Film via le menu, on reset le film sélectionné
            if selection == "Fiche Film":
                st.session_state.selected_movie_id = None
                
            st.session_state.current_page = selection
            st.rerun()

    # =========================================================
    # PAGE : ACCUEIL
    # =========================================================
    if st.session_state.current_page == "Accueil":
        
        st.markdown("""
            <style>
                .block-container { padding-top: 1rem !important; }
            </style>
            """, unsafe_allow_html=True)
            
        st.markdown("<h2 style='text-align: center;'>Une application de recommandation de films basée sur la data et l'IA.</h2>", unsafe_allow_html=True)
        
        try:
            st.image("pages/images/banner.png", use_container_width=True)
        except:
            st.warning("Image bannière introuvable")

        # Tri des films
        df_sorted = df.sort_values(['startYear', 'averageRating'], ascending=False).head(5)
        
        # Préparation galerie
        images_urls = []
        titles = []
        for url in df_sorted['poster_path']:
            images_urls.append(f"https://image.tmdb.org/t/p/w500{url}")
        for titre in df_sorted['primaryTitle']:
            titles.append(titre)

        st.subheader("Films à la une (Cliquez sur une affiche)")

        clicked_index = clickable_images(
            images_urls, 
            titles=titles,
            div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
            img_style={"height": "400px", "margin": "10px", "object-fit": "cover", "border-radius": "10px", "cursor": "pointer"},
        )

        if clicked_index > -1:
            film_id = df_sorted.iloc[clicked_index]['movieId']
            st.session_state.selected_movie_id = film_id
            st.session_state.current_page = "Fiche Film"
            st.rerun()

    # =========================================================
    # PAGE : FICHE FILM
    # =========================================================
    elif st.session_state.current_page == "Fiche Film":

        st.markdown("""
            <style>
                .block-container { padding-top: 1rem !important; }
            </style>
            """, unsafe_allow_html=True)
            
        try:
            st.image("pages/images/banner.png", use_container_width=True)
        except:
            pass

        st.title("Fiche Détaille")

        # CAS 1 : AUCUN FILM SÉLECTIONNÉ
        if st.session_state.selected_movie_id is None:
            st.info("Recherchez un film dans la liste ci-dessous.")
            
            liste_titres = df['primaryTitle'].unique()
            film_choisi = st.selectbox("Rechercher un film :", liste_titres)
            
            if st.button("Voir la fiche"):
                film_id_choisi = df[df['primaryTitle'] == film_choisi].iloc[0]['movieId']
                st.session_state.selected_movie_id = str(film_id_choisi)
                st.rerun()

        # CAS 2 : UN FILM EST SÉLECTIONNÉ
        else:
            current_id = str(st.session_state.selected_movie_id)
            movie_data = df[df['movieId'] == current_id]

            if movie_data.empty:
                st.error(f"Erreur : Impossible de trouver le film avec l'ID {current_id}")
                if st.button("Réinitialiser"):
                    st.session_state.selected_movie_id = None
                    st.rerun()
            else:
                row = movie_data.iloc[0]
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if pd.notna(row['poster_path']):
                        st.image(f"https://image.tmdb.org/t/p/w500{row['poster_path']}", use_container_width=True)
                    else:
                        st.text("Pas d'image disponible")
                
                with col2:
                    st.header(row['primaryTitle'])
                    st.markdown(f"**Année :** {row['startYear']}")
                    st.markdown(f"**Note :** ⭐ {row.get('averageRating', 'N/A')}/10")
                    st.markdown("### Synopsis")
                    st.write(row.get('overview', 'Aucune description disponible.'))

            st.write("---")
            if st.button("⬅️ Retour"):
                st.session_state.selected_movie_id = None
                # st.session_state.current_page = "Accueil" # Décommente si tu veux retourner à l'accueil
                st.rerun()