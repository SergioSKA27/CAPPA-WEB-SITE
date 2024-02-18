import streamlit as st
import streamlit_antd_components as sac
import hydralit_components as hc
from streamlit_searchbox import st_searchbox
from streamlit_pills import pills
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from modules import Dashboard, Card, Player
from st_xatadb_connection import XataConnection
import asyncio
import requests
import extra_streamlit_components as stx
from Clases import Usuario,Autenticador
import time

st.set_page_config(layout="wide", page_title="Problemas",initial_sidebar_state="collapsed", page_icon="rsc/Logos/LOGO_CAPPA.jpg")

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
  padding-bottom: 0;
}
</style>
''', unsafe_allow_html=True)


#--------------------------------- Funciones ---------------------------------

async def get_random_image():
    result = await asyncio.to_thread(requests.get, 'https://source.unsplash.com/random/600x400?programming,python,code')
    return result.content

async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')


def search_problem(s: str):
    try:
        res = xata.search_on_table("Problema",{"query": s, "fuzziness": 0, "prefix": "phrase"})
        data = []
        for p in res['records']:
            data.append(','.join([p['nombre'],p['id']]))
        return data if len(data) < 5 else data[:5]
    except:
        return []

def update_problems(query: dict = None,orderquery: dict = None):
    if query is not None:
        if query['type'] == 'tags':
            if orderquery['type'] == 'date':
                state.problems = [xata.query("Problema", {
                "columns": [
                    "id",
                    "nombre",
                    "tags",
                    "dificultad",
                    "score",
                    "creador.username"
                ],

                "filter": {
                    "tags": {'$includes': query['tag']}
                },
                "page": {
                    "size": 6
                },
                "sort": {
                    "xata.createdAt": orderquery['order']
                }
                })]
            elif orderquery['type'] == 'score':
                state.problems = [xata.query("Problema", {
                "columns": [
                    "id",
                    "nombre",
                    "tags",
                    "dificultad",
                    "score",
                    "creador.username"
                ],

                "filter": {
                    "tags": {'$includes': query['tag']}
                },
                "page": {
                    "size": 6
                },
                "sort": {
                    "score": orderquery['order']
                }
                })]
            elif orderquery['type'] == 'dificultad':
                state.problems = [xata.query("Problema", {
                "columns": [
                    "id",
                    "nombre",
                    "tags",
                    "dificultad",
                    "score",
                    "creador.username"
                ],

                "filter": {
                    "tags": {'$includes': query['tag']}
                },
                "page": {
                    "size": 6
                },
                "sort": {
                    "dificultad": orderquery['order']
                }
                })]

    else:
        if orderquery['type'] == 'date':
            state.problems = [xata.query("Problema", {
            "columns": [
                "id",
                "nombre",
                "tags",
                "dificultad",
                "score",
                "creador.username"
              ],
            "page": {
                "size": 6
              },
              "sort": {
                "xata.createdAt": orderquery['order']
              }
              })
            ]
        elif orderquery['type'] == 'score':
            state.problems = [xata.query("Problema", {
            "columns": [
                "id",
                "nombre",
                "tags",
                "dificultad",
                "score",
                "creador.username"
              ],
            "page": {
                "size": 6
              },
              "sort": {
                "score": orderquery['order']
              }
              })
            ]
        elif orderquery['type'] == 'dificultad':
            state.problems = [xata.query("Problema", {
            "columns": [
                "id",
                "nombre",
                "tags",
                "dificultad",
                "score",
                "creador.username"
              ],
            "page": {
                "size": 6
              },
              "sort": {
                "dificultad": orderquery['order']
              }
              })
            ]
    state.pageproblems = 0
    state.pimages = []


def switch_torender(idd):
    if 'query' not in state:
        state.query = {'Table': 'Problema', 'id': idd}
    else:
        state.query['Table'] = 'Problema'
        state.query['id'] = idd


def render_problem(problem: dict,k : int):
    COLORS = ['blue', 'yellow', 'purple', 'cyan', 'pink', 'brown', 'gray','magenta', 'teal', 'lime', 'lavender', 'turquoise', 'darkblue', 'darkgreen', 'darkred', 'lightblue', 'lightgreen', 'lightred', 'gold', 'lightgray']

    tags = [
        "Todos",
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

    emojis_tags = [
        "💊",
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




    with st.container(border=True):
        with st.spinner(f'Cargando Problema...'):
            if len(state.pimages) < k+1:
                img = asyncio.run(get_random_image())
                state.pimages.append(img)
            else:
                img = state.pimages[k]
        st.image(img, use_column_width=True)
        st.markdown(f'### {problem["nombre"]}')
        pls = []
        pls_icon = []
        if problem["dificultad"] == 1:
            pls.append(":green[Fácil]")
            pls_icon.append("🐛")
        elif problem["dificultad"] == 2:
            pls.append(":blue[Intermedio]")
            pls_icon.append("🐍")
        else:
            pls.append(":red[Difícil]")
            pls_icon.append("🐉")
        for tag in problem["tags"]:
            if tag not in tags:
                tags.append(tag)
                emojis_tags.append("💊")
            else:
                pls.append(tag)
                pls_icon.append(emojis_tags[tags.index(tag)])
        tagss = [f"{pls_icon[i]} {pls[i]}" for i in range(len(pls))]
        st.write(', '.join(tagss))
        st.markdown(f'''
        **Score:** {problem['score']}

        **Creador:** @{problem['creador']['username'] if 'creador' in problem else 'Anónimo'}

        **Fecha de Creación:** {format_date(problem['xata']['createdAt'][:10])}
        ''')
        if st.button('Ver Problema', key=f'b{k}',use_container_width=True, on_click=switch_torender, args=[problem['id']]):
            st.switch_page('pages/problem_render.py')

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




#--------------------------------- Variables de Estado ---------------------------------
if 'pageproblems' not in state:
    state.pageproblems = 0


if 'problems' not in state or state.problems is None:
    state.problems = [xata.query("Problema", {
    "columns": [
        "id",
        "nombre",
        "tags",
        "dificultad",
        "score",
        "creador.username"
    ],
    "page": {
        "size": 6
    }
})]


if 'problemquery' not in state:
    state.problemquery  = {}

if 'ptags' not in state:
    state.ptags = 'Todos'

if 'porder' not in state:
    state.porder = 'Más Recientes'

if 'porderquery' not in state:
    state.porderquery = {'type':'date','order':'desc'}

if 'pimages' not in state:
    state.pimages = []

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


#---------------------------------Navbar---------------------------------

if auth():
    #st.session_state['userinfo']
    if st.session_state.user is not None and  (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
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



    over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
    menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Inicio',
        login_name=None,
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
        first_select=10,
        )


    if menu_id == 'Inicio':
        st.switch_page('pages/app.py')

    if menu_id == 'code':
        st.switch_page('pages/code_editor.py')

    if menu_id == 'logout':
        st.session_state.auth_state = False
        st.session_state.userinfo = None
        st.session_state.user = None
        st.session_state.username = None
        cookie_manager.delete('Validado')
        st.session_state.logout = True

    if st.session_state.user is not None and  menu_id == st.session_state.user.usuario:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        st.switch_page('pages/profile_render.py')



    if st.session_state.user is not None and (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
        if menu_id == 'subid144':
            st.switch_page('pages/test_editor.py')

        if menu_id == 'doceditor':
            st.switch_page('pages/doc_editor.py')

        if menu_id == 'docshome':
            st.switch_page('pages/docs_home.py')

        if menu_id == 'subid44':
            st.switch_page('pages/problems_editor.py')
    else:
        if menu_id == 'docs':
            st.switch_page('pages/docs_home.py')
else:
    asyncio.run(show_message_error())
    st.stop()


#---------------------------------Body---------------------------------
with open('rsc/html/ProblemaHome-Banner.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)


cols0 = st.columns([0.3,0.4,0.3])
with cols0[1]:
    datasearch = st_searchbox(search_function=search_problem, placeholder="Buscar Problema")
    if datasearch is not None and datasearch != '' and not isinstance(datasearch, int):
        if 'searchbox' in state:
            del state.searchbox
        nm,idtfy = datasearch.split(',')
        st.write(nm)
        if 'query' not in state:
            state.query = {'Table': 'Problema', 'id': idtfy}
        else:
            state.query['Table'] = 'Problema'
            state.query['id'] = idtfy
        st.switch_page('pages/problem_render.py')

tags = [
    "Todos",
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

emojis_tags = [
    "💊",
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



tagss = pills('Categorías',tags, emojis_tags)

if tagss != state.ptags:
    if tagss == 'Todos':
        state.ptags = tagss
        update_problems(orderquery=state.porderquery)
        st.rerun()
    else:
        state.ptags = tagss
        update_problems({'type':'tags','tag':tagss},state.porderquery)
        st.rerun()

colls = st.columns([0.7,0.1,0.2])

colls[1].button('🔄',key='refresh',on_click=update_problems,use_container_width=True)
order = colls[2].selectbox('Ordenar',['Ordenar por',
'Más Recientes','Más Antiguos','Score ↑','Score ↓',
'Dificultad ↑','Dificultad ↓'],
index=0,placeholder='Ordenar por',label_visibility='collapsed')

if order != state.porder and order != 'Ordenar por':
    if order == 'Más Recientes':
        state.porder = order
        state.porderquery = {'type':'date','order':'desc'}
        update_problems(orderquery=state.porderquery,query=state.ptags if state.ptags != 'Todos' else None)
        st.rerun()
    elif order == 'Más Antiguos':
        state.porder = order
        state.porderquery = {'type':'date','order':'asc'}
        update_problems(orderquery=state.porderquery,query=state.ptags if state.ptags != 'Todos' else None)
        st.rerun()
    elif order == 'Score ↑':
        state.porder = order
        state.porderquery = {'type':'score','order':'asc'}
        update_problems(orderquery=state.porderquery,query=state.ptags if state.ptags != 'Todos' else None)
        st.rerun()
    elif order == 'Score ↓':
        state.porder = order
        state.porderquery = {'type':'score','order':'desc'}
        update_problems(orderquery=state.porderquery,query=state.ptags if state.ptags != 'Todos' else None)
        st.rerun()
    elif order == 'Dificultad ↑':
        state.porder = order
        state.porderquery = {'type':'dificultad','order':'asc'}
        update_problems(orderquery=state.porderquery,query=state.ptags if state.ptags != 'Todos' else None)
        st.rerun()
    elif order == 'Dificultad ↓':
        state.porder = order
        state.porderquery = {'type':'dificultad','order':'desc'}
        update_problems(orderquery=state.porderquery,query=state.ptags if state.ptags != 'Todos' else None)
        st.rerun()
elif order == 'Ordenar por':
    state.porder = order


sac.divider('',icon='hypnotize',align='center',)

if len(state.problems[state.pageproblems]['records']) == 0:
    st.warning('No hay problemas que mostrar')
problemscols = st.columns(3)
pcol = 0

for problem in range(len(state.problems[state.pageproblems]['records'])):
    if pcol == 3:
        pcol = 0
    with problemscols[pcol]:
        render_problem(state.problems[state.pageproblems]['records'][problem],problem)
    pcol += 1

pgcols = st.columns([0.8,0.1,0.1])

with pgcols[0]:
    st.caption(f'Página {state.pageproblems+1} de {len(state.problems)}')

if pgcols[1].button('<',use_container_width=True,disabled=state.pageproblems == 0):
    if state.pageproblems > 0:
        state.pageproblems -= 1
        st.rerun()

if pgcols[2].button('\>',use_container_width=True):
    if state.pageproblems < len(state.problems)-1:
        state.pageproblems += 1
        st.rerun()
    else:
        nxt = xata.next_page("Problema",state.problems[state.pageproblems],pagesize=6)
        if nxt is not None:
            state.pageproblems += 1
            state.problems.append(nxt)
            st.rerun()




st.empty()

#--------------------------------- Anuncios ---------------------------------
st.markdown('''
<h1 style="font-family: 'Roboto', sans-serif; color: #787878; font-size: 2.5em; text-align: left;padding-bottom: 0;">Anuncios
<hr style="border: 1px solid #C7C7C7; width: 50%; margin-top: 0.5em; margin-bottom: 0.5em;"/>
</h1>


