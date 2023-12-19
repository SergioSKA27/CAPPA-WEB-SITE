import streamlit as st
import bcrypt as bc

st.set_page_config(page_title='Login', page_icon=':lock:', layout='centered')

st.markdown('''
<style>

#MainMenu, header, footer {visibility: hidden;}
.st-emotion-cache-r421ms {
  border: 1px solid rgba(49, 51, 63, 0.0);
  border-radius: 2.5rem;
  padding: calc(1em - 1px);
}

.bg {
  animation:slide 20s ease-in-out infinite alternate;
  background: radial-gradient(ellipse at bottom, #0d1d31 0%, #0c0d13 100%);
  bottom:0;
  left:-50%;
  opacity:1;
  position:fixed;
  right:-50%;
  top:0;
  z-index:0;
  ackground-size: cover;
  background-position: center center;
}
</style>
<div class="bg"></div>
''', unsafe_allow_html=True)


with open('rsc/css/backgroundLogin.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    st.markdown('''
<div class="stars">
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
  <div class="star"></div>
</div>''',unsafe_allow_html=True)


with st.form(key='login_form'):
    st.markdown('''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
    </style>
    <h1 style="text-align: center;text-shadow: 2px 2px 5px #F5F5F5;font-family: 'Bebas Neue', cursive;">
    Iniciar sesión
    </h1>
    ''', unsafe_allow_html=True)
    username = st.text_input('Usuario',placeholder='Usuario')
    password = st.text_input('Contraseña', type='password',placeholder='Contraseña')
    cols = st.columns([0.4,0.3,0.3])
    with cols[1]:
        submit_button = st.form_submit_button(label='Iniciar sesión')
