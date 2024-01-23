import streamlit as st
import hydralit_components as hc
from streamlit_extras.switch_page_button import switch_page
from code_editor import code_editor
import subprocess
import tracemalloc
from types import SimpleNamespace
from time import perf_counter
from streamlit_profiler import Profiler
from streamlit_quill import st_quill
from streamlit import session_state as state
from streamlit_elements import elements, event, lazy, mui, sync
from streamlit_extras.switch_page_button import switch_page
from streamlit_profiler import Profiler
from st_xatadb_connection import XataConnection

from modules import Card, Dashboard, DataGrid, Editor, Pie, Player, Radar, Timer
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
  }
</style>
''', unsafe_allow_html=True)


if 'auth_state' not in st.session_state:
    switch_page('login')


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
#Navbar
menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':' subid11','icon': "bi bi-flower1", 'label':"Basicos"},
            {'id':'subid22','icon': "fa fa-paperclip", 'label':"Intermedios"},
            {'id':'subid33','icon': "bi bi-emoji-dizzy", 'label':"Avanzados"},
            {'id':'subid44','icon': "bi bi-gear", 'label':"Editor"}
        ]},
        {'id':'contest','icon': "bi bi-trophy", 'label':"Concursos"},
        {'icon': "bi bi-graph-up", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Docs"},
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests", 'submenu':[
            {'label':"Basicos 1", 'icon': "🐛"},
            {'icon':'🐍','label':"Intermedios"},
            {'icon':'🐉','label':"Avanzados",},
            {'id':'subid144','icon': "bi bi-gear", 'label':"Editor" }]},
        {'id':'About','icon':"bi bi-question-circle",'label':"FAQ"},
        {'id':'contact','icon':"bi bi-envelope",'label':"Contacto"},
        {'id':'logout','icon': "bi bi-door-open", 'label':"Logout"},#no tooltip message
    ]

over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Inicio',
        login_name=st.session_state['userinfo']['username'],
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
        first_select=10,
    )


if menu_id == 'Inicio':
  switch_page('Main')

if menu_id == 'subid00':
    switch_page('problems_home')


if menu_id == 'code':
    switch_page('code_editor')

if menu_id == 'subid144':
    switch_page('test_editor')

if menu_id == 'logout':
    st.session_state.pop('auth_state')
    st.session_state.pop('userinfo')
    st.session_state.pop('username')
    switch_page('login')

#------------------------------------- body ---------------------------------------------------------
st.title('Editor de Problemas 👨‍💻')
st.divider()


pname =st.text_input('Ingrese el nombre del Problema',placeholder="Problema 1")

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
tags = st.multiselect("Seleccione las etiquetas", tags,placeholder="Listas, Grafos, Programación Dinámica, etc",max_selections=5)


ops = st.columns(3)
dif = {'Basico': 1,'Intermedio': 2,'Avanzado': 3}
dificulty = ops[0].selectbox('Dificultad',['Basico','Intermedio','Avanzado'])
score = ops[1].number_input('Puntaje',min_value=100,max_value=1000,step=1)
timelimit = ops[2].number_input('Tiempo limite(en segundos)',min_value=1,max_value=5,step=1)

st.write('### Ingrese la descripción del Problema')

desc = ""
with st.form(key='my_form'):
  desc = st_quill(placeholder='Descripción del Problema', html=True,key='quill1')
  editcols = st.columns([0.8,0.2])

  with editcols[1]:
    savedesc = st.form_submit_button(label='Guardar Descripción 💾',use_container_width=True)
  if savedesc:
    st.markdown("##### Preview")
    st.markdown(desc, unsafe_allow_html=True)



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
			6,
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




st.write('### Ingrese la respuesta correcta')
useoutput = st.checkbox('Usar la salida del código como respuesta correcta(Maximo 250 caracteres)')
cans = st.text_area('Respuesta correcta(250 caracteres maximo)','**Respuesta correcta(puede ser una expresion regular)**', height=200)

upcols = st.columns([0.3,0.4,0.3])

if upcols[1].button('Subir Problema 🚀',use_container_width=True):
  if desc == "":
    st.warning('Debe ingresar una descripción y guardarla antes de subir el problema')
    st.stop()
  if pname == "":
    st.warning('Debe ingresar un nombre para el problema')
    st.stop()
  if useoutput and cans == "":
    st.warning('El codigo no tiene salida, por favor ingrese una respuesta correcta')
    st.stop()
  if tags == []:
    st.warning('Debe ingresar al menos una etiqueta')
    st.stop()
  if cans == "" and not useoutput:
    st.warning('Debe ingresar una respuesta correcta')
    st.stop()
  try:
    r = xata.insert("Problema", {
    "nombre": pname,
    "tags": tags,
    "dificultad": dif[dificulty],
    "socore": score,
    "time_limit": timelimit,
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



