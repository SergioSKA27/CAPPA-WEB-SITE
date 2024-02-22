from st_xatadb_connection import XataConnection
import streamlit as st
import hydralit_components as hc
from Clases import Autenticador, Usuario,DBmanager
import extra_streamlit_components as stx
import asyncio
import time
from streamlit_searchbox import st_searchbox



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

.appview-container .main .block-container
{
    padding-top: 0px;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-bottom: 0px;
}
</style>
""",unsafe_allow_html=True)

xata = st.connection('xata',type=XataConnection)


def search_usuario(s: str):
    try:
        result = xata.search_on_table('Usuario',{"query": s, "fuzziness": 0, "prefix": "phrase"})
        data = []
        for record in result['records']:
            data.append(', '.join([record['id'],record['username'],record['nombre_completo'],record['rol']]))
        return data
    except:
        return []

async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')

if 'ayudantes' not in st.session_state:
    st.session_state.ayudantes = []


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
        {'id':'couseeditor','icon': "bi bi-journal-code", 'label':"Editor de Cursos",'ttip':"Crea Cursos  y personaliza las opciones"},
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
        st.error('403 No tienes permisos para acceder a esta página')
        st.image('https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif')
        st.page_link('pages/app.py',label='Regresar a la Página de Inicio',icon='🏠')
        st.stop()




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


    if menu_id == 'Inicio':
      st.switch_page('pages/app.py')
    if  menu_id == 'courses':
        st.switch_page('pages/CoursesHome.py')
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




st.title('📔✏️ Crear Curso Nuevo')
st.divider()

namecurso = st.text_input('Nombre del Curso',help='Ejemplo: Introducción a la Programación en Python')
cols1 = st.columns(2)
with cols1[0]:
    maxest = 0
    if st.toggle('Limitar número de estudiantes',False,help='Si se activa, se podrá limitar el número de estudiantes que pueden inscribirse al curso'):
        maxest = st.number_input('Número Máximo de Estudiantes',min_value=1,max_value=1000,step=1)
with cols1[1]:
    publico = st.checkbox('Curso Público',help='Si el curso es público, cualquier usuario puede inscribirse')




st.subheader('Añadir ayudantes',help='Puedes añadir ayudantes que te ayuden a administrar el curso(Máximo 2 ayudantes)')



users = st_searchbox(search_usuario,placeholder="Nombre de Usuario o Numero de Cuenta",label="Buscar Usuario",clear_on_submit=True)


if users is not None and users not in st.session_state.ayudantes and len(st.session_state.ayudantes) < 2:
    st.session_state.ayudantes.append(users)
    st.success(f'{users} añadido a la lista de ayudantes')

#st.write(st.session_state.ayudantes)



for i,ayudante in enumerate(st.session_state.ayudantes):
    with st.container(border=True):
        colsayud = st.columns([0.7,0.3])
        with colsayud[0]:
            st.write(ayudante)
        with colsayud[1]:
            if st.button(f':red[Eliminar]',use_container_width=True,key=f'eliminar{i}'):
                if ayudante in st.session_state.ayudantes:
                    del st.session_state.ayudantes[st.session_state.ayudantes.index(ayudante)]
                    st.rerun()


if st.button('Crear Curso',help='Crea un curso nuevo con los datos proporcionados'):
    if namecurso != '':
        curso = {
    "nombre": namecurso,
    "capacidad": maxest,
    "publico": publico,
    "propietario": st.session_state.user.key,
    }
    if len(st.session_state.ayudantes) > 0:
        curso['ayudante1'] = st.session_state.ayudantes[0].split(',')[0]
    if len(st.session_state.ayudantes) > 1:
        curso['ayudante2'] = st.session_state.ayudantes[1].split(',')[0]

    with st.spinner('Creando Curso...'):
        try:
            xata.insert('Curso',curso)
            st.success('Curso Creado Exitosamente')
            st.balloons()
        except Exception as e:
            st.error(f'Error al crear el curso: {e}')
#---------------------------------Footer---------------------------------#
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
