import streamlit as st
import pandas as pd


# CONFIGURATION DE LA PAGE

st.set_page_config(page_title="Ciné Creuse/Nantes", layout="centered")

st.title("Découvrir")
st.markdown("Entrez un film que vous aimez, et vous nous recommanderons des films basés sur vos préférences.")

# 1.CHARGEMENT DES DONNÉES
df = pd.read_csv("~/Documents/WCS/VSC/dossier_projets/Projet_2/projet_recommandation_films/db/data_2.csv")

# 2. ML 

# 3. FONCTION DE RECOMMANDATION

# 4. L'INTERFACE UTILISATEUR
# Liste déroulante pour choisir un film 
movie_list = df['primaryTitle'].sort_values().values
selected_movie = st.selectbox("Sélectionnez un titre de film", movie_list)

st.button('Recommander')
