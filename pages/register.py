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

st.set_page_config(page_title='Login', page_icon=':lock:', layout='centered')

xata = st.connection('xata',type=XataConnection)




def check_username(usr):
  try:
    ans = xata.get("Usuario",usr)
    return True
  except Exception as e:
    return False

def validar_correo(correo):
    patron = r'\b[A-Za-z0-9._%+-]+@pcpuma\.acatlan\.unam\.mx\b'
    if re.match(patron, correo):
        return True
    else:
        return False




no_cuenta = st.text_input('Número de cuenta',placeholder='Número de cuenta')
username = st.text_input('Usuario',placeholder='Usuario')
password = st.text_input('Contraseña', type='password',placeholder='Contraseña')
rpassword = st.text_input('Repetir contraseña', type='password',placeholder='Repetir contraseña')
correo = st.text_input('Correo electrónico',placeholder='Correo electrónico', help="usa un correo de pcpuma")
colssreg = st.columns([.6,.4])
cname = colssreg[0].text_input('Nombre completo',placeholder='Nombre completo')
bdate = colssreg[1].date_input('Fecha de nacimiento',max_value=datetime.date.today(),min_value=datetime.date  (1900,1,1))
flag = True
data = {
    "username": username,
    "password": bc.hashpw(password.encode('utf-8'), bc.gensalt()).decode('utf-8'),
    "correo": correo,
    "rol": "Estudiante",
    "nombre_completo": cname,
    "fechaNacimiento": bdate.strftime("%Y-%m-%dT%H:%M:%SZ"),
    "avatar": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
}

if st.button(label='Registrarme',help='Regístrate para poder acceder a la plataforma',  use_container_width=True):
    try:
        with st.spinner("Registrando..."):
            ans = xata.insert("Usuario", {
    "username": "string",
    "password": "string",
    "correo": "a@b.com",
    "avatar": {
        "base64Content": "SGVsbG8gV29ybGQ=",
        "enablePublicUrl": False,
        "mediaType": "application/octet-stream",
        "name": "upload.txt",
        "signedUrlTimeout": 300
    },
    "rol": "string",
    "verificado": True,
    "rango": "string",
    "score": 3,
    "nombre_completo": "string",
    "fechaNacimiento": "2000-01-01T00:00:00Z",
    "sociaLinks": [
        "string"
    ],
    "feed": "longer text"
})
            st.success('Usuario registrado con éxito')
            st.balloons()
            #st.switch_page('pages/login.py')
    except Exception as e:
        st.error('Error al registrar usuario')
        st.error(e)
        st.stop()


