import base64
import streamlit as st
import pandas as pd
import ast


#Fonction qui permet de récupérer une image manuellement avec Streamlit
def get_base64_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


#fonction qui permet de changer l'image du background
def background_login_image():
    page_element='''
    <style>
    [data-testid="stMain"]{
        background-image: url("data:image/png;base64,%s");
        background-repeat: no-repeat;
        background-position: center;
        background-size: center;
    }
    [data-testid="stHeader"]{
        background-color: rgba(0,0,0,0);
    }
    [data-testid="stForm"]{
        background-color: rgba(255,255,255,0.5);
        
    }
    [data-testid="stWidgetLabel"], [data-testid="stHeading"]{
        color:#142735;
    }
    #film-data-lab, #film-data-lab-legend{
        color:#FFFFFF;
        font-weight:bold;
        text-align: center;
        margin:0;
    }
    </style>
    '''% (get_base64_file("pages/images/lock.png"))
    st.markdown(page_element, unsafe_allow_html=True)
    
def background_header_image():
    size = "100% 200px"
    page_element='''
    <style>
    [data-testid="stMainBlockContainer"]{
        margin-top:200px;
    }
    [data-testid="stHeader"]{
        background-color: rgba(0,0,0,0);
        background-image: url("data:image/png;base64,%s");
        background-repeat: no-repeat;
        background-position: top;
        background-size: %s;
        height:200px;
    }
    [data-testid="stToolbar"]{
        align-items: start;
        margin-top:15px;
    }
    </style>
    '''% (get_base64_file("pages/images/banner.png"), size) 
    st.markdown(page_element, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_data():
    try:
        df = pd.read_csv('db/data_2.csv')
        cols_to_fix = ['genres', 'actors', 'key_words', 'directors', 'production_countries']
        for col in cols_to_fix:
            # On gère le cas où c'est déjà une liste ou un string
            df[col] = df[col].fillna("[]").apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        return df

    except FileNotFoundError:
        st.error("❌ Fichier 'data_2.csv' introuvable.")
        st.stop()
        return False

@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df