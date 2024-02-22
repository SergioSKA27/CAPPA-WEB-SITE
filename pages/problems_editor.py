import subprocess
import tracemalloc
from time import perf_counter, sleep
from types import SimpleNamespace
import time
import asyncio
import hydralit_components as hc
import streamlit as st
from st_xatadb_connection import XataConnection,XataClient
import extra_streamlit_components as stx
from streamlit import session_state as state
from streamlit_elements import elements, event, lazy, mui, sync,partial
from streamlit_quill import st_quill
import google.generativeai as genai
from modules import Card, Dashboard, Editor, Timer
from Clases import Usuario,Autenticador,Runner
from st_tiny_editor import  tiny_editor


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
client = XataClient(st.secrets["XATA_API_KEY"],db_url=st.secrets["XATA_DB_URL"])
genai.configure(api_key=st.secrets["GEN_AI_KEY"])

st.markdown('''
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

    if  menu_id == 'courses':
        st.switch_page('pages/CoursesHome.py')

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

st.title('🔧Editor de Problemas')
st.divider()




name = st.text_input('Nombre del Problema',key='pname')



cols0 = st.columns(2)
difficulty = cols0[0].selectbox('Dificultad',['Basico','Intermedio','Avanzado'],key='difficulty')

tagss = cols0[1].multiselect('Etiquetas',tags,key='tags',placeholder='Seleccione una o más etiquetas')

cols1 = st.columns(2)
score = cols1[0].number_input('Puntaje',key='pscore',min_value=10,max_value=1000)
tlimit = cols1[1].number_input('Tiempo Limite(Segundos)',key='timelimit',min_value=1,max_value=5)




desc = tiny_editor(st.secrets['TINY_API_KEY'],
  height=600,
  key='desc',
  toolbar = 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | emoticons charmap | removeformat',
  plugins = [
    "advlist", "anchor", "autolink", "charmap", "code",
    "help", "image", "insertdatetime", "link", "lists", "media",
    "preview", "searchreplace", "table", "visualblocks", "accordion",'emoticons',
    ]
  )
editcols = st.columns([0.8,0.2])

with editcols[1]:
    savedesc = st.button(label='Guardar Descripción',use_container_width=True)

if savedesc and desc is not None:
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

runner = Runner()


codeeditcols = st.columns([0.8,0.2])
codeeditcols[0].subheader('Editor de Código')
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



if codeeditcols[1].toggle('Usar Editor legacy',False,help='Si el editor de código no funciona correctamente, activa esta opción'):
    code = st.text_area('Código',key='code',value="print('Hello world!')")
    _,execol = st.columns([0.8,0.2])
    if execol.button('Ejecutar',use_container_width=True):
        runner.run(code)
        if len(runner.stdout) > 1000:
            st.write(f'Salida: {runner.stdout[:1000]}')
            st.write("...")
        else:
            st.text(f'Salida: {runner.stdout}')
        if runner.stderr != "" and runner.stderr is not None:
            st.write(f':red[{runner.stderr}]')
            st.button('Explicar' ,on_click=set_explanin)



        st.write(f'Tiempo: {runner.time} segundos')
        st.write(f'Memoria: {runner.memory} bytes')
        st.write(f'Memoria Pico: {runner.peakmemory} bytes')

    if st.session_state.explanin:
        model = load_genmodel()
        prompt = f"Explica el error {runner.stderr} del código: {code}"
        with st.spinner("🧠 Generando Explicación"):
            response =  model.generate_content(prompt)
        with st.expander("💡 Explicación",expanded=True):
            st.session_state.explainstr = response.text
            st.write_stream(stream_text)
            st.button('Reintentar',on_click=set_explanin)
        st.session_state.explanin = False


else:
    with elements("workspace"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
        with w.dashboard(rowHeight=57):
            w.editor()
            runner.run(w.editor.get_content("Code"))
            w.timer(
                [runner.stdout, runner.stderr],runner.time,runner.memory,runner.peakmemory,set_explanin,set_reruncode
            )
            w.card("Editor de Código","https://assets.digitalocean.com/articles/how-to-code-in-python-banner/how-to-code-in-python.png")

    if st.session_state.explanin:
        model = load_genmodel()
        prompt = f"Explica el error {runner.stderr} del código: {w.editor.get_content('Code')}"
        with st.spinner("🧠 Generando explicación..."):
            response =  model.generate_content(prompt)

        with st.expander("💡 Explicación", expanded=True):
            st.session_state.explainstr = response.text
            st.write_stream(stream_text)

        st.session_state.explanin = False




st.write('### Ingrese la respuesta correcta')
useoutput = st.checkbox('Usar la salida del código como respuesta correcta(Maximo 250 caracteres)')
cans = st.text_area('Respuesta correcta(250 caracteres maximo)','**Respuesta correcta(puede ser una expresion regular)**', height=200)

upcols = st.columns([0.3,0.4,0.3])

dfdic = {'Basico':1,'Intermedio':2,'Avanzado':3}

if upcols[1].button('Subir Problema 🚀',use_container_width=True):
  try:
    r = xata.insert("Problema", {
    "nombre": name,
    "tags": tagss,
    "dificultad": int(dfdic[difficulty]),
    "score": int(score),
    "time_limit": int(tlimit),
    "desc": desc if desc is not None else "",
    "graph_code": g_desc,
    "correct_ans": str(runner.stdout) if useoutput else cans,
    "creador": st.session_state.user.key,
  })
    st.success('Problema subido correctamente')
    st.write(r)
    st.balloons()
  except Exception as e:
    st.error(f'Error al subir el problema: {e}')

#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
