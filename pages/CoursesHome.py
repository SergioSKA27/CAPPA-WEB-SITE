from st_xatadb_connection import XataConnection
import streamlit as st
import hydralit_components as hc
from Clases import Autenticador, Usuario,DBmanager
import extra_streamlit_components as stx
import asyncio
import time
import requests

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

async def get_random_image():
    result = await asyncio.to_thread(requests.get, 'https://source.unsplash.com/random/600x400?school,machine-learning,programming,python')
    return result.content

async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')


def switch_to_render(key):
    if 'query' not in st.session_state:
        st.session_state.query = {'Table': 'Curso', 'id': key}
    else:
        st.session_state.query['Table'] = 'Curso'
        st.session_state.query['id'] = key


def update_courses():
    st.session_state.cursos = [xata.query('Curso',{
    'filter':{
        'publico': {'$is': True}
    }
})]

@st.cache_data
def get_propietario(key):
    try:
        result = xata.get('Usuario',key)
        return result['nombre_completo']
    except:
        return "Desconocido"

def render_public_courses(course,indx ):
    with st.spinner(f'Cargando Curso {course["nombre"]}'):
        with st.container(border=True):
            cols = st.columns([0.2,0.8])
            with cols[0]:
                st.image(asyncio.run(get_random_image()),use_column_width=True)
            with cols[1]:
                st.write(f'#### {course["nombre"]}')
                st.write(get_propietario(course['propietario']['id']))
                _,bcol = st.columns([0.8,0.2])
                inscribir = bcol.button('Inscribirme',key=f'inscribir{indx}',use_container_width=True)

def render_my_courses(course,indx ):
    with st.spinner(f'Cargando Curso {course["nombre"]}'):
        with st.container(border=True):
            cols = st.columns([0.2,0.8])
            with cols[0]:
                st.image(asyncio.run(get_random_image()),use_column_width=True)
            with cols[1]:
                st.write(f'#### {course["nombre"]}')
                st.write(get_propietario(course['propietario']['id']))
                _,bcol = st.columns([0.8,0.2])
                if bcol.button('Ver curso',key=f'ircuros{indx}',use_container_width=True,on_click=switch_to_render,args=[course['id']]):
                    st.switch_page('pages/Course_render.py')



if 'cursos' not in st.session_state:
    st.session_state.cursos = [xata.query('Curso',{
    'filter':{
        'publico': {'$is': True}
    }
})]


if 'mycourses' not in st.session_state and 'user' in st.session_state and st.session_state.user is not None:
    st.session_state.mycourses = [xata.query('Curso',{
    'filter':{
        'propietario': {'$is': st.session_state.user.key}
    }})]

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
    if st.session_state.user is not None and (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
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
    elif st.session_state.user is not None:
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



    over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Inicio',
        login_name=None,
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
        first_select=20
    )

    if st.session_state.user is not None and (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
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
    if menu_id == 'Inicio':
        st.switch_page('pages/app.py')

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



    if st.session_state.user is not None and menu_id == st.session_state.user.usuario:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        st.switch_page('pages/profile_render.py')
else:
    asyncio.run(show_message_error())
    st.stop()




st.title('🗃️ Cursos')
st.divider()
titlecols = st.columns([0.8,0.2])
if st.session_state.user is not None and (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
    with titlecols[1]:
        st.page_link('pages/CourseEditor.py',label='Crear Curso',icon='📚')

st.subheader('Mis Cursos')
st.divider()

st.write(st.session_state.mycourses)

for i,mycourse in enumerate(st.session_state.mycourses[0]['records']):
    render_my_courses(mycourse,i)

st.subheader('Cursos Públicos')
st.divider()
st.button('Actualizar',on_click=update_courses)
st.write(st.session_state.cursos)


for i,course in enumerate(st.session_state.cursos[0]['records']):
    render_public_courses(course,i)




#---------------------------------Footer---------------------------------#
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
