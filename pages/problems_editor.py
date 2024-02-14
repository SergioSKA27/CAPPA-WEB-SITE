import subprocess
import tracemalloc
from time import perf_counter, sleep
from types import SimpleNamespace
import time
import asyncio
import hydralit_components as hc
import streamlit as st
from st_xatadb_connection import XataConnection
import extra_streamlit_components as stx
from streamlit import session_state as state
from streamlit_elements import elements, event, lazy, mui, sync,partial
from streamlit_quill import st_quill
import google.generativeai as genai
from modules import Card, Dashboard, Editor, Timer
from Clases import Usuario,Autenticador


#Autor: Sergio Lopez



#--------------------------------------------- page config ---------------------------------------------
#basic page configuration
st.set_page_config(
    page_title='CAPA',
    page_icon="rsc/Logos/LOGO_CAPPA.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': """# Web Site Club de Algoritmia Avanzada en Python.
                        Todos los derechos reservados 2023, CAPA."""
    }
)
xata = st.connection('xata',type=XataConnection)
genai.configure(api_key=st.secrets["GEN_AI_KEY"])

st.markdown('''
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
''', unsafe_allow_html=True)


#--------------------------------------------- Funciones ---------------------------------------------

def stream_text():
    """Stream text to the app"""
    for w in st.session_state.explainstr.split(' '):
        yield w + " "
        sleep(0.05)

@st.cache_resource
def load_genmodel():
    return genai.GenerativeModel("gemini-pro")

async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')


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

def update_pname(event):
	st.session_state.pname = event.target.value

def update_difficulty(event):
	st.session_state.difficulty = event.props.value

def update_tags(event,value):
	st.session_state.ptags = value

	if value.props.value in st.session_state.tagslist:
		del st.session_state.tagslist[st.session_state.tagslist.index(value.props.value)]
	else:
		st.session_state.tagslist.append(value.props.value)

def update_score(event):
	st.session_state.pscore = event.target.value

def update_timelimit(event):
	st.session_state.timelimit = event.target.value

if 'pname' not in st.session_state:
	st.session_state.pname = ""

if 'difficulty' not in st.session_state:
	st.session_state.difficulty = None


if 'ptags' not in st.session_state:
	st.session_state.ptags = []

if 'tagslist' not in st.session_state:
	st.session_state.tagslist = []

if 'pscore' not in st.session_state:
	st.session_state.pscore = 0

if 'timelimit' not in st.session_state:
	st.session_state.timelimit = 0


def set_explanin():
    st.session_state.explanin = True

def set_reruncode():
    st.session_state.reruncode = True


if 'explainstr' not in st.session_state:
    st.session_state.explainstr = ""
if 'explanin' not in st.session_state:
    st.session_state.explanin =  False

if 'reruncode' not in st.session_state:
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

##---------------------------------Navbar---------------------------------
if auth():
    if st.session_state.user is not None and  (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",'id':'subid00'},
        {'id':'subid44','icon': "bi bi-journal-code", 'label':"Editor"},
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
        st.error("403 No tienes permisos para acceder a esta página")
        st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
        st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')
        st.stop()


    over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
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


    if menu_id == 'Inicio':
        st.switch_page('pages/app.py')

    if menu_id == 'subid00':
        st.switch_page('pages/problems_home.py')

    if menu_id == 'docshome':
        st.switch_page('pages/docs_home.py')

    if menu_id == 'doceditor':
        st.switch_page('pages/doc_editor.py')

    if menu_id == 'code':
        st.switch_page('pages/code_editor.py')

    if menu_id == 'subid144':
        st.switch_page('pages/test_editor.py')

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


#------------------------------------- body ---------------------------------------------------------
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
    "Diccionarios"
    "Matrices",
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

with elements("header"):
	with mui.Box(sx={"display": "flex", "flexDirection": "row", "alignItems": "center", "justifyContent": "center"}):
		mui.icon.IntegrationInstructions(sx={"fontSize": "4.2vw","color": "#36A0A0"})
		mui.Typography("Editor de Problemas", sx={"fontFamily": "Monospace","fontSize": "4.2vw","fontWeight": "bold","letterSpacing": 10})

	mui.Divider()


desc = ""
with st.form(key='my_form'):
  desc = st_quill(placeholder='Descripción del Problema', html=True,key='quill1')
  editcols = st.columns([0.8,0.2])

  with editcols[1]:
    savedesc = st.form_submit_button(label='Guardar Descripción 💾',use_container_width=True)
  if savedesc:
    st.markdown("##### Preview")
    st.markdown(desc, unsafe_allow_html=True)


with elements("new_element"):
	with mui.Box(sx={"display": "flex", "flexDirection": "row", "alignItems": "center"}):
		mui.icon.Abc()
		mui.TextField(id="problem_name", label="Nombre del Problema", sx={"margin": "10px","width":"100%"},variant="filled",onChange=lazy(update_pname))

		mui.icon.Upgrade()
		with mui.FormControl(sx={"width":"100%", "margin": "10px"}):
			mui.InputLabel("Dificultad",id="Difficulty")
			mui.Select(mui.MenuItem("Basico", value="1"),
						mui.MenuItem("Intermedio", value="2"),
						mui.MenuItem("Avanzado", value="3"),
						labelId="Difficulty", id="difficulty",
						label="Dificultad", value=st.session_state.difficulty.props.value if st.session_state.difficulty else "Basico",
						onChange=sync(None,'difficulty'),
						)

	with mui.Box(sx={"display": "flex", "flexDirection": "row", "alignItems": "center"}):
		mui.icon.Tag()
		with mui.FormControl(sx={"width":"100%", "margin": "10px"}):
			mui.InputLabel("Etiquetas",id="Tags")
			with mui.Select(value=st.session_state.tagslist, multiple=True,
			labelId="Tags", id="tags", label="Etiquetas", sx={"width":"100%"}, onChange=partial(update_tags)) :
				for tag in tags:
					mui.MenuItem(tag, value=tag)

	with mui.Box(sx={"display": "flex", "flexDirection": "row", "alignItems": "center"}):
		mui.icon.Star()
		mui.TextField(id="score", label="Puntaje", sx={"margin": "10px","width":"50%"},
						variant="filled", type="number",InputLabelProps={"shrink":True},
						onChange=lazy(update_score))

		mui.icon.Timer()
		mui.TextField(id="time_limit", label="Tiempo Limite(Segundos)", sx={"margin": "10px","width":"50%"},
						variant="filled", type="number",InputLabelProps={"shrink":True},onChange=lazy(update_timelimit))

	with mui.Box(sx={"display": "flex", "alignItems": "left", "justifyContent": "flex-end"}):
		mui.Button(mui.icon.Save,"Guardar", sx={"margin": "10px"}, variant="contained", color="primary",onClick=sync())





cols = st.columns(2)
graph = cols[0].checkbox('Añadir grafica')


g_desc = ""

if graph:
  g_desc = st.text_area('Grafica','''
    digraph D {

  subgraph cluster_p {
    label = "Parent";

    subgraph cluster_c1 {
      label = "Child one";
      a;

      subgraph cluster_gc_1 {
        label = "Grand-Child one";
         b;
      }
      subgraph cluster_gc_2 {
        label = "Grand-Child two";
          c;
          d;
      }

    }

    subgraph cluster_c2 {
      label = "Child two";
      e;
    }
  }
}
''', height=200)

  st.graphviz_chart(g_desc)



if "w_editorp" not in state:
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
    state.w_editorp = w
    w.editor.add_tab("Code", "print('Hello world!')", "python")


else:
    w = state.w_editorp

with elements("workspace"):
    event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
    with w.dashboard(rowHeight=57):
        w.editor()
        content = w.editor.get_content("Code")
        result =  execute_code(w.editor.get_content("Code"), timeout=3)
        w.timer(result[0],str(result[1]),result[2],result[3],set_explanin,set_reruncode)
        w.card("Editor de Código","https://assets.digitalocean.com/articles/how-to-code-in-python-banner/how-to-code-in-python.png")

    if st.session_state.explanin:
        model = load_genmodel()
        prompt = f"Explica el error {result[0][1]} del código: {w.editor.get_content('Code')}"
        with st.spinner("🧠 Generando explicación..."):
            response =  model.generate_content(prompt)

        with st.expander("💡 Explicación", expanded=True):
            st.session_state.explainstr = response.text
            st.write_stream(stream_text)

        st.session_state.explanin = False

with st.container(height=200):
    st.write('### Salida')
    st.text(result[0][0])
    st.write(f":red[{result[0][1]}]")

st.write('### Ingrese la respuesta correcta')
useoutput = st.checkbox('Usar la salida del código como respuesta correcta(Maximo 250 caracteres)')
cans = st.text_area('Respuesta correcta(250 caracteres maximo)','**Respuesta correcta(puede ser una expresion regular)**', height=200)

upcols = st.columns([0.3,0.4,0.3])

if upcols[1].button('Subir Problema 🚀',use_container_width=True):
  if desc == "":
    st.warning('Debe ingresar una descripción y guardarla antes de subir el problema')
    st.stop()
  if st.session_state.pname == "":
    st.warning('Debe ingresar un nombre para el problema')
    st.stop()
  if useoutput and cans == "":
    st.warning('El codigo no tiene salida, por favor ingrese una respuesta correcta')
    st.stop()
  if st.session_state.tagslist == []:
    st.warning('Debe ingresar al menos una etiqueta')
    st.stop()
  if cans == "" and not useoutput:
    st.warning('Debe ingresar una respuesta correcta')
    st.stop()
  try:
    r = xata.insert("Problema", {
    "nombre": st.session_state.pname,
    "tags": st.session_state.tagslist,
    "dificultad": int(st.session_state.difficulty.props.value),
    "score": int(st.session_state.pscore),
    "time_limit": int(st.session_state.timelimit),
    "desc": desc,
    "graph_code": g_desc,
    "correct_ans": str(result[0]) if useoutput else cans,
    "creador": st.session_state['username'],
  })
    st.success('Problema subido correctamente')
    st.write(r)
    st.balloons()
  except Exception as e:
    st.error(f'Error al subir el problema: {e}')

#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
