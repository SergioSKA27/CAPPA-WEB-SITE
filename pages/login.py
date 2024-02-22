import streamlit as st
import streamlit_antd_components as sac
import bcrypt as bc
from streamlit_extras.switch_page_button import switch_page
from st_xatadb_connection import XataConnection
import datetime
import re
from Clases import Usuario, Autenticador
import extra_streamlit_components as stx
import time
import base64

st.set_page_config(page_title='Login', page_icon=':lock:', layout='centered', initial_sidebar_state='collapsed')

xata = st.connection('xata',type=XataConnection)




st.markdown('''
<style>
[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}
.st-emotion-cache-152jn8i {
  position: absolute;
  background: rgb(244, 235, 232);
  color: rgb(49, 51, 63);
  inset: 0px;
    top: 0px;
  overflow: hidden;
  top: 0px;
}
.st-emotion-cache-r421ms {
  border: 1px solid rgba(49, 51, 63, 0.0);
  border-radius: 2.5rem;
  padding: calc(1em - 1px);
}

.bg {
  background: radial-gradient(ellipse at bottom, #0d1d31 0%, #0c0d13 100%);
  bottom:0;
  left:-50%;
  opacity:1;
  position:fixed;
  right:-50%;
  top:0;
  z-index:0;
  background-size: cover;
  background-position: center center;
  width: 149%;
height: 100%;
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


if 'chatHistory' in st.session_state:
    del st.session_state['chatHistory']

if 'firstTime' not in st.session_state:
    del st.session_state['firstTime']

if 'text_stream' not in st.session_state:
    del st.session_state['text_stream']

if 'stream_last' not in st.session_state:
    del st.session_state['stream_last']




def validate_login(username, password):

    try:
        ans = xata.get("Usuario",username)
        if auth.validate_password(password, ans['password']):
            return True
        else:
            return False
    except Exception as e:
        return False

def get_manager():
    return stx.CookieManager()


cookie_manager = get_manager()
auth = Autenticador(xata,cookie_manager)
#------------------------Login------------------------
logo = base64.b64encode(open('rsc/Logos/LOGO_CAPPA.jpg', 'rb').read()).decode()
with st.form(key='login_form'):
    st.markdown(f'''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
    </style>
    <div style="text-align:center">
    <img src="data:image/jpeg;base64,{logo}" width="100" height="100" style="border-radius: 50%;margin-right: 10px;">
    </div>
    <h1 style="text-align: center;text-shadow: 2px 2px 5px #F5F5F5;font-family: 'Bebas Neue', cursive;">
    Iniciar sesión
    </h1>
    ''', unsafe_allow_html=True)
    username = st.text_input('Usuario',placeholder='No. de cuenta')
    password = st.text_input('Contraseña', type='password',placeholder='Contraseña')
    remember1month = st.checkbox('Recuerdame por 1 mes')
    cols = st.columns([0.3,0.4,0.3])
    with cols[1]:
        submit_button = st.form_submit_button(label='Iniciar sesión',use_container_width=True)

    if submit_button:
        if username == "" or password == "":
            st.error('El usuario o la contraseña no pueden estar vacíos')
        else:
            with st.spinner('Verificando credenciales...'):
                response = validate_login(username,password)
            if response == True:
                toat = st.toast(f'Usuario {username} validado con éxito!',icon='🎉')
                st.session_state['username'] = username
                st.session_state['auth_state'] = True
                st.session_state['userinfo'] = xata.get("Usuario",username)
                st.session_state['user'] = Usuario(st.session_state['userinfo'])
                if remember1month:
                    cookie_manager.set('Validado',username,expires_at=datetime.datetime.now() + datetime.timedelta(days=30))
                else:
                    cookie_manager.set('Validado',username)
                time.sleep(2)
                toat.toast('Redirigiendo a la página principal',icon='🚀')
                time.sleep(3)
                st.switch_page('pages/app.py')



            else:
                st.error('Usuario o contraseña incorrectos')



#st.write(cookie_manager.get_all())

opt = sac.tabs([
sac.TabsItem(label='Necesitas ayuda?', icon='question-circle-fill'),
sac.TabsItem(label='Olvidé mi contraseña', icon='lock'),
sac.TabsItem(label='Registrarme', icon='clipboard-plus'),
sac.TabsItem(label='Inicio', icon='house-door-fill')

],position='bottom',align='center',return_index=True)






if opt == 3:
    switch_page('Main')

if opt == 2:
    st.switch_page('pages/register.py')
