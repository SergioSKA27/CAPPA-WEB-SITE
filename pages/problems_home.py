import streamlit as st
import streamlit_antd_components as sac
from streamlit.components.v1 import  html
import hydralit_components as hc
from streamlit_searchbox import st_searchbox
from streamlit_pills import pills
from streamlit_extras.switch_page_button import switch_page
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from modules import Dashboard,Editor, Card, DataGrid, Radar, Pie, Player,Bar
import asyncio
import concurrent.futures

st.set_page_config(layout="wide", page_title="Problemas",initial_sidebar_state="collapsed", page_icon="rsc/Logos/LOGO_CAPPA.jpg")

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



def search_problem(s: str):
    return []


def handle_cardClick():
    state.cardclicked = True
    switch_page('Main')


if 'cardclicked' not in state:
    state.cardclicked = False
elif state.cardclicked:
    del state['cardclicked']
    switch_page('Main')


#---------------------------------
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
        login_name='User',
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
        first_select=10,
    )


if menu_id == 'Inicio':
  switch_page('Main')

if menu_id == 'logout':
    switch_page('Login')

#---------------------------------
#Main

with open('rsc/html/ProblemaHome-Banner.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)


cols0 = st.columns([0.3,0.4,0.3])
with cols0[1]:
    st_searchbox(search_function=search_problem, placeholder="Buscar Problema", )

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

sac.divider('',icon='hypnotize',align='center',)

cols1 = st.columns([0.3,0.7])

with cols1[0]:
  st.image('https://images.squarespace-cdn.com/content/v1/574faff6f8baf35e5da43485/1553914921320-JL7TJLMKYJ0H1JUXG5CY/Data-Inspect.gif',
  use_column_width=True)

with cols1[1]:
  st.markdown('### Problema 1')
  sac.tags(
  [
    sac.Tag("Fácil", color="green",icon="snow"),
    sac.Tag("Árboles", color="blue",bordered=True),
    sac.Tag("Divide y Vencerás", color="red",bordered=True),
    sac.Tag("Programación Dinámica", color="orange",bordered=True)

  ],align="start",key='t1'
  )
  st.markdown('''
  **Descripción:**
  Dado un árbol binario, encuentre el número de nodos en el árbol.
  ''')
  renderp = st.button('Ver Problema',key='b1')

st.divider()

cols2 = st.columns([0.3,0.7])

with cols2[0]:
  st.image('https://images.squarespace-cdn.com/content/v1/574faff6f8baf35e5da43485/1553914921320-JL7TJLMKYJ0H1JUXG5CY/Data-Inspect.gif',
  use_column_width=True)

with cols2[1]:
  st.markdown('### Problema 1')
  sac.tags(
  [
    sac.Tag("Fácil", color="green",icon="snow"),
    sac.Tag("Árboles", color="blue",bordered=True),
    sac.Tag("Divide y Vencerás", color="red",bordered=True),

  ],align="start",key='t2'
  )
  st.markdown('''
  **Descripción:**
  Dado un árbol binario, encuentre el número de nodos en el árbol.
  ''')
  renderp = st.button('Ver Problema',key='b2')

st.divider()
cols3 = st.columns([0.3,0.7])

with cols3[0]:
  st.image('https://images.squarespace-cdn.com/content/v1/574faff6f8baf35e5da43485/1553914921320-JL7TJLMKYJ0H1JUXG5CY/Data-Inspect.gif',
  use_column_width=True)

with cols3[1]:
  st.markdown('### Problema 1')
  sac.tags(
  [
    sac.Tag("Fácil", color="green",icon="snow"),
    sac.Tag("Árboles", color="blue",bordered=True),
    sac.Tag("Divide y Vencerás", color="red",bordered=True),
    sac.Tag("Programación Dinámica", color="orange",bordered=True)

  ],align="start",key='t3'
  )
  st.markdown('''
  **Descripción:**
  Dado un árbol binario, encuentre el número de nodos en el árbol.
  ''')
  renderp = st.button('Ver Problema',key='b3')

st.divider()
cols4 = st.columns([0.3,0.7])

with cols4[0]:
  st.image('https://images.squarespace-cdn.com/content/v1/574faff6f8baf35e5da43485/1553914921320-JL7TJLMKYJ0H1JUXG5CY/Data-Inspect.gif',
  use_column_width=True)

with cols4[1]:
  st.markdown('### Problema 1')
  sac.tags(
  [
    sac.Tag("Fácil", color="green",icon="snow"),
    sac.Tag("Árboles", color="blue",bordered=True),
    sac.Tag("Divide y Vencerás", color="red",bordered=True),
    sac.Tag("Programación Dinámica", color="orange",bordered=True)

  ],align="start",key='t4'
  )
  st.markdown('''
  **Descripción:**
  Dado un árbol binario, encuentre el número de nodos en el árbol.
  ''')
  renderp = st.button('Ver Problema',key='b4')

st.divider()
cols5 = st.columns([0.3,0.7])

with cols5[0]:
  st.image('https://images.squarespace-cdn.com/content/v1/574faff6f8baf35e5da43485/1553914921320-JL7TJLMKYJ0H1JUXG5CY/Data-Inspect.gif',
  use_column_width=True)

with cols5[1]:
  st.markdown('### Problema 1')
  sac.tags(
  [
    sac.Tag("Fácil", color="green",icon="snow"),
    sac.Tag("Árboles", color="blue",bordered=True),
    sac.Tag("Divide y Vencerás", color="red",bordered=True),
    sac.Tag("Programación Dinámica", color="orange",bordered=True)

  ],align="start",key='t5'
  )
  st.markdown('''
  **Descripción:**
  Dado un árbol binario, encuentre el número de nodos en el árbol.
  ''')
  renderp = st.button('Ver Problema',key='b5')

st.divider()

sac.pagination(total=100,page_size=5,align='center',jump=True,show_total=True)

if "w" not in state:
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
    state.w = w
else:
    w = state.w
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
        tags=['tag1','tag2','tag3','tag4','tag5']
        ,button='Ver mas')
        x = w.dashboard.layout()
        #x

if state.cardclicked:
  switch_page('Main')

