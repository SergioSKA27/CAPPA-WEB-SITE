import subprocess
import tracemalloc
from functools import wraps
from time import perf_counter
from types import SimpleNamespace

import hydralit_components as hc
import streamlit as st
from code_editor import code_editor
from streamlit import session_state as state
from streamlit_elements import elements, event, lazy, mui, sync
from streamlit_extras.switch_page_button import switch_page
from streamlit_profiler import Profiler

from modules import Card, Dashboard, DataGrid, Editor, Pie, Player, Radar, Timer

# Autor: Sergio Lopez


# --------------------------------------------- page config ---------------------------------------------
# basic page configuration
st.set_page_config(
    page_title="CAPA",
    page_icon=":snake:",
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
  }
</style>
""",
    unsafe_allow_html=True,
)


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
	return result, e-s, cu, p

##---------------------------------
# Navbar
menu_data = [
    {
        "icon": "bi bi-cpu",
        "label": "Problemas",
        "ttip": "Seccion de problemas",
        "submenu": [
            {"id": "subid00", "icon": "bi bi-search", "label": "Todos"},
            {"id": " subid11", "icon": "bi bi-flower1", "label": "Basicos"},
            {"id": "subid22", "icon": "fa fa-paperclip", "label": "Intermedios"},
            {"id": "subid33", "icon": "bi bi-emoji-dizzy", "label": "Avanzados"},
            {"id": "subid44", "icon": "bi bi-gear", "label": "Editor"},
        ],
    },
    {"id": "contest", "icon": "bi bi-trophy", "label": "Concursos"},
    {
        "icon": "bi bi-graph-up",
        "label": "Dashboard",
        "ttip": "I'm the Dashboard tooltip!",
    },  # can add a tooltip message
    {"id": "docs", "icon": "bi bi-file-earmark-richtext", "label": "Docs"},
    {"id": "code", "icon": "bi bi-code-square", "label": "Editor de Código"},
    {
        "icon": "bi bi-pencil-square",
        "label": "Tests",
        "submenu": [
            {"label": "Basicos 1", "icon": "🐛"},
            {"icon": "🐍", "label": "Intermedios"},
            {
                "icon": "🐉",
                "label": "Avanzados",
            },
            {"id": "subid144", "icon": "bi bi-gear", "label": "Editor"},
        ],
    },
    {"id": "About", "icon": "bi bi-question-circle", "label": "FAQ"},
    {"id": "contact", "icon": "bi bi-envelope", "label": "Contacto"},
    {
        "id": "logout",
        "icon": "bi bi-door-open",
        "label": "Logout",
    },  # no tooltip message
]

over_theme = {"txc_inactive": "#FFFFFF", "menu_background": "#3670a0"}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name="Inicio",
    login_name="User",
    hide_streamlit_markers=False,  # will show the st hamburger as well as the navbar now!
    sticky_nav=True,  # at the top or not
    sticky_mode="sticky",  # jumpy or not-jumpy, but sticky or pinned
    first_select=50,
)


if menu_id == "Inicio":
    switch_page("Main")

if menu_id == "logout":
    switch_page("Login")

if menu_id == "subid00":
    switch_page("problems_home")


# --------------------------------------------- page config ---------------------------------------------
# Run the Python code and capture the output
# with Profiler():
#    result = subprocess.run(['python', '-c', editor0['text']], capture_output=True, text=True)
#    with st.expander(label=":blue[Output: ]",expanded=True):
#      st.write(result.stdout, result.stderr)


if "w" not in state:
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
			5,
			4,
			6,
		),
    )
    state.w = w
    w.editor.add_tab("Code", "print('Hello world!')", "python")


else:
    w = state.w

with elements("workspace"):
    event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
    with w.dashboard(rowHeight=57):
        w.editor()
        content = w.editor.get_content("Code")
        result =  execute_code(w.editor.get_content("Code"), timeout=3)
        w.timer(result[0],str(result[1]),result[2],result[3])
        w.card("Editor de Código","https://assets.digitalocean.com/articles/how-to-code-in-python-banner/how-to-code-in-python.png")

