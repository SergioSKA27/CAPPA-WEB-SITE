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
    try:

        result = await asyncio.to_thread(requests.get, 'https://source.unsplash.com/random/600x400?programming,python,code',timeout=1)
        return result.content
    except:
        return 'https://source.unsplash.com/random/600x400?programming,python,code'

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
            img = asyncio.run(get_random_image())

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

        **Creador:** @{problem['creador']['username'] if 'creador' in problem and 'username' in problem['creador'] else 'Anónimo'}

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
    state.porder = 'Ordenar por'

if 'porderquery' not in state:
    state.porderquery = {'type':'date','order':'desc'}



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

    if  menu_id == 'courses':
        st.switch_page('pages/CoursesHome.py')

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

colls[1].button('🔄',key='refresh',on_click=update_problems,use_container_width=True,kwargs={'orderquery': state.porderquery})
order = colls[2].selectbox('Ordenar',['Ordenar por',
'Más Recientes','Más Antiguos','Score ↑','Score ↓',
'Dificultad ↑','Dificultad ↓'],
index=0,placeholder='Ordenar por',label_visibility='collapsed')

if order != state.porder and order != 'Ordenar por':
    if order == 'Más Recientes':
        state.porder = order
        state.porderquery = {'type':'date','order':'desc'}
        update_problems(orderquery=state.porderquery,query={'type':'tags','tag':state.ptags} if state.ptags != 'Todos' else None)
        st.rerun()
    elif order == 'Más Antiguos':
        state.porder = order
        state.porderquery = {'type':'date','order':'asc'}
        update_problems(orderquery=state.porderquery,query={'type':'tags','tag':state.ptags} if state.ptags != 'Todos' else None)
        st.rerun()
    elif order == 'Score ↑':
        state.porder = order
        state.porderquery = {'type':'score','order':'asc'}
        update_problems(orderquery=state.porderquery,query={'type':'tags','tag':state.ptags} if state.ptags != 'Todos' else None)
        st.rerun()
    elif order == 'Score ↓':
        state.porder = order
        state.porderquery = {'type':'score','order':'desc'}
        update_problems(orderquery=state.porderquery,query={'type':'tags','tag':state.ptags} if state.ptags != 'Todos' else None)
        st.rerun()
    elif order == 'Dificultad ↑':
        state.porder = order
        state.porderquery = {'type':'dificultad','order':'asc'}
        update_problems(orderquery=state.porderquery,query={'type':'tags','tag':state.ptags} if state.ptags != 'Todos' else None)
        st.rerun()
    elif order == 'Dificultad ↓':
        state.porder = order
        state.porderquery = {'type':'dificultad','order':'desc'}
        update_problems(orderquery=state.porderquery,query={'type':'tags','tag':state.ptags} if state.ptags != 'Todos' else None)
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

st.divider()
pgcols = st.columns([0.8,0.1,0.1])
st.divider()
with pgcols[0]:
    st.caption(f'Página {state.pageproblems+1} de {len(state.problems)}')

if pgcols[1].button('<',use_container_width=True,disabled=state.pageproblems == 0):
    if state.pageproblems > 0 and len(state.problems) > 1:
        state.pageproblems -= 1

if pgcols[2].button('\>',use_container_width=True):
    if state.pageproblems < len(state.problems)-1:
        state.pageproblems += 1
    else:
        nxt = xata.next_page("Problema",state.problems[state.pageproblems],pagesize=6)
        if nxt is not None:
            state.pageproblems += 1
            state.problems.append(nxt)






#---------------------------------Footer---------------------------------#
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
