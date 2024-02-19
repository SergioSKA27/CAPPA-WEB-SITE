from st_xatadb_connection import XataConnection
import streamlit as st
import hydralit_components as hc
from Clases import Autenticador, Usuario,DBmanager
import extra_streamlit_components as stx
import asyncio
import time
from streamlit_searchbox import st_searchbox
import requests
from streamlit_quill import st_quill
import base64
from modules import Card, Dashboard, Editor,  Timer,Player
from streamlit_elements import elements, event, lazy, mui, sync,media
from types import SimpleNamespace




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


def get_adjunto(idd):
    try:
        result = xata.get('Recurso',idd,columns=['adjunto.base64Content'])
        return result['adjunto']['base64Content']
    except:
        return None

@st.cache_data
def get_user(key):
    try:
        result = xata.get('Usuario',key)
        return result['nombre_completo']
    except:
        return "Desconocido"

def is_owner():
    return st.session_state.currentcourse['propietario']['id'] == st.session_state.user.key

def update_course():
    try:
        st.session_state.currentcourse = xata.get('Curso',st.session_state.query['id'])
    except Exception as e:
        st.error(f'Error al obtener el curso: {e}')
        st.stop()

def update_resources():
    try:
        st.session_state.recursos = xata.query('Recurso',{"columns": ["*"],
        "filter":{ "curso": {"$is": st.session_state.currentcourse['id']}},
        "page": {"size": 1000}

        })
    except Exception as e:
        st.error(f'Error al obtener los recursos: {e}')
        st.stop()

async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')


def get_resources_section(sec):
    data = []
    for rec in st.session_state.recursos['records']:
        if rec['seccion'] == sec:
            data.append(rec)

    return data

def render_recurso(recurso):
    with st.container(border=True):
        st.write(f'## **{recurso["nombre"]}**')
        st.write(recurso['desc'],unsafe_allow_html=True)
        if 'adjunto' in recurso:
            if recurso['adjunto']['mediaType'] == 'application/pdf':
                ad = get_adjunto(recurso['id'])
                base64_pdf = ad
                # Embedding PDF in HTML
                pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'

                # Displaying File
                with st.expander('Ver Archivo Adjunto',expanded=False):
                    st.markdown(pdf_display, unsafe_allow_html=True)
            elif recurso['adjunto']['mediaType'] == 'image/png' or recurso['adjunto']['mediaType'] == 'image/jpeg' or recurso['adjunto']['mediaType'] == 'image/jpg':
                st.image(recurso['adjunto']['url'],use_column_width=True)
            elif recurso['adjunto']['mediaType'] == 'video/mp4':
                st.video(recurso['adjunto']['url'])
            elif recurso['adjunto']['mediaType'] == 'audio/mp3' or recurso['adjunto']['mediaType'] == 'audio/wav' or recurso['adjunto']['mediaType'] == 'audio/ogg':
                st.audio(recurso['adjunto']['url'])
        if 'video_url' in recurso and recurso['video_url'] != "":
            with elements(recurso['id']):
                with mui.Box(sx={'display':'flex','justifyContent':'center','alignItems':'center'}):
                    media.Player(recurso['video_url'])

        delcols = st.columns([0.9,0.1])
        if is_owner():
            if delcols[1].button('❌ :red[Eliminar]',help='Elimina el recurso',key=f'del{recurso["id"]}',on_click=del_recurso,args=[recurso['id']],use_container_width=True):
                st.rerun()




def del_recurso(idd):
    try:
        xata.delete('Recurso',idd)
        st.toast('Recurso Eliminado',icon='🎉')
        update_resources()
        time.sleep(2)
    except Exception as e:
        st.error(f'Error al eliminar el recurso: {e}')


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

if "query" in st.session_state and st.session_state.query["Table"] != "Curso":
    st.switch_page("pages/problems_home.py")
elif "query" not in st.session_state:
    pass
