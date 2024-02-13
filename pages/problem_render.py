import subprocess
import tracemalloc
from time import perf_counter, sleep
from types import SimpleNamespace
import time
import extra_streamlit_components as stx
import google.generativeai as genai
import hydralit_components as hc
import streamlit as st
from st_xatadb_connection import XataConnection
from streamlit import session_state as state
from streamlit_elements import elements, event, lazy, mui, sync
from streamlit_pills import pills
from streamlit_profiler import Profiler
from Clases import Usuario,Autenticador

from modules import Card, Dashboard, DataGrid, Editor, Pie, Player, Radar, Timer

# Autor: Sergio Lopez


# --------------------------------------------- page config ---------------------------------------------
# basic page configuration
st.set_page_config(
    page_title="CAPA",
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
xata = st.connection("xata", type=XataConnection)
genai.configure(api_key=st.secrets["GEN_AI_KEY"])
st.markdown(
    """
<style>
[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}
.st-emotion-cache-152jn8i {
  position: absolute;
  background: rgb(244, 235, 232);
  color: rgb(49, 51, 63);
  inset: 0px;
    top: 0px;
  overflow: hidden;
  top: 0px;
}

.st-emotion-cache-z5fcl4 {
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  padding-bottom: 0;
}
</style>
""",
    unsafe_allow_html=True,
)


def stream_text():
    """Stream text to the app"""
    for w in st.session_state.explainstr.split(" "):
        yield w + " "
        sleep(0.05)


def format_date(date: str):
    dt = date.split("-")
    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]

    return f"{dt[2]} de {meses[int(dt[1])-1]} del {dt[0]}"


@st.cache_resource
def load_genmodel():
    return genai.GenerativeModel("gemini-pro")


def run_code(code, timeout=1, test_file: bytes = None):
    """Run code and capture the output"""
    try:
        if test_file:
            result = subprocess.run(
                ["python", "-c", code],
                capture_output=True,
                text=True,
                timeout=timeout,
                stdin=test_file,
            )
        else:
            result = subprocess.run(
                ["python", "-c", code], capture_output=True, text=True, timeout=timeout
            )
        return result.stdout, result.stderr
    except subprocess.TimeoutExpired or Exception as e:
        return "", "TimeoutExpired"


def execute_code(code, timeout=1, test_file: bytes = None):
    s = perf_counter()
    result = run_code(code, timeout, test_file)
    cu, p = tracemalloc.get_traced_memory()
    e = perf_counter()
    return result, e - s, cu, p


if "query" not in state or state.query["Table"] != "Problema":
    st.switch_page("pages/problems_home.py")
else:
    # st.write(state.query)
    if "current_problem" not in state:
        state.current_problem = xata.get("Problema", state.query["id"])
    else:
        if state.current_problem["id"] != state.query["id"]:
            state.current_problem = xata.get(
                "Problema",
                state.query["id"],
                columns=[
                    "nombre",
                    "dificultad",
                    "score",
                    "time_limit",
                    "tags",
                    "desc",
                    "creador.nombre_completo",
                    "correct_ans",
                    "graph_code",
                ],
            )

# st.write(state.current_problem)


def set_explanin():
    st.session_state.explanin = True


def set_reruncode():
    st.session_state.reruncode = True


if "explainstr" not in st.session_state:
    st.session_state.explainstr = ""

if "explanin" not in st.session_state:
    st.session_state.explanin = False

if "reruncode" not in st.session_state:
    st.session_state.reruncode = False

if st.session_state.reruncode:
    st.session_state.reruncode = False
    sync()


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


# ---------------------------------Navbar---------------------------------
if auth():
    if st.session_state.user.is_admin() or st.session_state.user.is_teacher():
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':'subid44','icon': "bi bi-journal-code", 'label':"Editor"}
        ]},
        {"id": "prender","icon": "bi bi-lightbulb","label": "Problema","ttip": "Visualizar Problema"},
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
        {"id": "prender","icon": "bi bi-lightbulb","label": "Problema","ttip": "Visualizar Problema"},
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
    first_select=20,
    )


    if menu_id == "Inicio":
        st.switch_page("pages/app.py")

    if menu_id == "code":
        st.switch_page("pages/code_editor.py")

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

    if st.session_state.user.is_admin() or st.session_state.user.is_teacher():
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
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')
    st.stop()

# ---------------------------------Main---------------------------------#


