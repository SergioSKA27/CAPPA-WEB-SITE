# trunk-ignore-all(isort)
import asyncio


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

from modules import Card, Dashboard, Editor, Timer

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

div.stSpinner > div {
    text-align:center;
    align-items: center;
    justify-content: center;
  }
</style>
""",
    unsafe_allow_html=True,
)

genai.configure(api_key=st.secrets["GEN_AI_KEY"])
if "auth_state" not in st.session_state or st.session_state["auth_state"] == False:
    # Si no hay un usuario logeado, se muestra la pagina de login
    switch_page("login")


# ---------------------------------Funciones---------------------------------


def stream_text():
    """Stream text to the app"""
    for w in st.session_state.explainstr.split(" "):
        yield w + " "
        sleep(0.05)


def measure_performance(func):
    """Measure performance of a function"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        start_time = perf_counter()
        func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        finish_time = perf_counter()
        st.write(f"Function: {func.__name__}")
        st.write(f"Method: {func.__doc__}")
        st.write(
            f"Memory usage:\t\t {current / 10**6:.6f} MB \n"
            f"Peak memory usage:\t {peak / 10**6:.6f} MB "
        )
        st.write(f"Time elapsed is seconds: {finish_time - start_time:.6f}")
        st.write(f'{"-"*40}')
        tracemalloc.stop()

    return wrapper


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


if "explainstr" not in st.session_state:
    st.session_state.explainstr = ""
if "explanin" not in st.session_state:
    st.session_state.explanin = False

if "reruncode" not in st.session_state:
    st.session_state.reruncode = False

if st.session_state.reruncode:
    st.session_state.reruncode = False
    sync()

##---------------------------------Navbar---------------------------------
if (
    st.session_state.user.is_admin()
    or st.session_state.user.is_professor()
    or st.session_state.user.is_moderator
):
    menu_data = [
        {
            "icon": "bi bi-cpu",
            "label": "Problemas",
            "ttip": "Problemas de Programación",
            "submenu": [
                {"id": "subid00", "icon": "bi bi-search", "label": "Todos"},
                {"id": "subid44", "icon": "bi bi-gear", "label": "Editor"},
            ],
        },
        {"id": "contest", "icon": "bi bi-trophy", "label": "Concursos"},
        {
            "icon": "bi bi-graph-up",
            "label": "Analisis de Datos",
            "ttip": "Herramientas de Analisis de Datos",
        },
        {
            "id": "docs",
            "icon": "bi bi-file-earmark-richtext",
            "label": "Blog",
            "ttip": "Articulos e Información",
            "submenu": [
                {"id": "doceditor", "icon": "bi bi-gear", "label": "Editor"},
                {"id": "docshome", "icon": "bi bi-search", "label": "Home"},
            ],
        },
        {"id": "code", "icon": "bi bi-code-square", "label": "Editor de Código"},
        {
            "icon": "bi bi-pencil-square",
            "label": "Tests",
            "submenu": [
                {"label": "Todos", "icon": "bi bi-search", "id": "alltests"},
                {"id": "subid144", "icon": "bi bi-gear", "label": "Editor"},
            ],
        },
        {"id": "logout", "icon": "bi bi-door-open", "label": "Cerrar Sesión"},
    ]
else:
    menu_data = [
        {
            "icon": "bi bi-cpu",
            "label": "Problemas",
            "ttip": "Problemas de Programación",
            "id": "Problemas",
        },
        {"id": "contest", "icon": "bi bi-trophy", "label": "Concursos"},
        {
            "icon": "bi bi-graph-up",
            "label": "Analisis de Datos",
            "ttip": "Herramientas de Analisis de Datos",
        },
        {
            "id": "docs",
            "icon": "bi bi-file-earmark-richtext",
            "label": "Blog",
            "ttip": "Articulos e Información",
        },
        {"id": "code", "icon": "bi bi-code-square", "label": "Editor de Código"},
        {"icon": "bi bi-pencil-square", "label": "Tests"},
        {"id": "logout", "icon": "bi bi-door-open", "label": "Cerrar Sesión"},
    ]

logname = st.session_state.user.usuario

over_theme = {"txc_inactive": "#FFFFFF", "menu_background": "#3670a0"}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name="Inicio",
    login_name=logname,
    hide_streamlit_markers=False,  # will show the st hamburger as well as the navbar now!
    sticky_nav=True,  # at the top or not
    sticky_mode="sticky",  # jumpy or not-jumpy, but sticky or pinned
    first_select=50,
)


if menu_id == "Inicio":
    switch_page("Main")

if menu_id == "Analisis de Datos":
    switch_page("data_analysis_home")

if menu_id == "logout":
    st.session_state.pop("auth_state")
    st.session_state.pop("userinfo")
    st.session_state.pop("username")
    switch_page("login")


if menu_id == st.session_state.user.usuario:
    if "query" not in st.session_state:
        st.session_state.query = {"Table": "Usuario", "id": st.session_state.user.key}
    else:
        st.session_state.query = {"Table": "Usuario", "id": st.session_state.user.key}
    switch_page("profile_render")

if (
    st.session_state["userinfo"]["rol"] == "Administrador"
    or st.session_state["userinfo"]["rol"] == "Profesor"
    or st.session_state["userinfo"]["rol"] == "Moderador"
):
    if menu_id == "subid144":
        switch_page("test_editor")

    if menu_id == "doceditor":
        switch_page("doc_editor")

    if menu_id == "docshome":
        switch_page("docs_home")

    if menu_id == "subid44":
        switch_page("problems_editor")

    if menu_id == "subid00":
        switch_page("problems_home")
else:
    if menu_id == "docs":
        switch_page("docs_home")

    if menu_id == "Problemas":
        switch_page("problems_home")


# ---------------------------------Body---------------------------------


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
        prompt = f"Explica el error {result[0][1]}, este es el código: {w.editor.get_content('Code')}"
        with st.spinner("🧠 Generando explicación..."):
            response = asyncio.run(generate_explanation(prompt))

        with st.expander("💡 Explicación", expanded=True):
            st.session_state.explainstr = response.text
            st.write_stream(stream_text)

        st.session_state.explanin = False


with st.expander("Salida"):
    if len(result[0][0]) > 1000:
        st.write(result[0][0][:1000])
        st.write("...")
    else:
        st.text(result[0][0])

    st.write(f":red[{result[0][1]}]")


# ---------------------------------Footer---------------------------------
with open("rsc/html/minimal_footer.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)