''', unsafe_allow_html=True)


if "wphome" not in state:
    board = Dashboard()
    args = {}
    args["board"] = board
    w = SimpleNamespace(
        dashboard=board,
        player=Player(board, 0, 0, 8, 12, minH=6),
        card=Card(board, 8, 0, 4, 6, minW=4, minH=6),
        card2=Card(board, 4, 12, 4, 6, minW=4, minH=6),
        card3=Card(board, 0,12, 4, 6, minW=4, minH=6),
        card4=Card(board, 8, 6, 4, 6, minW=4, minH=6),
        card5=Card(board, 8, 12, 4, 6, minW=4, minH=6),
    )
    state.wphome = w
else:
    w = state.wphome
with elements("demo"):
    event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
    def handle_layout_change(updated_layout):
        # You can save the layout in a file, or do anything you want with it.
        # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
        st.write(updated_layout)
    with w.dashboard(rowHeight=57, ):
        w.player()
        w.card("Este es un Anuncio",'data:image/png;base64,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')
        w.card2('Anuncio 2','https://www.certus.edu.pe/blog/wp-content/uploads/2020/09/que-es-data-analytics-importancia-1-1200x720.jpg')
        w.card3('Anuncio 3','https://www.certus.edu.pe/blog/wp-content/uploads/2020/09/que-es-data-analytics-importancia-1-1200x720.jpg')
        w.card4('Anuncio 4','https://www.certus.edu.pe/blog/wp-content/uploads/2020/09/que-es-data-analytics-importancia-1-1200x720.jpg')
        w.card5('Anuncio 5',
        'https://www.certus.edu.pe/blog/wp-content/uploads/2020/09/que-es-data-analytics-importancia-1-1200x720.jpg',
        tags=['tag1','tag2','tag3','tag4','tag5'])
        x = w.dashboard.layout()
        #x


#---------------------------------Footer---------------------------------#
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
