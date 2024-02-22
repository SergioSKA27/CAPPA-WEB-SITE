# trunk-ignore-all(isort)
import asyncio

import time
import subprocess
import tracemalloc
from functools import wraps
from time import perf_counter, sleep
from types import SimpleNamespace

import google.generativeai as genai
import hydralit_components as hc
import streamlit as st
from streamlit import session_state as state
from streamlit_elements import elements, event, lazy, mui, sync
from streamlit_extras.switch_page_button import switch_page
import extra_streamlit_components as stx
from st_xatadb_connection import XataConnection

from modules import Card, Dashboard, Editor, Timer
from Clases import Usuario,Autenticador,Runner

# Autor: Sergio Lopez


# --------------------------------------------- page config ---------------------------------------------
# basic page configuration
st.set_page_config(
    page_title="CAPPA",
    page_icon="rsc/Logos/LOGO_CAPPA.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": """# Web Site Club de Algoritmia Avanzada en Python.
                        Todos los derechos reservados 2023, CAPA.""",
    },
)

st.markdown(
    """
<style>
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
div.stSpinner > div {
    text-align:right;
    align-items: right;
    justify-content: right;
  }
</style>
""",
    unsafe_allow_html=True,
)

xata = st.connection("xata", type=XataConnection)
genai.configure(api_key=st.secrets["GEN_AI_KEY"])

# ---------------------------------Funciones---------------------------------
def get_manager():
    return stx.CookieManager()

def stream_text():
    """Stream text to the app"""
    for w in st.session_state.explainstr.split(" "):
        yield w + " "
        sleep(0.05)



@st.cache_resource
def load_genmodel():
    return genai.GenerativeModel("gemini-pro")

async def generate_explanation(prompt):
    """Generate an explanation for the code"""
    model = load_genmodel()
    try:
        response = model.generate_content(prompt)
    except Exception as e:
        response = f"Error generando explicación {e} 🤯\n Intente Nuevamente dentro de unos minutos"
    await asyncio.sleep(10)
    return response


def set_explanin():
    st.session_state.explanin = True


def set_reruncode():
    st.session_state.reruncode = True

async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')


if "explainstr" not in st.session_state:
    st.session_state.explainstr = ""
if "explanin" not in st.session_state:
    st.session_state.explanin = False

if "reruncode" not in st.session_state:
    st.session_state.reruncode = False

if st.session_state.reruncode:
    st.session_state.reruncode = False
    sync()

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


##---------------------------------Navbar---------------------------------


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

    over_theme = {"txc_inactive": "#FFFFFF", "menu_background": "#3670a0"}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name="Inicio",
        login_name=None,
        hide_streamlit_markers=False,  # will show the st hamburger as well as the navbar now!
        sticky_nav=True,  # at the top or not
        sticky_mode="sticky",  # jumpy or not-jumpy, but sticky or pinned
        first_select=40,
    )


    if menu_id == "Inicio":
        st.switch_page("pages/app.py")

    if menu_id == 'logout':
        st.session_state.auth_state = False
        st.session_state.userinfo = None
        st.session_state.user = None
        st.session_state.username = None
        cookie_manager.delete('Validado')
        st.session_state.logout = True

    if  menu_id == 'courses':
        st.switch_page('pages/CoursesHome.py')

    if st.session_state.user is not None and menu_id == st.session_state.user.usuario:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        st.switch_page('pages/profile_render.py')

    if st.session_state.user is not None and (
        st.session_state.user.is_admin()
        or st.session_state.user.is_teacher()
    ):
        if menu_id == "subid144":
            st.switch_page("pages/test_editor.py")

        if menu_id == "doceditor":
            st.switch_page("pages/doc_editor.py")

        if menu_id == "docshome":
            st.switch_page("pages/docs_home.py")

        if menu_id == "subid44":
            st.switch_page("pages/problems_editor.py")

        if menu_id == "subid00":
            st.switch_page("pages/problems_home.py")
    else:
        if menu_id == "docs":
            st.switch_page("pages/docs_home.py")

        if menu_id == "Problemas":
            st.switch_page("pages/problems_home.py")
else:
    asyncio.run(show_message_error())
    st.stop()

# ---------------------------------Body---------------------------------
runner = Runner()

if "w_code" not in state:
    board = Dashboard()
    w = SimpleNamespace(
        dashboard=board,
        editor=Editor(
            board,
            0,
            0,
            8,
            11,
        ),
        timer=Timer(
            board,
            11,
            0,
            4,
            6,
        ),
        card=Card(
            board,
            11,
            6,
            4,
            6,
        ),
    )
    state.w_code = w
    w.editor.add_tab("Code", "print('Hello world!')", "python")


else:
    w = state.w_code

with elements("editorcodigo"):
    event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
    with w.dashboard(rowHeight=57):
        w.editor()
        runner.run(w.editor.get_content("Code"))
        w.timer(
            [runner.stdout, runner.stderr],runner.time,runner.memory,runner.peakmemory,set_explanin,set_reruncode
        )
        w.card(
            "Editor de Código",
            "https://assets.digitalocean.com/articles/how-to-code-in-python-banner/how-to-code-in-python.png",
        )
    if st.session_state.explanin:
        model = load_genmodel()
        prompt = f"Explica el error {runner.stderr}, este es el código: {w.editor.get_content('Code')}"
        with st.spinner("🧠 Generando explicación..."):
            response = asyncio.run(generate_explanation(prompt))

        with st.expander("💡 Explicación", expanded=True):
            st.session_state.explainstr = response.text
            st.write_stream(stream_text)

        st.session_state.explanin = False






with st.expander("Salida"):
    if len(runner.stdout) > 1000:
        st.write(runner.stdout[:1000])
        st.write("...")
    else:
        st.text(runner.stdout)

    st.write(f":red[{runner.stderr}]")

st.caption(
    "Si el editor no se muestra correctamente, por favor recargue la página. Disculpe las molestias."
)
# ---------------------------------Footer---------------------------------
with open("rsc/html/minimal_footer.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)
