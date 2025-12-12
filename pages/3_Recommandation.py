import streamlit as st
import pandas as pd


# CONFIGURATION DE LA PAGE

st.set_page_config(page_title="Ciné Creuse/Nantes", layout="centered")

st.title("Découvrir")
st.write("Entrez un film que vous aimez, et nous vous recommandons des films basés sur vos préférences.")

# 1.CHARGEMENT DES DONNÉES
df = pd.read_csv("~/Documents/WCS/VSC/dossier_projets/Projet_2/projet_recommandation_films/db/data_2.csv")

# 2. ML 



# 3. L'INTERFACE UTILISATEUR
# Liste déroulante pour choisir un film 
movie_list = df['primaryTitle'].sort_values().values
chosen_movie = st.selectbox("Sélectionnez un film", movie_list, index= None , placeholder = "Aucun film sélectionné",)
chosen_poster = df[df["primaryTitle"]==chosen_movie]["poster_path"].reset_index()["poster_path"].iloc[0]

# 4. FONCTION DE RECOMMANDATION
if st.button('Recommander',width = "stretch", type= "primary"):

    # récupération des images et index des films recommandés
    sample = df.sample(6)
    list_index = list(sample.index)
    rec_image = list(sample["poster_path"])
    
    # affichage des images des films    
    col1,col2 = st.columns([2.27,3])
    
    with col1:
        st.write("Le film que vous avez choisi")
    with col2:
        st.write("Les films qui pourraient vous intéresser")
        
    col0,col00, col01 , col02 = st.columns([2.27,1,1,1])
    
    with col0:
        st.image(f"https://image.tmdb.org/t/p/w500{chosen_poster}", use_container_width=True)
        st.button('details       ', width = "stretch", type= "secondary")
    with col00 :
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[0]}", use_container_width=True)
        st.button('détails', width = "stretch", type= "secondary")
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[3]}", use_container_width=True)
        st.button('détails ', width = "stretch", type= "secondary")
    with col01 :
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[1]}", use_container_width=True)
        st.button('détails  ', width = "stretch", type= "secondary")
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[4]}", use_container_width=True)
        st.button('détails   ', width = "stretch", type= "secondary")
    with col02 :
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[2]}", use_container_width=True)
        st.button('détails    ', width = "stretch", type= "secondary")
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[5]}", use_container_width=True)
        st.button('détails     ', width = "stretch", type= "secondary")

        