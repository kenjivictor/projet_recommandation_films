import streamlit as st
import pandas as pd
# Importation du module
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate
#st.image("images/lock.png")
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
   st.image("images/lock.png")
elif st.session_state["authentication_status"] is False:
   st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"]:
  
# On affiche un menu déroulant (selectbox) DANS la barre latérale (sidebar)
# Création de la side bar qui contient le bouton de deconnexion et le menu 
#qui va afficher les choix qui se trouvent dans la variable options
  with st.sidebar:
    authenticator.logout("Déconnexion")# Le bouton de déconnexion
    st.title(f"Bienvenue {st.session_state['username']}")
    selection = option_menu(
              menu_title=None,
              options = ["Accueil", "visuel"],
              icons=["bi bi-house-door-fill","bi bi-camera2"]
          )
  # On indique au programme quoi faire en fonction du choix avec la condition si
  if selection == "Accueil":
      st.markdown('''<h2 style='text-align: center;'>Découvrez FilmDataLab, une application de recommandation de films basée sur la data et l'IA, développée à Nantes.</h2>''', unsafe_allow_html=True)
      st.image("images/banner.png")
  elif selection == "visuel":
      st.title("New York, plus qu’une destination \nune expérience à vivre au rythme de vos rêves.")
      st.image("https://cdn.pixabay.com/photo/2021/10/09/12/15/statue-of-liberty-6693960_1280.jpg")
      # Création de 3 colonnes 
      col1, col2, col3 = st.columns(3)
      # Contenu de la première colonne : 
      with col1:
        st.markdown("<h2 style='text-align: center;'>Manhattan</h2>", unsafe_allow_html=True)
        st.image("https://cdn.pixabay.com/photo/2019/09/07/12/46/new-york-4458710_1280.jpg")
      # Contenu de la deuxième colonne :
      with col2:
        st.markdown("<h2 style='text-align: center;'>Queens</h2>", unsafe_allow_html=True)
        st.image("https://cdn.pixabay.com/photo/2021/09/27/16/04/sphere-6661449_1280.jpg")
      # Contenu de la troisième colonne : 
      with col3:
        st.markdown("<h2 style='text-align: center;'>Brooklyn</h2>", unsafe_allow_html=True)
        st.image("https://cdn.pixabay.com/photo/2019/06/19/16/02/new-york-4285255_1280.jpg")
