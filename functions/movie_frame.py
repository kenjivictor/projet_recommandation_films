import streamlit as st
import pandas as pd
import numpy as np
import requests

from googletrans import Translator
import asyncio


# ------------- DEFINITION DES VARIABLES ----------------------

# récupération des données
df = pd.read_csv('db/data_2.csv')
df['actors'] = df['actors'].apply(lambda x: eval(x))
df['directors'] = df['directors'].apply(lambda x: eval(x))
df['writers'] = df['writers'].apply(lambda x: eval(x))
df['production_companies_name'] = df['production_companies_name'].apply(lambda x: eval(x))
df['production_countries'] = df['production_countries'].apply(lambda x: eval(x))
df['genres'] = df['genres'].apply(lambda x: eval(x))



# init the Google API translator
translator = Translator()


# ------------- DEFINITION DES FONCTIONS ----------------------



# permet de transformer une liste en texte
def get_list_as_string(liste):
    if len(liste) >0:
        retour = ""
        retour = ', '.join(liste)
    else:
        retour = "Inconnu"
    
    return retour




# traduire un texte anglais 
async def translateText(texte):
    async with Translator() as translator:
        translation = await translator.translate(texte, dest='fr')
        return translation.text


# Récupérer le résumé du film en français
def read_overview(movieId):
    retour = ""
    try:
        url = f"https://api.themoviedb.org/3/movie/{movieId}/translations"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZTRhNmYxMjc1M2ZhNmMxMmIwZmMwMjUzYjVlNjY3ZiIsInN1YiI6IjY1NDEyOWM4MzU4MThmMDBhZGM2YzZhNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.NDGx7z7tJWcKpdFU43nTPar8V_i17RwgJjKMWWZ5D9Q"}

        response = requests.get(url, headers=headers)
        
        overview = response.json()
        
        count = 0
        for i in overview["translations"]:
            if i["name"]=="Français" and i["data"]["overview"] != '':
                retour += f"{i["data"]["overview"]}\n"
                count=+1
            if count == 1:
                break
        if count == 0:
            for i in overview["translations"]:
                if i["name"]=="English":
                    retour += "**Pas de résumé en Français disponible, voici un résumé traduit automatiquement : **<br>"
                    retour += f"{asyncio.run(translateText(i["data"]["overview"]))}\n"
    except:
        retour += "Une erreur s'est produite. Impossible de récupérer "
    
    return retour


# convertion des runtimmeMinutes
def get_time(runtimeMinutes):
    heures = runtimeMinutes // 60
    minutes = runtimeMinutes % 60
    
    if heures == 0:
        heures = ""
    else:
        heures = str(heures) + "h"
    
    if minutes == 0:
        minutes = ""
    
    return f"{heures}{minutes}"




# ------------- FONCTION D'AFFICHAGE DES ELEMENTS ----------------------

def movie_frame(movie_index):
    try:
        movie_selected = df.iloc[movie_index]

        col1, col2 = st.columns(2)

        with col1:
            st.image(f"https://image.tmdb.org/t/p/w500{movie_selected['poster_path']}", use_container_width=True)

        with col2:
            st.header(movie_selected['primaryTitle'])
            st.html(f"<b>Titre original :</b> {movie_selected['originalTitle']}<br>{movie_selected['startYear']} - {get_time(movie_selected['runtimeMinutes'])} <br> ⭐ {movie_selected['averageRating']}")
            st.html(f"<b>Genre(s) :</b> {get_list_as_string(movie_selected['genres'])}")
            st.html(f"<b>Réalisateur(s) :</b> {get_list_as_string(movie_selected['directors'])}")
            st.html(f"<b>Scénaristes :</b> {get_list_as_string(movie_selected['writers'])}")
            st.html(f"<b>Acteurs :</b> {get_list_as_string(movie_selected['actors'])}")
            st.html(f"<b>Societé de production :</b> {get_list_as_string(movie_selected['production_companies_name'])}")
            st.html(f"<b>Origine :</b> {get_list_as_string(movie_selected['production_countries'])}")

        st.html(f"<b>Résumé :</b><br>{read_overview(movie_selected['movieId'])}")
    except:
        st.html("🎞️ Le film demandé est introuvable. Veuillez relancer la recherche.")