else:
    if 'query' in st.session_state:
        if 'currentcourse' not in st.session_state:
            try:
                st.session_state.currentcourse = xata.get('Curso',st.session_state.query['id'])
            except Exception as e:
                st.error(f'Error al obtener el curso: {e}')
                st.stop()
        else:
            if st.session_state.currentcourse['id'] != st.session_state.query['id']:
                try:
                    st.session_state.currentcourse = xata.get('Curso',st.session_state.query['id'])
                except Exception as e:
                    st.error(f'Error al obtener el curso: {e}')
                    st.stop()




if 'recursos' not in st.session_state:
    if 'currentcourse' in st.session_state:
        st.session_state.recursos = xata.query('Recurso',{"columns": ["*"],
        "filter":{ "curso": {"$is": st.session_state.currentcourse['id']}},
        "page": {"size": 1000}

        })



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
        {'id':'corse','icon': "bi bi-calculator", 'label':"Curso"},
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
        {'id':'corse','icon': "bi bi-calculator", 'label':"Curso"},
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



#st.write(st.session_state.currentcourse)
#st.write(st.session_state.recursos)


maincols = st.columns([0.3,0.7])

with maincols[0]:
    with st.container(border=True):
        st.image('https://source.unsplash.com/random/600x400?school,machine-learning,programming,python',use_column_width=True)
        st.write(f'### {st.session_state.currentcourse["nombre"]}')
        st.write(f'**Maximo de Estudiantes:** {st.session_state.currentcourse["capacidad"] if st.session_state.currentcourse["capacidad"] > 0 else "Sin límite"}')
        st.write(f'**Profesor:** {get_user(st.session_state.currentcourse["propietario"]["id"])}')
        st.write(f'**Visibilidad:** {"Público" if st.session_state.currentcourse["publico"] else "Privado"}')

        if 'ayudante1' in st.session_state.currentcourse or 'ayudante2' in st.session_state.currentcourse:
            st.write(f'**Ayudantes:**')
            if 'ayudante1' in st.session_state.currentcourse:
                st.write(f'- {get_user(st.session_state.currentcourse["ayudante1"]["id"])}')
            if 'ayudante2' in st.session_state.currentcourse:
                st.write(f'- {get_user(st.session_state.currentcourse["ayudante2"]["id"])}')
        if is_owner():
            if st.button('Editar',use_container_width=True):
                pass



if is_owner():
    with maincols[1]:
        addcols = st.columns([0.4,0.3,0.3])
        if addcols[1].toggle('Añadir Sección',help='Añade una nueva sección al curso'):
            with st.container(border=True):
                secname = st.text_input('Nombre de la Sección')
                bcolsaddsec = st.columns([0.7,0.3])
                if bcolsaddsec[1].button('Añadir',use_container_width=True):
                    if 'secciones' not in st.session_state.currentcourse:
                        if secname != "":
                            sec = [secname]
                            try:
                                xata.update('Curso',st.session_state.currentcourse['id'],{"secciones":sec})
                                update_course()
                                st.toast('Sección Añadida',icon='🎉')
                                time.sleep(2)
                                st.rerun()
                            except Exception as e:
                                st.error(f'Error al añadir la sección: {e}')
                    else:
                        if secname != "" and secname not in st.session_state.currentcourse["secciones"]:
                            sec = st.session_state.currentcourse['secciones']
                            sec.append(secname)
                            try:
                                xata.update('Curso',st.session_state.currentcourse['id'],{"secciones":sec})
                                update_course()
                                st.toast('Sección Añadida',icon='🎉')
                                time.sleep(2)
                                st.rerun()
                            except Exception as e:
                                st.error(f'Error al añadir la sección: {e}')

        if addcols[2].toggle('Editar Texto de bienvenida',help='Edita el texto de bienvenida del curso'):
            wwelcome = st.session_state.currentcourse['bio_curso']
            welcome = ""
            with st.form(key='editwelcome'):
                st.write('**Texto de Bienvenida**')
                welcome = st_quill(value=wwelcome,key='welcomeeditor',html=True)
                if st.form_submit_button('Preview'):
                    st.markdown(welcome,unsafe_allow_html=True)
            if welcome != wwelcome and welcome != "" :
                st.text(welcome)
                if st.button('Guardar Cambios',help='Guarda los cambios realizados'):
                    try:
                        xata.update('Curso',st.session_state.currentcourse['id'],{"bio_curso":welcome})
                        #result = client.records().update('Curso',st.session_state.currentcourse['id'],{"bio_curso":welcome})
                        #st.write(result)
                        update_course()
                        st.toast('Cambios Guardados',icon='🎉')
                        time.sleep(2)
                        st.rerun()
                    except Exception as e:
                        st.error(f'Error al guardar los cambios: {e}')


