import streamlit as st
import hydralit_components as hc
from streamlit_lottie import st_lottie
import streamlit_antd_components as sac
from streamlit_calendar import calendar
import datetime
from Clases import Autenticador, Usuario,DBmanager
import extra_streamlit_components as stx
from st_xatadb_connection import XataConnection
import time
import asyncio
import requests

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
async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')


async def get_random_image():
    try:
        result = await asyncio.to_thread(requests.get, 'https://source.unsplash.com/random/600x400?machine-learning,programming,python,mathematics',timeout=1)
        return result.content
    except Exception as e:
        return "https://source.unsplash.com/random/600x400?machine-learning,programming,python,mathematics"

@st.cache_data
def get_propietario(key):
    try:
        result = xata.get('Usuario',key)
        return result['nombre_completo']
    except:
        return "Desconocido"


def update_courses():
    st.session_state.mycourses = [xata.query('Curso',{
    "columns": [],
    'filter':{
        'propietario': {'$is': st.session_state.user.key}
    }})]
    st.session_state.inscritos =  xata.query('Inscripcion',{"columns": [],'filter':{
        'user': {'$is': st.session_state.user.key}
    }})


def switch_to_render(key):
    if 'query' not in st.session_state:
        st.session_state.query = {'Table': 'Curso', 'id': key}
    else:
        st.session_state.query['Table'] = 'Curso'
        st.session_state.query['id'] = key

async def render_my_courses(course,indx ):
    img = await get_random_image()
    with st.spinner(f'Cargando Curso {course["nombre"]}'):
        with st.container(border=True):
            cols = st.columns([0.4,0.6])
            with cols[0]:
                st.image(img,use_column_width=True)
            with cols[1]:
                st.write(f'#### {course["nombre"]}')
                st.write(f"**Inscritos**: {course['inscritos']}")
                st.write(f"**Capacidad**: {str(course['capacidad'])+' Inscritos' if course['capacidad'] > 0 else 'Ilimitada'}")
                st.write(f"**Eres el Propietario**" if course['propietario']['id'] == st.session_state.user.key else f"**Propietario**: {get_propietario(course['propietario']['id'])}")
                st.write(f"**Visibilidad**: {'Público' if course['publico'] else 'Privado'}")
            _,bcol = st.columns([0.8,0.2])
            if bcol.button('Ver curso',key=f'ircuros{indx}',use_container_width=True,on_click=switch_to_render,args=[course['id']]):
                st.switch_page('pages/Course_render.py')

async def render_inscription(ins,index):
    with st.spinner(f'Cargando Curso...'):
        img = await get_random_image()
        data = xata.get('Curso',ins['cursoInscrito']['id'])
        with st.container(border=True):
            cols = st.columns([0.4,0.6])
            with cols[0]:
                st.image(img,use_column_width=True)
            with cols[1]:
                st.write(f'#### {data["nombre"]}')
                st.write(f"**Inscritos**: {data['inscritos']}")
                st.write(f"**Capacidad**: {str(data['capacidad'])+' Inscritos' if data['capacidad'] > 0 else 'Ilimitada'}")
                st.write(f"**Propietario**: {get_propietario(data['propietario']['id'])}")
            _,bcol = st.columns([0.8,0.2])
            if bcol.button('Ver curso',key=f'ircuros{index}',use_container_width=True,on_click=switch_to_render,args=[data['id']]):
                st.switch_page('pages/Course_render.py')


if 'inscritos' not in st.session_state and 'user' in st.session_state and st.session_state.user is not None:
    st.session_state.inscritos =  xata.query('Inscripcion',{"columns": [],'filter':{
        'user': {'$is': st.session_state.user.key}
    }})

if 'mycourses' not in st.session_state and 'user' in st.session_state and st.session_state.user is not None:
    st.session_state.mycourses = [xata.query('Curso',{
    "columns": [],
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


    if menu_id == 'Analisis de Datos':
        st.switch_page('pages/data_analysis_home.py')

    if menu_id == 'Blog':
        st.switch_page('pages/docs_home.py')

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
else:
    asyncio.run(show_message_error())
    st.stop()
st.write('Bienvenido a CAPPA, el Centro de Aprendizaje y Programación para Programadores Avanzados')


featurescols = st.columns([0.3,0.7])

with featurescols[0]:
    with st.container(border=True):
        st.markdown('⚙️**Herramientas**')
        st.page_link('pages/data_analysis_home.py',label='Analisis de Datos',icon='📊',
            use_container_width=True,help='Herramientas de Analisis de Datos para el desarrollo de proyectos de programación y ciencia de datos')
        st.page_link('pages/chatbot.py',label='Chatbot',icon='🤖',use_container_width=True,
                help='Interactua con nuestro chatbot para obtener ayuda con tus dudas de programación')
        st.caption('Proximamente')
        st.page_link('pages/problems_home.py',label='Concursos',icon='🏆',use_container_width=True,disabled=True,
            help='Participa en concursos de programación y demuestra tus habilidades')
        st.page_link('pages/problems_home.py',label='Foro',icon='📚',use_container_width=True,disabled=True,
                help='Participa en nuestro foro para compartir tus conocimientos y aprender de otros')
        st.page_link('pages/problems_home.py',label='Herramientas Matemáticas',icon='🧮',
                use_container_width=True,disabled=True,help='Herramientas matemáticas para el desarrollo de proyectos de programación y ciencia de datos')
        st.page_link('pages/problems_home.py',label='Herramientas Ciencia de Datos',icon='📈',
                use_container_width=True,disabled=True,help='Herramientas de Ciencia de Datos')

    with st.container(border=True,height=400):
        st.markdown('📌**Tareas Pendientes**')
        st.caption('Proximamente')

    with st.container(border=True,height=400):
        st.markdown('🔔**Notificaciones**')
        st.caption('Proximamente')


with featurescols[1]:
    st.subheader('🌟Mis Cursos')
    st.divider()
    _,upd = st.columns([0.8,0.2])
    upd.button('Actualizar Cursos',on_click=update_courses,use_container_width=True)

    for i,mycourse in enumerate(st.session_state.mycourses[0]['records']):
        asyncio.run(render_my_courses(mycourse,i))

    for j,ins in enumerate(st.session_state.inscritos['records']):
        asyncio.run(render_inscription(ins,j))



#--------------------------------- Anuncios ---------------------------------
st.markdown('''
<h1 style="font-family: 'Roboto', sans-serif; color: #787878; font-size: 2.5em; text-align: left;padding-bottom: 0;">Anuncios
<hr style="border: 1px solid #C7C7C7; width: 50%; margin-top: 0.5em; margin-bottom: 0.5em;"/>
</h1>


''', unsafe_allow_html=True)



# ---------------------------------Footer---------------------------------
with open("rsc/html/minimal_footer.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)
