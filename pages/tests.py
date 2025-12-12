import streamlit as st

st.set_page_config(layout="wide")
# Custom HTML/CSS for the banner
custom_html = """
<div class="banner">
    <img src="https://media.discordapp.net/attachments/1437456002575372453/1447955495053693174/banner.png?ex=693ccce3&is=693b7b63&hm=4842a8eccea3026c64aea0244b9c17326dbd8e9b16dafc650da0cacf2a054441&=&format=webp&quality=lossless&width=1066&height=312" alt="Banner Image">
</div>
<style>
    .banner {
        width: 100%;
        height: 2000px;
    }
    .banner img {
        width: 100%;
    }
</style>
"""
# Display the custom HTML
st.components.v1.html(custom_html)

# Sidebar content
st.sidebar.header("Sidebar Title")
st.sidebar.subheader("Subheading")
st.sidebar.text("Sidebar content goes here.")

# Main content
st.title("Main Content")
st.write("Welcome to my Streamlit app!")
st.write("This is the main content area.")