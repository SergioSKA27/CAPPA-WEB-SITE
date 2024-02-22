import streamlit as st
import google.generativeai as genai
import asyncio
from time import sleep
import extra_streamlit_components as stx
import hydralit_components as hc
from st_xatadb_connection import XataConnection
from Clases import Autenticador, Usuario,DBmanager
import time




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


genai.configure(api_key=st.secrets["GEN_AI_KEY"])

async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')


@st.cache_resource
def load_genmodel():
    return genai.GenerativeModel("gemini-pro")

def stream_text():
    """Stream text to the app"""
    for w in st.session_state.text_stream.split(" "):
        yield w + " "
        sleep(0.05)

async def generate_response(prompt):
    with st.spinner("Generando Respuesta..."):
        await asyncio.sleep(10)
        response = model.generate_content(prompt)
    return response.text

model = load_genmodel()

if 'chatHistory' not in st.session_state:
    st.session_state.chatHistory = []

if 'firstTime' not in st.session_state:
    st.session_state.firstTime = ''



if 'text_stream' not in st.session_state:
    st.session_state.text_stream = ""

if 'stream_last' not in st.session_state:
    st.session_state.stream_last = True


if st.session_state.user is not None and not st.session_state.user.is_verified():
    st.warning("Solo usuarios verificados pueden enviar mensajes",icon='🔒')
    st.caption("Solicta la verificación a un administrador o profesor")


if st.session_state.chatHistory == [] and st.session_state.firstTime == '':
    gretting =  asyncio.run(generate_response("Presentate con el usuario y dale la bienvenida, dale ejemplos de preguntas que puede hacer"))
    st.session_state.firstTime = gretting
    st.session_state.text_stream = gretting

    with st.chat_message("assistant"):
        st.write_stream(stream_text)
else:
    with st.chat_message("assistant"):
        st.write(st.session_state.firstTime)


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
        {'id':'chatbot','icon': "bi bi-chat-left-text", 'label':"Chatbot",'ttip':"Chatbot de CAPPA"},
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
        {'id':'chatbot','icon': "bi bi-chat-left-text", 'label':"Chatbot",'ttip':"Chatbot de CAPPA"},
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

    if menu_id == "Inicio":
        st.switch_page("pages/app.py")

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




prompt = st.chat_input("Escribe tu mensaje",disabled=(st.session_state.user is not None and not st.session_state.user.is_verified()))


for message in st.session_state.chatHistory:
    if message['role'] == 'user':
        if st.session_state.userinfo is not None and 'avatar' in st.session_state.userinfo:
            if 'url' in st.session_state.userinfo['avatar']:
                avatar = st.session_state.userinfo['avatar']['url']
            else:
                avatar = None
        else:
            avatar = None
        with st.chat_message("user",avatar=avatar):
            if message == st.session_state.chatHistory[-1] and st.session_state.stream_last:
                st.session_state.text_stream = message['parts'][0]
                st.write_stream(stream_text)
                st.session_state.stream_last = False
            else:
                st.write(message['parts'][0])
    else:
        with st.chat_message("assistant"):
            if message == st.session_state.chatHistory[-1] and st.session_state.stream_last:
                st.session_state.text_stream = message['parts'][0]
                st.write_stream(stream_text)
                st.session_state.stream_last = False
            else:
                st.write(message['parts'][0])



if prompt and prompt != '':
    question =  {
        'role': 'user',
        'parts': [prompt]
    }

    st.session_state.chatHistory.append(question)

    try:
        response =  asyncio.run(generate_response(st.session_state.chatHistory))
        r = {
            'role': 'model',
            'parts': [response]
        }
        st.session_state.chatHistory.append(r)
        st.session_state.stream_last = True
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")
        del st.session_state.chatHistory[-1]
        st.rerun()


