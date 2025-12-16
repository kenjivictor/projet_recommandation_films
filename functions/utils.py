import base64
import streamlit as st


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
