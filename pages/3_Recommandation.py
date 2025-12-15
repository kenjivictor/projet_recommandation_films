import streamlit as st
import pandas as pd
from functions import movie_frame as mf


    
id = None
# CONFIGURATION DE LA PAGE

st.set_page_config(page_title="Ciné Creuse/Nantes", layout="centered")

st.title("Découvrir")
st.write("Entrez un film que vous aimez, et nous vous recommandons des films basés sur vos préférences.")

# 1.CHARGEMENT DES DONNÉES
df = pd.read_csv("db/data_2.csv")

# 2. ML 



# 3. L'INTERFACE UTILISATEUR
# Liste déroulante pour choisir un film 
movie_list = df['primaryTitle'].sort_values().values
chosen_movie = st.selectbox("Sélectionnez un film", movie_list, index= None , placeholder = "Aucun film sélectionné",)


# 4. FONCTION DE RECOMMANDATION
try:
    chosen_poster = df[df["primaryTitle"]==chosen_movie]["poster_path"].reset_index()["poster_path"].iloc[0]
    index_chosen_movie = df[df["primaryTitle"]==chosen_movie].index[0]
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
        if st.button('details       ', width = "stretch", type= "secondary"):
            id = index_chosen_movie
        
    with col00 :
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[0]}", use_container_width=True)
        if st.button('détails', width = "stretch", type= "secondary"):
            id = list_index[0]
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[3]}", use_container_width=True)
        if st.button('détails ', width = "stretch", type= "secondary"):
            id = list_index[3]
    with col01 :
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[1]}", use_container_width=True)
        if st.button('détails  ', width = "stretch", type= "secondary") :
            id = list_index[1]
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[4]}", use_container_width=True)
        if st.button('détails   ', width = "stretch", type= "secondary"):
            id = list_index[4]
    with col02 :
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[2]}", use_container_width=True)
        if st.button('détails    ', width = "stretch", type= "secondary"):
            id = list_index[2]
        st.image(f"https://image.tmdb.org/t/p/w500{rec_image[5]}", use_container_width=True)
        if st.button('détails     ', width = "stretch", type= "secondary"):
            id = list_index[5]
except:
    st.write("Découvrez maintenant plusieurs miliers de films basés sur vos préférences, en seulement quelques clicks. \nN'attendez pas, lancez votre recherche maintenant!\nEn attendant voici les dernières nouveautés:(rajouter les films les plus récents pour avoir un visual intéressant)")

if id != None :
    mf.movie_frame(id)

