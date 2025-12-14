from functions import movie_frame as mf
import streamlit as st
# So, instead, we use session state to store the "pressed" state of each button, and
# make each button press toggle that entry in the session state.


if "button1" not in st.session_state:
    st.session_state["button1"] = False

if "button2" not in st.session_state:
    st.session_state["button2"] = False

if st.button("Button1"):
    st.session_state["button1"] = not st.session_state["button1"]

if st.session_state["button1"]:
    if st.button("details"):
        st.session_state["button2"] = not st.session_state["button2"]
        id = 1
        
    if st.button("details "):
        st.session_state["button2"] = not st.session_state["button2"]
        id = 2
        
        
if st.session_state["button1"] and st.session_state["button2"]:
    st.write(id)
