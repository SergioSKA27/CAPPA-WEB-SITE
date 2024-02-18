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
import asyncio

st.set_page_config(page_title='Login', page_icon=':lock:', layout='centered')

xata = st.connection('xata',type=XataConnection)


async def check_no_cuenta(no_cuenta):
    try:
        await asyncio.sleep(0.5)
        user = xata.get("Usuario", no_cuenta)
        if user:
            return True
        else:
            return False
    except Exception as e:
        return False

async def check_username(usr):
  try:
    await asyncio.sleep(0.5)
    user = xata.query("Usuario", {"filter": {"username": {"$is": usr}}})
    if len(user['records']) > 0:
      return True
    else:
        return False
  except Exception as e:
    return False

async def check_correo(correo):
    try:
        await asyncio.sleep(0.5)
        user = xata.query("Usuario", {"filter": {"correo": {"$is": correo}}})
        if len(user['records']) > 0:
            return True
        else:
            return False
    except Exception as e:
        return False

def validar_correo(correo):
    patron = r'\b[A-Za-z0-9._%+-]+@pcpuma\.acatlan\.unam\.mx\b'
    if re.match(patron, correo):
        return True
    else:
        return False


def validar_no_cuenta():
    if st.session_state.no_cuenta != "":
        with st.spinner("Verificando número de cuenta..."):
            if asyncio.run(check_no_cuenta(st.session_state.no_cuenta)):
                st.error('El número de cuenta ya está registrado')
                st.session_state.reg_flag += 1
            else:
                if st.session_state.reg_flag > 0:
                    st.session_state.reg_flag -= 1


def validar_username():
    if st.session_state.username != "":
        with st.spinner("Verificando nombre de usuario..."):
            if asyncio.run(check_username(st.session_state.username)):
                st.error('Ya existe un usuario con ese nombre')
                st.session_state.reg_flag += 1
            else:
                if len(st.session_state.username) < 6:
                    st.error('El nombre de usuario debe tener al menos 6 caracteres')
                    st.session_state.reg_flag += 1
                elif len(st.session_state.username) > 20:
                    st.error('El nombre de usuario debe tener máximo 20 caracteres')
                    st.session_state.reg_flag += 1
                else:
                    st.success('Nombre de usuario disponible')
                    if st.session_state.reg_flag > 0:
                        st.session_state.reg_flag -= 1


def validar_correo_av():
    if st.session_state.correo != "":
        if not validar_correo(st.session_state.correo):
            st.error('El correo debe ser de pcpuma')
            st.session_state.reg_flag += 1
        else:
            with st.spinner("Verificando correo..."):
                if asyncio.run(check_correo(st.session_state.correo)):
                    st.error('El correo ya está registrado')
                    st.session_state.reg_flag += 1
                else:
                    st.success('Correo disponible')
                    if st.session_state.reg_flag > 0:
                        st.session_state.reg_flag -= 1



if 'reg_flag' not in st.session_state:
    st.session_state.reg_flag = 0

no_cuenta = st.text_input('Número de cuenta',placeholder='Número de cuenta', key='no_cuenta',on_change=validar_no_cuenta)


username = st.text_input('Usuario',placeholder='Usuario', key='username',on_change=validar_username)


password = st.text_input('Contraseña', type='password',placeholder='Contraseña')
rpassword = st.text_input('Repetir contraseña', type='password',placeholder='Repetir contraseña')

if password != rpassword and password != "" and rpassword != "":
    st.error('Las contraseñas no coinciden')
    st.stop()
elif password != "" and rpassword != "":
    if len(password) < 8:
        st.error('La contraseña debe tener al menos 8 caracteres')
        st.stop()
    elif len(password) > 20:
        st.error('La contraseña debe tener máximo 20 caracteres')
        st.stop()
    else:
        st.success('Contraseña válida')

correo = st.text_input('Correo electrónico',placeholder='Correo electrónico', help="usa un correo de pcpuma", key='correo',on_change=validar_correo_av)


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
    "fechaNacimiento": bdate.strftime("%Y-%m-%dT%H:%M:%SZ")
}

if st.button(label='Registrarme',help='Regístrate para poder acceder a la plataforma',  use_container_width=True,
disabled=st.session_state.reg_flag != 0 and (no_cuenta == "" or username == "" or password == "" or rpassword == "" or correo == "" or cname == "" or bdate == "" or st.session_state.reg_flag > 0)):
    try:
        with st.spinner("Registrando..."):
            ans = xata.insert("Usuario", data)
            st.toast('Usuario registrado con éxito',icon='🎉')
            st.balloons()
        with st.spinner("Redirigiendo al login..."):
            time.sleep(3)
        st.switch_page('pages/login.py')
    except Exception as e:
        st.error('Error al registrar usuario')
        st.error(e)
        st.stop()


st.session_state.reg_flag
