import streamlit as st


st.set_page_config(layout="wide", page_title='CAPPA', page_icon='rsc/Logos/LOGO_CAPPA.jpg', initial_sidebar_state='collapsed')


with open("rsc/html/DataAHomeBanner.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)
