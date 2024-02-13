import streamlit as st
import hydralit_components as hc
from streamlit_lottie import st_lottie
import streamlit_antd_components as sac
from streamlit_extras.switch_page_button import switch_page
from streamlit_calendar import calendar
import datetime
from Clases import Autenticador, Usuario
import extra_streamlit_components as stx
from st_xatadb_connection import XataConnection
import time

#Autor: Sergio Demis Lopez Martinez
#This is the main file for the CAPPA project and will contain the landing page


st.set_page_config(layout="wide", page_title='CAPPA', page_icon='rsc/Logos/LOGO_CAPPA.jpg', initial_sidebar_state='collapsed')
st.markdown("""
<style>
body {
background-color: #f4ebe8;

}

[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}

.st-emotion-cache-z5fcl4 {
  width: 100%;
  padding: 0rem 1rem 1rem;
    padding-right: 0.5rem;
    padding-left: 1rem;
    padding-bottom: 0.5rem;
  min-width: auto;
  max-width: initial;

}
</style>
""",unsafe_allow_html=True)

xata = st.connection('xata',type=XataConnection)


#---------------------------------  Variables de Sesión ---------------------------------------------------------
if 'auth_state' not in st.session_state:
    st.session_state.auth_state = False

if 'username' not in st.session_state:
    st.session_state.username = None

if 'userinfo' not in st.session_state:
    st.session_state.userinfo = None

if 'user' not in st.session_state:
    st.session_state.user = None


if 'logout' not in st.session_state:
    st.session_state.logout = False

def get_manager():
    return stx.CookieManager()
#---------------------------------#
#Navigation Bar
if st.session_state.logout:
    with st.spinner('Cerrando Sesión...'):
        time.sleep(2)
    st.session_state.logout = False
    st.switch_page('pages/login.py')

cookie_manager = get_manager()
auth = Autenticador(xata,cookie_manager)
valcookie = cookie_manager.get('Validado')
if auth() == False and valcookie is not None:
    auth.validate_cookie(valcookie)
    st.rerun()


if auth():
    #st.session_state['userinfo']
    if st.session_state.user.is_admin() or st.session_state.user.is_teacher():
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':'subid44','icon': "bi bi-journal-code", 'label':"Editor"}
        ]},
        {'id':'courses','icon': "bi bi-journal-bookmark", 'label':"Cursos",'ttip':"Cursos de Programación y Ciencia de Datos en CAPPA"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Blog",'ttip':"Articulos e Información",
        'submenu':[
            {'id':'doceditor','icon': "bi bi-file-earmark-richtext", 'label':"Editor" },
            {'id':'docshome','icon': "bi bi-search", 'label':"Home"}]
        },
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests", 'submenu':[
            {'label':"Todos", 'icon': "bi bi-search",'id':'alltests'},
            {'id':'subid144','icon': "bi bi-card-checklist", 'label':"Editor" }]},
        {'id':st.session_state.user.usuario,'icon': "bi bi-person", 'label':st.session_state.user.usuario,
        'submenu':[
            {'label':"Perfil", 'icon': "bi bi-person",'id':st.session_state.user.usuario},
            {"id": "logout", "icon": "bi bi-door-open", "label": "Cerrar Sesión"},
        ]}

    ]
    else:
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",'id':'Problemas'},
        {'id':'courses','icon': "bi bi-journal-bookmark", 'label':"Cursos",'ttip':"Cursos de Programación y Ciencia de Datos en CAPPA"},
        {'id':'Blog','icon': "bi bi-file-earmark-richtext", 'label':"Blog",'ttip':"Articulos e Información"},
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests"},
        {'id':st.session_state.user.usuario,'icon': "bi bi-person", 'label':st.session_state.user.usuario,
        'submenu':[
            {'label':"Perfil", 'icon': "bi bi-person",'id':st.session_state.user.usuario},
            {"id": "pcourses", "icon": "bi bi-journal-bookmark", "label": "Mis Cursos"},

            {"id": "logout", "icon": "bi bi-door-open", "label": "Cerrar Sesión"},
        ]}
    ]
    logname = st.session_state.user.usuario



    over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Inicio',
        login_name=None,
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
    )

    if st.session_state.user.is_admin() or st.session_state.user.is_teacher():
        if menu_id == 'subid00':
            st.switch_page('pages/problems_home.py')

        if menu_id == 'subid44':
            st.switch_page('pages/problems_editor.py')

        if menu_id == 'docshome':
            st.switch_page('pages/docs_home.py')

        if menu_id == 'doceditor':
            st.switch_page('pages/doc_editor.py')

        if menu_id == 'subid144':
            st.switch_page('pages/test_editor.py')

    else:
        if menu_id == 'Problemas':
            st.switch_page('pages/problems_home.py')

        if menu_id == 'Blog':
            st.switch_page('pages/docs_home.py')


    if menu_id == 'Analisis de Datos':
        st.switch_page('pages/data_analysis_home.py')

    if menu_id == 'Blog':
        st.switch_page('pages/docs_home.py')

    if menu_id == 'code':
        st.switch_page('pages/code_editor.py')

    if menu_id == 'logout':
        st.session_state.auth_state = False
        st.session_state.userinfo = None
        st.session_state.user = None
        st.session_state.username = None
        cookie_manager.delete('Validado')
        st.session_state.logout = True



    if menu_id == st.session_state.user.usuario:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        st.switch_page('pages/profile_render.py')
else:
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')
    st.stop()
st.write('Bienvenido a CAPPA, el Centro de Aprendizaje y Programación para Programadores Avanzados')


featurescols = st.columns([0.2,0.8])

with featurescols[0]:
    with st.container(border=True):
        st.markdown(':gear: **Herramientas**')
        st.page_link('pages/data_analysis_home.py',label='Analisis de Datos',icon='📊',
            use_container_width=True,help='Herramientas de Analisis de Datos para el desarrollo de proyectos de programación y ciencia de datos')

        st.caption('Proximamente')
        st.page_link('pages/problems_home.py',label='Concursos',icon='🏆',use_container_width=True,disabled=True,
            help='Participa en concursos de programación y demuestra tus habilidades')
        st.page_link('pages/problems_home.py',label='Chatbot',icon='🤖',use_container_width=True,disabled=True,
                help='Interactua con nuestro chatbot para obtener ayuda con tus dudas de programación')
        st.page_link('pages/problems_home.py',label='Foro',icon='📚',use_container_width=True,disabled=True,
                help='Participa en nuestro foro para compartir tus conocimientos y aprender de otros')
