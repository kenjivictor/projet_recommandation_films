import streamlit as st
import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

# =========================================================
# 1. CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="NANTFLIX Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thème sombre pour Seaborn (pour les graphiques Matplotlib)
sns.set_theme(style="darkgrid")

with st.sidebar:
    st.header("🍿 NANTFLIX")
    st.info("Visualisation des données du catalogue.")

st.title("📊 Dashboard Analytique : NANTFLIX")

# =========================================================
# 2. CHARGEMENT
# =========================================================
def load_data():
    df = pd.read_csv('db/data_2.csv')
    
    # Nettoyage des colonnes contenant des listes (format string -> list)
    cols_to_fix = ['genres', 'actors', 'key_words', 'directors', 'production_countries']
    for col in cols_to_fix:
        df[col] = df[col].fillna("[]").apply(ast.literal_eval)
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ Fichier 'data_2.csv' introuvable.")
    st.stop()

# =========================================================
# 3. INTERFACE (4 ONGLETS)
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Stats Globales", 
    "🎭 Genres", 
    "🌍 Origine", 
    "🎬 Réalisateurs"
])

# --- TAB 1 : STATS GLOBALES ---
with tab1:
    st.header("Vue d'ensemble")
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

# --- TAB 2 : GENRES ---
with tab2:
    st.header("Analyse des Genres")
    df_genres = df.explode('genres')
    counts = df_genres['genres'].value_counts().head(15).reset_index()
    counts.columns = ['Genre', 'Nombre']
    
    fig3 = px.bar(counts, x='Nombre', y='Genre', orientation='h', 
                title="Top 15 Genres", 
                color='Nombre', 
                color_continuous_scale='Viridis_r')
    fig3.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, use_container_width=True)

# --- TAB 3 : ORIGINE (US/FR/GB/CA vs Autres) ---
with tab3:
    st.header("🌍 Origine Géographique")
    
    df_countries = df.explode('production_countries')
    target_countries = ['US', 'FR', 'GB', 'CA']
    
    # Fonction de regroupement
    def group_country(country):
        if not country or pd.isna(country): return 'Autres'
        if country in target_countries: return country
        return 'Autres'

    df_countries['grouped_country'] = df_countries['production_countries'].apply(group_country)
    
    final_counts = df_countries['grouped_country'].value_counts().reset_index()
    final_counts.columns = ['Pays', 'Nombre de films']
    
    palette_inversee = px.colors.sequential.Viridis[::-1]

    fig4 = px.pie(
        final_counts, 
        values='Nombre de films', 
        names='Pays', 
        title='Répartition des productions par pays',
        hole=0.4,
        color_discrete_sequence=palette_inversee
    )
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig4, use_container_width=True)

# --- TAB 4 : RÉALISATEURS (TOP 10 BAR CHART) ---
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
        title=f"Top 10 des Réalisateurs (min. {min_films} films)",
        color_continuous_scale='Viridis',
        hover_data=['Nb Films', 'Popularité (Votes)'] # Infos supplémentaires au survol
    )
    
    # Mise en page
    fig5.update_traces(texttemplate='%{text:.2f}', textposition='inside')
    fig5.update_layout(yaxis=dict(autorange="reversed")) # Le 1er en haut
    fig5.update_xaxes(range=[0, 10]) # Force l'axe de 0 à 10 pour la note
    
    st.plotly_chart(fig5, use_container_width=True)