tags = [
    "Programación Dinámica",
    "Divide Y Vencerás",
    "Backtracking",
    "Grafos",
    "Programación Greedy",
    "Árboles",
    "Listas",
    "Pilas",
    "Colas",
    "Deques",
    "Diccionarios" "Matrices",
    "Ordenamiento",
    "Búsqueda Binaria",
    "Cadenas",
    "Recursividad",
    "Geometría",
    "Orden Topológico",
    "String Matching",
    "Conjuntos",
    "Bit Manipulation",
    "Programación De Redes",
    "Programación Concurrente",
    "Árboles Binarios",
    "Gráficos",
    "Optimización",
    "Matemáticas",
    "Álgebra",
    "Teoría De Números",
    "Programación Condicional",
    "Programación Funcional",
    "Combinatoria",
    "Probabilidad",
    "Manejo De Archivos",
    "Inteligencia Artificial",
    "Machine Learning",
    "Redes Neuronales",
    "Visión Por Computadora",
    "Procesamiento De Lenguaje Natural",
    "Automatización",
]

emojis_tags = [
    "💡",  # Programación Dinámica
    "🔍",  # Divide Y Vencerás
    "🔄",  # Backtracking
    "📊",  # Grafos
    "🤔",  # Programación Greedy
    "🌲",  # Árboles
    "📑",  # Listas
    "🔄",  # Pilas
    "🔄",  # Colas
    "🔄",  # Deques
    "📚",  # Diccionarios
    "🧮",  # Matrices
    "🔍",  # Ordenamiento
    "👾",  # Búsqueda Binaria
    "🔄",  # Cadenas
    "📐",  # Recursividad
    "🔼",  # Geometría
    "🔄",  # Orden Topológico
    "🔄",  # String Matching
    "💡",  # Conjuntos
    "🌐",  # Bit Manipulation
    "🔄",  # Programación De Redes
    "🌳",  # Programación Concurrente
    "📊",  # Árboles Binarios
    "⚙️",  # Gráficos
    "🔢",  # Optimización
    "🧮",  # Matemáticas
    "🔢",  # Álgebra
    "🔄",  # Teoría De Números
    "📜",  # Programación Condicional
    "♾️",  # Programación Funcional
    "🎲",  # Combinatoria
    "📂",  # Probabilidad
    "🤖",  # Manejo De Archivos
    "🧠",  # Inteligencia Artificial
    "🌐",  # Machine Learning
    "👀",  # Redes Neuronales
    "🗣️",  # Visión Por Computadora
    "⚡ ",  # Procesamiento De Lenguaje Natural
]


rtags = []
remojis_tags = []

cols = st.columns([0.7, 0.3])

if state.current_problem["dificultad"] == 1:
    rtags.append("Fácil")
    remojis_tags.append("🐛")
elif state.current_problem["dificultad"] == 2:
    rtags.append("Intermedio")
    remojis_tags.append("🐍")
else:
    rtags.append("Difícil")
    remojis_tags.append("🐉")

for tag in state.current_problem["tags"]:
    rtags.append(tag)
    remojis_tags.append(emojis_tags[tags.index(tag)])


with cols[1]:
    with st.container(border=True):
        st.image("https://source.unsplash.com/800x600/?python", use_column_width=True)
        st.title(state.current_problem["nombre"])
        st.caption(
            f"""
        :blue[**Puntaje**:] {state.current_problem['score']}

        :green[**Tiempo límite**:] {state.current_problem['time_limit']}s

        **Publicado:** {format_date(state.current_problem['xata']['createdAt'][:10])}

        """
        )
        pills("Etiquetas", rtags, remojis_tags)

        st.subheader("Envía tu solución")
        file_code = st.file_uploader("Sube tu código", type=["py"])

        useeditorcode = st.checkbox("Enviar código desde el editor")
        st.button("Enviar Solución", use_container_width=True)


if "w_prender" not in state:
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
    state.w_prender = w
    w.editor.add_tab("Code", "print('Hello world!')", "python")


else:
    w = state.w_prender

with elements("workspace"):
    event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
    with w.dashboard(rowHeight=57):
        w.editor()
        content = w.editor.get_content("Code")
        result = execute_code(w.editor.get_content("Code"), timeout=3)
        w.timer(
            result[0], str(result[1]), result[2], result[3], set_explanin, set_reruncode
        )
        w.card(
            "Editor de Código",
            "https://assets.digitalocean.com/articles/how-to-code-in-python-banner/how-to-code-in-python.png",
        )
    if st.session_state.explanin:
        model = load_genmodel()
        prompt = f"Explica el error {result[0][1]} del código: {w.editor.get_content('Code')}"
        with st.spinner("🧠 Generando explicación..."):
            response = model.generate_content(prompt)

        with st.expander("💡 Explicación", expanded=True):
            st.session_state.explainstr = response.text
            st.write_stream(stream_text)

        st.session_state.explanin = False

with cols[0]:
    st.markdown(state.current_problem["desc"], unsafe_allow_html=True)


# ---------------------------------Footer---------------------------------#
with open("rsc/html/minimal_footer.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)