with maincols[1]:
    if 'bio_curso' in st.session_state.currentcourse:
        st.markdown(st.session_state.currentcourse['bio_curso'],unsafe_allow_html=True)


if 'secciones' in st.session_state.currentcourse:
    sectabs = st.tabs(st.session_state.currentcourse['secciones'])


for sec in range(0,len(st.session_state.currentcourse['secciones'])):
    with sectabs[sec]:
        resources = get_resources_section(st.session_state.currentcourse['secciones'][sec])
        #st.write(resources)
        for rec in resources:
            render_recurso(rec)

        if is_owner():
            secoptions = st.columns([0.6,0.2,0.2])

            if secoptions[1].toggle('Añadir Recurso',help='Añade un recurso a la sección',key=f'addrec{sec}'):
                with st.container(border=True):
                    recname = st.text_input('Nombre del Recurso', key=f'recname{sec}')
                    adj = st.file_uploader('Archivo',type=['pdf','png','jpg','jpeg','gif','mp4','mp3','wav','ogg'],key=f'adj{sec}')
                    desc = st.text_area('Descripción',height=100,help='Escibe una descripción del recurso puedes usar Markdown',key=f'desc{sec}')
                    if st.toggle('Añadir video de YouTube',key=f'yt{sec}'):
                        if "w_videocourses" not in st.session_state:
                            board = Dashboard()
                            wv = SimpleNamespace(
                                dashboard=board,
                                player=Player(
                                    board,
                                    0,
                                    0,
                                    10,
                                    6,
                                )
                            )
                            st.session_state.w_videocourses = wv
                        else:
                            wv = st.session_state.w_videocourses


                        with elements("videodocuments"):
                            with wv.dashboard(rowHeight=57):
                                wv.player()
                                st.caption("Para añadir un video, copia el link del video y reprodúcelo en el reproductor para tener una vista previa.")
                                st.caption("Una vez que estés satisfecho con el video, presiona el botón de añadir video para añadirlo al recurso.")

                        addv = st.checkbox("Añadir Video")



                    if st.button('Añadir',key=f'addbtn{sec}'):
                        if recname != ""  or adj is not None:
                            reid = None
                            try:
                                payload = {
                                    "nombre": recname,
                                    "seccion": st.session_state.currentcourse['secciones'][sec],
                                    "desc": desc if desc != "" else 'Recurso sin descripción',
                                    "curso": st.session_state.currentcourse['id']
                                }
                                if addv:
                                    payload['video_url'] = wv.player._url

                                reid = xata.insert('Recurso',payload)
                            except Exception as e:
                                st.error(f'Error al añadir el recurso: {e}')

                            if adj is not None and reid is not None:
                                try:
                                    xata.upload_file('Recurso',reid['id'],'adjunto',adj.read(),content_type=adj.type)
                                except Exception as e:
                                    st.error(f'Error al añadir el archivo adjunto: {e}')
                            st.toast('Recurso Añadido',icon='🎉')
                            update_resources()
                            time.sleep(2)
                            st.rerun()




#---------------------------------Footer---------------------------------#
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
