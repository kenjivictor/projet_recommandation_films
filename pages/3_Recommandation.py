import streamlit as st
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Ciné Creuse/Nantes", layout="wide")

st.title("🍿 Le Recommandeur de Films")
st.markdown("Bienvenue ! Entrez un film que vous aimez, et découvrez nos pépites.")

# 1. CHARGEMENT DES DONNÉES

# 2. CALCUL DU ML (Peut aussi être mis en cache)

# Indexation pour la recherche
df = df.reset_index(drop=True)
indices = pd.Series(df.index, index=df['primaryTitle']).drop_duplicates()

# 3. FONCTION DE RECOMMANDATION

# 4. L'INTERFACE UTILISATEUR
# Liste déroulante pour choisir un film 
movie_list = df['primaryTitle'].values
selected_movie = st.selectbox("Quel film avez-vous aimé ?", movie_list)

if st.button('Recommander'):
    recommendations = get_recommendations(selected_movie)
    
    if recommendations is not None:
        st.subheader(f"Si vous avez aimé *{selected_movie}*, vous aimerez :")
        
        # Affichage en colonnes
        cols = st.columns(5)
        for i, col in enumerate(cols):
            movie = recommendations.iloc[i]
            with col:
                # Construction de l'URL de l'image
                poster_url = "https://image.tmdb.org/t/p/w500" + str(movie['poster_path'])
                st.image(poster_url, use_container_width=True)
                st.caption(f"**{movie['primaryTitle']}** ({movie['startYear']})")
                st.write(f"⭐ {movie['averageRating']}")