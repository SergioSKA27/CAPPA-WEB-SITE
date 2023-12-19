import streamlit as st
import streamlit_antd_components as sac
from streamlit.components.v1 import  html
import hydralit_components as hc
from streamlit_searchbox import st_searchbox
from streamlit_pills import pills
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
    )






st.markdown('''
<style>
.col {
display: flex;
flex-direction: row;
width: 100%;
align-items: center;
justify-content: center;
}

.banner{
  display: flex;
  align-items: center;
  justify-content: center;
  background: #F1F1F100;
  overflow: default;
  margin-left: 0;
  margin-right: 0;
  margin-top: 0px;
}
.perspective-text {
  color: #fffae8;
  font-family: Arial;
  font-size: 58px;
  font-weight: 900;
  letter-spacing: -2px;
  text-transform: uppercase;
}

.perspective-line {
  height: 50px;
  overflow: hidden;
  position: relative;
}

.banner p {
  margin: 0;
  height: 50px;
  line-height: 50px;
  transition: all 0.5s ease-in-out;
}

.perspective-line:nth-child(odd) {
  transform: skew(60deg, -30deg) scaleY(0.667);
}

.perspective-line:nth-child(even) {
  transform: skew(0deg, -30deg) scaleY(1.337);
}

.perspective-text:hover p {
  transform: translate(0, -50px);
}

.perspective-line:nth-child(1) {
  left: 29px;
}

.perspective-line:nth-child(2) {
  left: 58px;
  background: #f07e6e;
}

.perspective-line:nth-child(3) {
  left: 87px;
  background: #84cdfa;
}

.perspective-line:nth-child(4) {
  left: 116px;
  background: #5ad1cd;
}

.perspective-line:nth-child(5) {
  left: 145px;
}
.text {
  display: flex;
  justify-content: center;
  margin-top: 10vh;
  transform: translateY(-50%);
  // margin: 250px auto;
  text-align: center;
  // border: 1px solid #000;
  transition: transform .3s ease-in-out;

  &:hover {
    transform: rotateX(35deg), translateY(-50%);
    span {
      color: #ccc;
      &:nth-child(odd) {
        transform: skewY(15deg);
        // background-color: #f00;
        // box-shadow: 0 60px 20px rgba(0,0,0,0.1);
      }
      &:nth-child(even) {
        transform: skewY(-15deg);
        background-color: #f9f9f9;
        color: #a6a6a6;
        // box-shadow: 0 60px 20px rgba(0,0,0,0.1);
      }
    }
  }

  > span {
    display: block;
    background-color: #fff;
    width: 70px;
    height: 70px;
    line-height: 70px;
    transition: transform .3s ease-in-out, color .3s ease-in-out, background-color .3s ease-in-out;
    box-shadow: 0 40px 50px rgba(0,0,0,0.1);
    &:first-child {
      border-radius: 5px 0 0 5px;
    }
  }
}
/* Media query para pantallas pequeñas */
@media only screen and (max-width: 600px) {

.col {
display: flex;
flex-direction: column;
width: 100%;

}

.text {
  display: flex;
  justify-content: center;
  margin-top: 10vh;
  transform: translateY(-50%);
  // margin: 250px auto;
  text-align: center;
  // border: 1px solid #000;
  transition: transform .3s ease-in-out;

  &:hover {
    transform: rotateX(35deg), translateY(-50%);
    span {
      color: #ccc;
      &:nth-child(odd) {
        transform: skewY(15deg);
        // background-color: #f00;
        // box-shadow: 0 60px 20px rgba(0,0,0,0.1);
      }
      &:nth-child(even) {
        transform: skewY(-15deg);
        background-color: #f9f9f9;
        color: #a6a6a6;
        // box-shadow: 0 60px 20px rgba(0,0,0,0.1);
      }
    }
  }

  > span {
    display: block;
    background-color: #fff;
    width: 50px;
    height: 50px;
    line-height: 50px;
    transition: transform .3s ease-in-out, color .3s ease-in-out, background-color .3s ease-in-out;
    box-shadow: 0 40px 50px rgba(0,0,0,0.1);
    &:first-child {
      border-radius: 5px 0 0 5px;
    }
  }
}
}
</style>
<div class="col">
    <div class="text">
      <span>P</span>
      <span>R</span>
      <span>O</span>
      <span>B</span>
      <span>L</span>
      <span>E</span>
      <span>M</span>
      <span>A</span>
      <span>S</span>
    </div>
    <div class="banner">
        <div class="perspective-text">
          <div class="perspective-line">
            <p></p>
            <p>Problemas</p>
          </div>
          <div class="perspective-line">
            <p>Problemas</p>
            <p>Avanzados</p>
          </div>
          <div class="perspective-line">
            <p>Avanzados</p>
            <p>Intermedios</p>
          </div>
          <div class="perspective-line">
            <p>Intermedios</p>
            <p>Básicos</p>
          </div>
          <div class="perspective-line">
            <p>Básicos</p>
            <p></p>
          </div>
        </div>
    </div>
</div>
''', unsafe_allow_html=True)

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
