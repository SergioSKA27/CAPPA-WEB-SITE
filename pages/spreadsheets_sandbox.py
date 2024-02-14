import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
import pandas as pd
import hydralit_components as hc
import extra_streamlit_components as stx
from Clases import Usuario,Autenticador
import time
from st_xatadb_connection import XataConnection

# Adjust the width of the Streamlit page
st.set_page_config(layout="wide", page_title='CAPPA', page_icon='rsc/Logos/LOGO_CAPPA.jpg', initial_sidebar_state='collapsed')

# Establish communication between pygwalker and streamlit
xata = st.connection('xata',type=XataConnection)

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
  padding: 1rem 1rem 1rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    padding-bottom: 0.5rem;
  min-width: auto;
  max-width: initial;

}
</style>
""",unsafe_allow_html=True)



def get_manager():
    return stx.CookieManager()



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
    if st.session_state.user is not None and (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':'subid44','icon': "bi bi-journal-code", 'label':"Editor"}
        ]},
        {'id':'courses','icon': "bi bi-journal-bookmark", 'label':"Cursos",'ttip':"Cursos de Programación y Ciencia de Datos en CAPPA"},
        {'id':'spreadsheet','icon': "bi bi-file-earmark-richtext", 'label':"Mitosheet",'ttip':"Herramientas de Analisis de Datos"},
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
        {'id':'spreadsheet','icon': "bi bi-file-earmark-richtext", 'label':"Mitosheet",'ttip':"Herramientas de Analisis de Datos"},
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
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')
    st.stop()

#---------------------------------Body---------------------------------
st.title("Mitosheet Sandbox")
st.divider()
datasetspths = [
    'Default',
    ]
data = st.selectbox("Selecciona un Dataset", datasetspths,)


if data == 'Default':
    datas = 'https://raw.githubusercontent.com/plotly/datasets/master/tesla-stock-price.csv'
else:
    if  data.endswith('.csv'):
        datas = pd.read_csv(data)
    elif data.endswith('.xlsx'):
        datas = pd.read_excel(data)

new_dfs, code = spreadsheet(datas)

if st.checkbox('Mostrar Dataframes'):
    for k , df in new_dfs.items():
        st.dataframe(df,use_container_width=True)

st.subheader('Código de Python generado')
st.code(code)


#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
