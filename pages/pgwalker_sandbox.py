import time
from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd
import streamlit as st
import hydralit_components as hc
from streamlit_lottie import st_lottie
import streamlit_antd_components as sac
import extra_streamlit_components as stx
from st_xatadb_connection import XataConnection
import asyncio

from Clases import Usuario,Autenticador
# Adjust the width of the Streamlit page
st.set_page_config(layout="wide", page_title='CAPPA', page_icon='rsc/Logos/LOGO_CAPPA.jpg', initial_sidebar_state='collapsed')

# Establish communication between pygwalker and streamlit
init_streamlit_comm()

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
    padding-left: 0.5rem;
    padding-bottom: 0.5rem;
  min-width: auto;
  max-width: initial;

}
</style>
""",unsafe_allow_html=True)
xata = st.connection('xata',type=XataConnection)

def get_manager():
    return stx.CookieManager()

async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')


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

#---------------------------------#
#Navigation Bar
if auth():
    #st.session_state['userinfo']
    if st.session_state.user is not None and (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':'subid44','icon': "bi bi-journal-code", 'label':"Editor"}
        ]},
        {'id':'courses','icon': "bi bi-journal-bookmark", 'label':"Cursos",'ttip':"Cursos de Programación y Ciencia de Datos en CAPPA"},
        {'id':'pygwalker','icon': "bi bi-cpu", 'label':"Pygwalker",'ttip':"Herramientas de Analisis de Datos"},
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
    elif st.session_state.user is not None:
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",'id':'Problemas'},
        {'id':'courses','icon': "bi bi-journal-bookmark", 'label':"Cursos",'ttip':"Cursos de Programación y Ciencia de Datos en CAPPA"},
        {'id':'pygwalker','icon': "bi bi-cpu", 'label':"Pygwalker",'ttip':"Herramientas de Analisis de Datos"},
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


    over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
    menu_id = hc.nav_bar(
            menu_definition=menu_data,
            override_theme=over_theme,
            home_name='Inicio',
            login_name=None,
            hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
            sticky_nav=True, #at the top or not
            sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
            first_select=30
        )


    if menu_id == 'Inicio':
        st.switch_page('pages/app.py')

    if menu_id == 'code':
        st.switch_page('pages/code_editor.py')

    if  menu_id == 'courses':
        st.switch_page('pages/CoursesHome.py')

    if menu_id == 'logout':
        st.session_state.auth_state = False
        st.session_state.userinfo = None
        st.session_state.user = None
        st.session_state.username = None
        cookie_manager.delete('Validado')
        st.session_state.logout = True


    if st.session_state.user is not None and menu_id == st.session_state.user.usuario:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        st.switch_page('pages/profile_render.py')


    if st.session_state.user is not None and (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
        if menu_id == 'subid144':
            st.switch_page('pages/test_editor.py')

        if menu_id == 'doceditor':
            st.switch_page('pages/doc_editor.py')

        if menu_id == 'docshome':
            st.switch_page('pages/docs_home.py')

        if menu_id == 'subid44':
            st.switch_page('pages/problems_editor.py')

        if menu_id == 'subid00':
            st.switch_page('pages/problems_home.py')
    else:
        if menu_id == 'docs':
            st.switch_page('pages/docs_home.py')

        if menu_id == 'Problemas':
            st.switch_page('pages/problems_home.py')
else:
    asyncio.run(show_message_error())
    st.stop()




# Add a title
st.title("Pygwalker Sandbox",help='Esta es una herramienta de analisis de datos para la plataforma CAPPA usando Pygwalker')
st.divider()
datasetspths = [
    'Default',
    "datasets/pop-by-zip-code.csv",
    "datasets/Coronavirus_daily_data.csv"
    ]
data = st.selectbox("Selecciona un Dataset", datasetspths,)
# Get an instance of pygwalker's renderer. You should cache this instance to effectively prevent the growth of in-process memory.
@st.cache_resource
def get_pyg_renderer(data) -> "StreamlitRenderer":
    if data != "Default":
        if data.endswith(".xlsx"):
            df = pd.read_excel(data)
        elif data.endswith(".csv"):
            df = pd.read_csv(data)
    else:
        df = pd.read_csv("https://kanaries-app.s3.ap-northeast-1.amazonaws.com/public-datasets/bike_sharing_dc.csv")
    # When you need to publish your app to the public, you should set the debug parameter to False to prevent other users from writing to your chart configuration file.
    return StreamlitRenderer(df, spec="./gw_config.json", debug=False)

renderer = get_pyg_renderer(data)

# Render your data exploration interface. Developers can use it to build charts by drag and drop.
renderer.render_explore(width=1300)



#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
