import streamlit as st
import pandas as pd
from streamlit_authenticator import Authenticate

st.set_page_config(page_title="Fiche Film", layout="wide")

# AUTHENTIFICATION & SÉCURITÉ

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


# CHARGEMENT

@st.cache_data
def load_data():
    df = pd.read_csv("db/data_2.csv")
    df['movieId'] = df['movieId'].astype(str)
    return df

try:
    df = load_data()
except:
    st.error("Fichier introuvable")
    st.stop()

# AFFICHAGE

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
st.subheader("Fiche Film Détaillée")


# CAS 1 : Aucun film sélectionné (via menu latéral)
if st.session_state.get('selected_movie_id') is None:
    st.info("Recherchez un film ci-dessous :")
    liste_titres = df['primaryTitle'].sort_values().unique()
    film_choisi = st.selectbox("Film", liste_titres, index=None, placeholder="Tapez le nom d'un film...")
    
    if film_choisi:
        id_trouve = df[df['primaryTitle'] == film_choisi].iloc[0]['movieId']
        st.session_state.selected_movie_id = id_trouve
        st.rerun()

# CAS 2 : Film sélectionné
else:
    current_id = str(st.session_state.selected_movie_id)
    movie_data = df[df['movieId'] == current_id]

    if st.button("⬅️ Retour à l'accueil"):
        st.switch_page("pages/1_Accueil.py")
    
    st.divider()

    if not movie_data.empty:
        row = movie_data.iloc[0]
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if pd.notna(row['poster_path']):
                st.image(f"https://image.tmdb.org/t/p/w500{row['poster_path']}", use_container_width=True)
            else:
                st.text("Pas d'image")
        
        with col2:
            st.header(row['primaryTitle'])
            st.caption(f"ID: {current_id}")
            st.markdown(f"**Année :** {row['startYear']}")
            st.markdown(f"**Note :** ⭐ {row.get('averageRating', 'N/A')}/10")
            st.markdown("### Synopsis")
            st.write(row.get('overview', 'Aucune description.'))
            
            if st.button("Chercher un autre film"):
                st.session_state.selected_movie_id = None
                st.rerun()
    else:
        st.error("Erreur : Film introuvable avec cet ID.")