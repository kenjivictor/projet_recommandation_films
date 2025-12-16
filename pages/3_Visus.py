import streamlit as st
import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_authenticator import Authenticate

st.set_page_config(page_title="Visus", layout="wide")

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


# CONTENU PAGE

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
st.header("Dashboard Analytique : FilmDataLab")
sns.set_theme(style="darkgrid")

def load_data():
    df = pd.read_csv('db/data_2.csv')
    cols_to_fix = ['genres', 'actors', 'key_words', 'directors', 'production_countries']
    for col in cols_to_fix:
        # On gère le cas où c'est déjà une liste ou un string
        df[col] = df[col].fillna("[]").apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ Fichier 'data_2.csv' introuvable.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["📈 Stats Globales", "🎭 Genres", "🌍 Origine", "🎬 Réalisateurs"])

# TAB 1
with tab1:
    st.subheader("Vue d'ensemble")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Films", len(df))
    c2.metric("Note Moy.", f"{round(df['averageRating'].mean(), 1)}/10")
    c3.metric("Votes", f"{df['numVotes'].sum():,.0f}".replace(",", " "))
    c4.metric("Année Méd.", int(df['startYear'].median()))
    st.divider()
    c_g1, c_g2 = st.columns(2)
    with c_g1:
        st.subheader("Chronologie")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(df['startYear'], bins=30, kde=True, color="#5ec962", ax=ax, linewidth=0)
        ax.set_ylabel("")
        ax.set_xlabel("Année")
        st.pyplot(fig)
    with c_g2:
        st.subheader("Durées")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.histplot(df['runtimeMinutes'], bins=30, color="#fde725", ax=ax2, linewidth=0)
        ax2.set_xlim(0, 200)
        ax2.set_ylabel("")
        st.pyplot(fig2)

# TAB 2
with tab2:
    st.header("Analyse des Genres")
    df_genres = df.explode('genres')
    counts = df_genres['genres'].value_counts().head(15).reset_index()
    counts.columns = ['Genre', 'Nombre']
    fig3 = px.bar(counts, x='Nombre', y='Genre', orientation='h', title="Top 15 Genres", color='Nombre', color_continuous_scale='Viridis_r')
    fig3.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, use_container_width=True)

# TAB 3
with tab3:
    st.header("🌍 Origine Géographique")
    df_countries = df.explode('production_countries')
    target = ['US', 'FR', 'GB', 'CA']
    df_countries['grouped'] = df_countries['production_countries'].apply(lambda x: x if x in target else 'Autres')
    palette_inversee = px.colors.sequential.Viridis[::-1]
    final_counts = df_countries['grouped'].value_counts().reset_index()
    final_counts.columns = ['Pays', 'Nombre de films']
    fig4 = px.pie(final_counts, values='Nombre de films', names='Pays', title='Répartition des productions par pays', hole=0.4,color_discrete_sequence=palette_inversee)
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig4, use_container_width=True)

# TAB 4
with tab4:
    st.header("🎬 Top 10 Réalisateurs")
    st.markdown("Classement basé sur la **Note Moyenne** (min. 3 films). La couleur indique la popularité (nombre de votes).")
    # 1. Préparation des données
    df_dirs = df.explode('directors')
    df_dirs = df_dirs[df_dirs['directors'] != ""]
    # 2. Calcul des métriques par réalisateur
    stats_dirs = df_dirs.groupby('directors').agg({
        'primaryTitle': 'count',      # Nombre de films
        'averageRating': 'mean',      # Note moyenne
        'numVotes': 'sum'             # Somme des votes
    }).reset_index()
    
    stats_dirs.columns = ['Réalisateur', 'Nb Films', 'Note Moyenne', 'Popularité (Votes)']
    
    # 3. Filtre : On garde ceux qui ont au moins 3 films (pour éviter les notes parfaites sur 1 seul film)
    min_films = 3
    filtered_dirs = stats_dirs[stats_dirs['Nb Films'] >= min_films]
    
    # 4. Tri : On prend les 10 meilleurs selon la note moyenne
    top_10_dirs = filtered_dirs.sort_values(by='Note Moyenne', ascending=False).head(10)
    
    # 5. Graphique à Barres Horizontales
    fig5 = px.bar(
        top_10_dirs, 
        x='Note Moyenne', 
        y='Réalisateur', 
        orientation='h',
        color='Popularité (Votes)',  # La couleur dépend du nombre de votes
        text='Note Moyenne',         # Affiche la note sur la barre
#        title=f"Top 10 des Réalisateurs (min. {min_films} films)",
        color_continuous_scale='Viridis',
        hover_data=['Nb Films', 'Popularité (Votes)'] # Infos supplémentaires au survol
    )
    
    # Mise en page
    fig5.update_traces(texttemplate='%{text:.2f}', textposition='inside')
    fig5.update_layout(yaxis=dict(autorange="reversed")) # Le 1er en haut
    fig5.update_xaxes(range=[0, 10]) # Force l'axe de 0 à 10 pour la note
    
    st.plotly_chart(fig5, use_container_width=True)