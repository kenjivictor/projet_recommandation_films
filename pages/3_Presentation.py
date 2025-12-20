import streamlit as st
import pandas as pd
import ast
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_authenticator import Authenticate
import functions.utils as utils

st.set_page_config(page_title="Presentation", layout="wide")

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
    # 1. Le Titre et la description
    st.title("FilmDataLab")
    st.write("Une application de recommandation de films basée sur la data et l'IA.")
    st.divider()
    
    # 2. La Navigation Manuelle Identique à l'accueil
    st.page_link("pages/1_Accueil.py", label="Accueil", icon="🏠")
    st.page_link("pages/3_Presentation.py", label="Presentation", icon="📊")
    st.page_link("pages/4_Recommandation.py", label="Recommandation", icon="🎬")
    st.page_link("pages/5_Recherche.py", label="Recherche", icon="🎞️")
    
    st.divider()
    
    # 3. Le bouton de déconnexion
    authenticator.logout("Déconnexion", "sidebar")

# Nettoyage systématique dès qu'on navigue ailleurs que sur Recommandation
if "selected_movie_id" in st.session_state and st.session_state.selected_movie_id is not None:
    # On ne nettoie que si on n'est pas en train de cliquer sur une image à cet instant précis
    if st.session_state.get("une", -1) == -1 and st.session_state.get("sample", -1) == -1:
        st.session_state.selected_movie_id = None

# réinitialisation pour l'affichage du df aléatoire de la page de recherche
st.session_state.has_searched = False
st.session_state.shuffled_index = None

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

#st.markdown("<h1 style='text-align: center;'>Une application de recommandation de films basée sur la data et l'IA.</h1>", unsafe_allow_html=True)
        

st.header("Dashboard Analytique :")
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

tab1, tab2, tab3, tab4 , tab5 = st.tabs(["A propos", "📈 Stats Globales", "🎭 Genres", "🌍 Origine", "🎬 Réalisateurs"])

# TAB 1
with tab1:
    st.header("ℹ️ À propos de FilmDataLab")
    
    # --- 1. LE PROJET ---
    st.subheader("🎬 Le Projet")
    st.markdown("""
    **Nantes Cinéma** lance son offensive numérique avec **FilmDataLab**, une application web innovante destinée à ses spectateurs de Loire-Atlantique.
    
    L'objectif est double :
    1.  **Digitaliser l'offre** pour attirer un public plus jeune (Gen Z et Millennials).
    2.  **Personnaliser l'expérience** grâce à un moteur de recommandation intelligent capable de suggérer le "film parfait" en fonction des goûts de chacun.
    """)
    
    st.info("💡 *\"Où chaque film trouve son audience\"* - La promesse FilmDataLab.")

    st.divider()

    # --- 2. MÉTHODOLOGIE TECHNIQUE (NOUVEAU) ---
    st.subheader("⚙️ Méthodologie & Technique")
    st.markdown("""
    Notre approche s'est déroulée en trois phases clés pour garantir la pertinence des suggestions :
    
    #### 1️⃣ Étude de Marché & Ciblage
    Avant de coder, nous avons analysé les données démographiques locales (Loire-Atlantique).
    * **Cible Prioritaire :** Les 15-30 ans (représentant 1/3 de la population).
    * **Préférences Identifiées :** Forte appétence pour la **Comédie** et l'**Animation**.
    * **Format :** Priorité aux contenus en **Version Française (VF)**.
    
    #### 2️⃣ Préparation de la Donnée (Data Engineering)
    Nous avons exploité une base de données cinéma complète et l'avons nettoyée pour en extraire la valeur.
    * **Volume :** 5 644 Films, 31 000+ Acteurs, 3 500+ Réalisateurs.
    * **Traitement :** Nettoyage des valeurs manquantes, formatage des genres et filtrage des films pertinents.
    
    #### 3️⃣ Le Moteur de Recommandation (Machine Learning)
    L'intelligence de l'application repose sur un système de filtrage qui croise :
    * **Le contenu :** Similitude entre les films (genres, mots-clés, réalisateurs).
    * **La popularité :** Pondération par la note moyenne et le nombre de votes.
    """)
    
    st.divider()
    
    # --- 3. L'ÉQUIPE ---
    st.subheader("👥 L'Équipe Data")
    
    st.write("Ce projet a été réalisé pour **Nantes Cinéma** par une équipe de passionnés :")
    
    col_team1, col_team2, col_team3, col_team4 = st.columns(4)
    
    # Membre 1
    with col_team1:
        st.markdown("### 👩‍💻") 
        st.markdown("Carole Pons-Bachmann") 
        st.caption("Wilder Data Analyst") 
        st.markdown("[LinkedIn](https://www.linkedin.com/in/carole-pons-bachmann/)")

    # Membre 2
    with col_team2:
        st.markdown("### 👩‍💻")
        st.markdown("Kenji Victor")
        st.caption("Wilder Data Analyst")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/kenji-victor/)")

    # Membre 3
    with col_team3:
        st.markdown("### 👩‍💻")
        st.markdown("Helena Steyaert")
        st.caption("Wilder Data Analyst")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/helena-steyaert/)")

    # Membre 4
    with col_team4:
        st.markdown("### 🧑‍💻")
        st.markdown("Naoufel Kaouachi")
        st.caption("Wilder Data Analyst")
        st.markdown("[LinkedIn](https://www.linkedin.com/in/naoufelkaouachi/)")


with tab2:
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

# TAB 3
with tab3:
    st.header("Analyse des Genres")
    counts = df['genres'].explode().value_counts().head(15).reset_index()
    counts.columns = ['Genre', 'Nombre']
    fig3 = px.bar(counts, x='Nombre', y='Genre', orientation='h', title="Top 15 Genres", color='Nombre', color_continuous_scale='Viridis_r')
    fig3.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, use_container_width=True)

# TAB 4
with tab4:
    st.header("🌍 Origine Géographique")
    pays_counts = df['production_countries'].explode().value_counts().reset_index()
    autres_pays = pd.DataFrame({'production_countries':['Autres'], 'count': [pays_counts.loc[5:]['count'].sum()]})
    final_counts = pd.concat([pays_counts.loc[0:4], autres_pays], ignore_index=True).rename(columns={'production_countries': 'Pays', 'count':'Nombre de films'})
    palette_inversee = px.colors.sequential.Viridis[::-1]
    fig4 = px.pie(final_counts, values='Nombre de films', names='Pays', title='Répartition des productions par pays', hole=0.4,color_discrete_sequence=palette_inversee)
    fig4.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig4, use_container_width=True)

# TAB 5
with tab5:
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
    
utils.background_header_image()