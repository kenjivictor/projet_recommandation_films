import streamlit as st
from streamlit_authenticator import Authenticate
import functions.utils as utils


# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(page_title="Connexion", layout="centered", initial_sidebar_state="collapsed")

# Masquer la sidebar sur la page de login pour forcer la connexion
st.markdown("""
<style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# DONNÉES UTILISATEURS
# =========================================================
lesDonneesDesComptes = {
    'usernames': {
        'utilisateur': {'name':'utilisateur', 'password':'utilisateurMDP', 'email':'user@gmail.com', 'role':'user'},
        'root': {'name':'root', 'password':'rootMDP', 'email':'admin@gmail.com', 'role':'admin'}
    }
}

# =========================================================
# AUTHENTIFICATION
# =========================================================
authenticator = Authenticate(
    lesDonneesDesComptes,
    "cookie_name", 
    "cookie_key",
    30,
)

#titres de la page
st.html("<h1 id='film-data-lab'>Film Data Lab</h1>")
st.html("<h2 id='film-data-lab-legend'>Une application de recommandation de films basée sur la data et l'IA.</h2>")

#formulaire d'authentification
authenticator.login(
    location = 'main',
    fields = {'Form name':'Connexion', 'Username':'Utilisateur', 'Password':'Mot de passe','Login':'Connexion', 'Captcha':'Captcha'})

#image de fond sur la page de login
utils.background_login_image()

# =========================================================
# REDIRECTION
# =========================================================
if st.session_state["authentication_status"]:
    # Initialisation de la variable de navigation
    if 'selected_movie_id' not in st.session_state:
        st.session_state.selected_movie_id = None
    
    # Redirection vers l'accueil
    st.switch_page("pages/1_Accueil.py")

elif st.session_state["authentication_status"] is False:
    st.error("Nom d'utilisateur ou mot de passe incorrect. Merci de remplir Les champs avec username: utilisateur / password: utilisateurMDP")

elif st.session_state["authentication_status"] is None:
    st.warning('Veuillez vous connecter pour accéder à l\'application. Les champs username et password doivent être remplis. username: utilisateur / password: utilisateurMDP')