import streamlit as st
from streamlit_searchbox import st_searchbox
from st_xatadb_connection import XataConnection
import hydralit_components as hc
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as stac
import datetime
import google.generativeai as genai

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

genai.configure(api_key=st.secrets['GEN_AI_KEY'])

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
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    padding-bottom: 0;
  }
</style>
''', unsafe_allow_html=True)

@st.cache_resource
def load_genmodel():
    return genai.GenerativeModel('gemini-pro')


def render_docs(docs:list):

    #First column
    fc1 = st.columns([0.4,0.3,0.3])
    fc2 = st.columns(3)

    if len (docs) > 0:
        with fc1[0]:
            with st.container(border=True):

                st.image(docs[0]['banner_pic']['url'],use_column_width=True)
                st.caption(f"{docs[0]['tipo']}")
                st.write(f"### {docs[0]['titulo']}")
                st.write(f"{docs[0]['shortdesc']}")
                bcols0 = st.columns([0.7,0.3])
                with bcols0[0]:
                    st.write(f"{docs[0]['autor']['nombre_completo']}")
                    st.write(f"{docs[0]['xata']['createdAt'][0:10]}")
                with bcols0[1]:
                    st.button('Leer',key=f"doc0",use_container_width=True)

    if len (docs) > 1:
        with fc1[1]:
            with st.container(border=True):
                st.image(docs[1]['banner_pic']['url'],use_column_width=True)
                st.caption(f"## {docs[1]['tipo']}")
                st.write(f"## {docs[1]['titulo']}")
                st.write(f"### {docs[1]['shortdesc']}")
                bcols1 = st.columns([0.7,0.3])
                with bcols1[0]:
                    st.write(f"{docs[1]['autor']['nombre_completo']}")
                    st.write(f"{docs[1]['xata']['createdAt'][0:10]}")
                with bcols1[1]:
                    st.button('Leer',key=f"doc1",use_container_width=True)
    if len (docs) > 2:
        with fc1[2]:
            with st.container(border=True):
                st.image(docs[2]['banner_pic']['url'],use_column_width=True)
                st.caption(f"{docs[2]['tipo']}")
                st.write(f"### {docs[2]['titulo']}")
                st.write(f"{docs[2]['shortdesc']}")
                bcols2 = st.columns([0.7,0.3])
                with bcols2[0]:
                    st.write(f"{docs[2]['autor']['nombre_completo']}")
                    st.write(f"{docs[2]['xata']['createdAt'][0:10]}")
                with bcols2[1]:
                    st.button('Leer',key=f"doc2",use_container_width=True)

    if len (docs) > 3:
        with fc2[0]:
            with st.container(border=True):
                st.image(docs[3]['banner_pic']['url'],use_column_width=True)
                st.caption(f"{docs[3]['tipo']}")
                st.write(f"### {docs[3]['titulo']}")
                st.write(f"{docs[3]['shortdesc']}")
                bcols3 = st.columns([0.7,0.3])
                with bcols3[0]:
                    st.write(f"{docs[3]['autor']['nombre_completo']}")
                    st.write(f"{docs[3]['xata']['createdAt'][0:10]}")
                with bcols3[1]:
                    st.button('Leer',key=f"doc3",use_container_width=True)

    if len (docs) > 4:
        with fc2[1]:
            with st.container(border=True):
                st.image(docs[4]['banner_pic']['url'],use_column_width=True)
                st.caption(f"{docs[4]['tipo']}")
                st.write(f"### {docs[4]['titulo']}")
                st.write(f"{docs[4]['shortdesc']}")
                bcols4 = st.columns([0.7,0.3])
                with bcols4[0]:
                    st.write(f"{docs[4]['autor']['nombre_completo']}")
                    st.write(f"{docs[4]['xata']['createdAt'][0:10]}")
                with bcols4[1]:
                    st.button('Leer',key=f"doc0",use_container_width=True)

    if len (docs) > 5:
        with fc2[2]:
            with st.container(border=True):
                st.image(docs[5]['banner_pic']['url'],use_column_width=True)
                st.caption(f"{docs[5]['tipo']}")
                st.write(f"## {docs[5]['titulo']}")
                st.write(f"{docs[5]['shortdesc']}")
                st.write(f"{docs[5]['autor']['nombre_completo']}")
                st.write(f"{docs[5]['xata']['createdAt'][0:10]}")

def render_daylycard(title, body, day, month):
    meses = {'January':'Enero','February':'Febrero','March':'Marzo','April':'Abril','May':'Mayo','June':'Junio','July':'Julio','August':'Agosto','September':'Septiembre','October':'Octubre','November':'Noviembre','December':'Diciembre'}
    st.markdown('''
<style>
@import url(https://fonts.googleapis.com/css?family=Roboto);
/* The card */
.cardtwo {
  position: relative;
  height: 450px;
  width: 900px;
  margin: 200px auto;
  background-color: #FFF;
  -webkit-box-shadow: 10px 10px 93px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 10px 10px 93px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 10px 10px 93px 0px rgba(0, 0, 0, 0.75);
}
/* Image on the left side */
.thumbnail {
  float: left;
  position: relative;
  left: 30px;
  top: -30px;
  height: 320px;
  width: 530px;
  -webkit-box-shadow: 10px 10px 60px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 10px 10px 60px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 10px 10px 60px 0px rgba(0, 0, 0, 0.75);
  overflow: hidden;
}
/*object-fit: cover;*/
/*object-position: center;*/
img.left {
  position: absolute;
  left: 50%;
  top: 50%;
  height: auto;
  width: 100%;
  -webkit-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}
/* Right side of the card */
.right {
  margin-left: 590px;
  margin-right: 20px;
}
.cardtwo h1 {
  padding-top: 15px;
  font-size: 1.3rem;
  color: #4B4B4B;
}
.author {
  background-color: #9ECAFF;
  height: 30px;
  width: 110px;
  border-radius: 20px;
}
.author h2 {
    padding-top: 5px;
}
.author > img {
  padding-top: 5px;
  margin-left: 10px;
  float: left;
  height: 20px;
  width: 20px;
  border-radius: 50%;
}
.right h2 {
  padding-top: 8px;
  margin-right: 6px;
  text-align: right;
  font-size: 0.8rem;
}
.separator {
  margin-top: 10px;
  border: 1px solid #C3C3C3;
}
.cardtwo p {
  text-align: justify;
  padding-top: 10px;
  font-size: 0.65rem;
  line-height: 150%;
  color: #4B4B4B;
}
/* DATE of release*/
.right h5 {
  position: absolute;
  left: 30px;
  bottom: 0px;
  font-size: 6rem;
  color: #C3C3C3;
  top: 300px;
}
.right h6 {
  position: absolute;
  left: 30px;
  bottom: 0px;
  font-size: 2rem;
  color: #C3C3C3;
  bottom: -10px;
}
/* Those futur buttons */
.right ul {
  margin-left: 250px;
}
.right li {
  display: inline;
  list-style: none;
  padding-right: 40px;
  color: #7B7B7B;
}
/* Floating action button */
.fab {
  position: absolute;
  display: flex;
  justify-content: center;
  right: 50px;
  box-sizing: border-box;
  padding-top: 18px;
  background-color: #1875D0;
  width: 80px;
  height: 80px;
  color: white;
  text-align: center;
  border-radius: 50%;
  -webkit-box-shadow: 10px 10px 50px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 10px 10px 50px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 10px 10px 50px 0px rgba(0, 0, 0, 0.75);
  align-items: center;
}
</style>
''', unsafe_allow_html=True)

    #1440x900
    st.markdown(f'''
<div class="cardtwo">
    <div class="thumbnail">
        <img class="left" src="https://source.unsplash.com/1440x900/?code">
    </div>
    <div class="right">
        <h1>{title}</h1>
        <div class="separator"></div>
        <p>{body}</p>
        <h5>{day}</h5>
        <h6>{meses[month]}</h6>
    </div>
    <div class="fab"><img src="https://cdn-icons-png.flaticon.com/128/1565/1565867.png" width="60"></div>
</div>

''', unsafe_allow_html=True)

def render_recentdocs(docs:list):
    st.markdown('''
<style>
@import url("https://fonts.googleapis.com/css2?family=Quicksand:wght@300..700&display=swap");
.containercard {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 1300px;
  margin-block: 2rem;
  gap: 2rem;
}

img {
  max-width: 100%;
  display: block;
  object-fit: cover;
}

.card {
  display: flex;
  flex-direction: column;
  width: clamp(20rem, calc(20rem + 2vw), 22rem);
  overflow: hidden;
  box-shadow: 0 .1rem 1rem rgba(0, 0, 0, 0.1);
  border-radius: 1em;
  background: #ECE9E6;
background: linear-gradient(to right, #FFFFFF, #ECE9E6);

}
.card h4 {
  margin-block: 0.5rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  padding: 1rem 1rem 0 1rem;
}
.card p {
    margin-block: 0.5rem;
    font-size: 1rem;
    font-weight: 400;
    color: #333;
    padding: 0 1rem 1rem 1rem;
    }
.card__footer {
    padding: 1rem 1rem 0 1rem;
}
.card__footer h5 {
    padding-bottom:0;
    }
.tag {
    padding: 1rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: #333;
    text-transform: uppercase;
    letter-spacing: 0.1rem;
    }
</style>
''', unsafe_allow_html=True)

    typedoc = 'Articulo'
    autor = 'Jhon Doe'
    fecha = datetime.date.today().strftime("%B %d, %Y")
    titulo = 'Python para principiantes'
    shortdesc = 'Aprende a programar en python desde cero.'
    avatar = 'https://i.pravatar.cc/40?img=1'

    typedoc1 = 'Articulo'
    autor1 = 'Mary Doe'
    fecha1 = datetime.date.today().strftime("%B %d, %Y")
    titulo1 = 'Python para Intermedios'
    shortdesc1 = 'Aprende conceptos intermedios de programacion en python.'
    avatar1 = 'https://i.pravatar.cc/40?img=2'

    typedoc2 = 'Articulo'
    autor2 = 'Jhon Doe'
    fecha2 = datetime.date.today().strftime("%B %d, %Y")
    titulo2 = 'Python para principiantes'
    shortdesc2 = 'Aprende a programar en python desde cero'
    avatar2 = 'https://i.pravatar.cc/40?img=3'

    if len (docs) > 0:
        typedoc = docs[0]['tipo']
        autor = docs[0]['autor']['nombre_completo']
        fecha = docs[0]['xata']['createdAt'][0:10]
        if len(docs[0]['titulo']) > 20:
            titulo = docs[0]['titulo'][0:20]+'...'
        else:
            titulo = docs[0]['titulo']
        if len(docs[0]['shortdesc']) > 100:
            shortdesc = docs[0]['shortdesc'][0:100]+'...'
        else:
            shortdesc = docs[0]['shortdesc']

        if 'avatar' in docs[0]['autor']:
            avatar = docs[0]['autor']['avatar']['url']


    if len (docs) > 1:
        typedoc1 = docs[1]['tipo']
        autor1 = docs[1]['autor']['nombre_completo']
        fecha1 = docs[1]['xata']['createdAt'][0:10]
        if len(docs[1]['titulo']) > 20:
            titulo1 = docs[1]['titulo'][0:20]+'...'
        else:
            titulo1 = docs[1]['titulo']
        if len(docs[1]['shortdesc']) > 100:
            shortdesc1 = docs[1]['shortdesc'][0:100]+'...'
        else:
            shortdesc1 = docs[1]['shortdesc']

        if 'avatar' in docs[1]['autor']:
            avatar1 = docs[1]['autor']['avatar']['url']


    if len (docs) > 2:
        typedoc2 = docs[2]['tipo']
        autor2 = docs[2]['autor']['nombre_completo']
        fecha2 = docs[2]['xata']['createdAt'][0:10]
        if len(docs[2]['titulo']) > 20:
            titulo2 = docs[2]['titulo'][0:20]+'...'
        else:
            titulo2 = docs[2]['titulo']
        if len(docs[2]['shortdesc']) > 100:
            shortdesc2 = docs[2]['shortdesc'][0:100]+'...'
        else:
            shortdesc2 = docs[2]['shortdesc']

        if 'avatar' in docs[2]['autor']:
            avatar2 = docs[2]['autor']['avatar']['url']


    st.markdown(f'''
<div class="containercard">
  <div class="card">
    <div class="card__header">
      <img src="https://source.unsplash.com/600x400/?computer" alt="card__image" class="card__image" width="600">
    </div>
    <div class="card__body">
      <span class="tag">{typedoc}</span>
      <h4>{titulo}</h4>
      <p>{shortdesc}</p>
    </div>
    <div class="card__footer">
      <div class="user">
        <img src="{avatar}" alt="user__image" class="user__image" width="40">
        <div class="user__info">
          <h5>{autor}</h5>
          <small>{fecha}</small>
        </div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card__header">
      <img src="https://source.unsplash.com/600x400/?code" alt="card__image" class="card__image" width="600">
    </div>
    <div class="card__body">
      <span class="tag">{typedoc1}</span>
      <h4>{titulo1}</h4>
      <p> {shortdesc1}</p>
    </div>
    <div class="card__footer">
      <div class="user">
        <img src="{avatar1}" alt="user__image" class="user__image" width="40">
        <div class="user__info">
          <h5>{autor1}</h5>
          <small>{fecha1}</small>
        </div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card__header">
      <img src="https://source.unsplash.com/600x400/?programming,python" alt="card__image" class="card__image" width="600">
    </div>
    <div class="card__body">
      <span class="tag">{typedoc2}</span>
      <h4>{titulo2}</h4>
      <p>{shortdesc2}</p>
    </div>
    <div class="card__footer">
      <div class="user">
        <img src="{avatar2}" alt="user__image" class="user__image" width="40">
        <div class="user__info">
          <h5>{autor2}</h5>
          <small>{fecha2}</small>
        </div>
      </div>
    </div>
  </div>
</div>
''', unsafe_allow_html=True)




def search_doc(s: str):
    return []


def update_pagedocs():
    st.session_state.docspage = [xata.query("Documento", {
    "columns": ["autor", "titulo", "banner_pic.url",'tags','tipo','shortdesc','xata.createdAt',],
    "page": {
        "size": 6
    }}
    )]
    st.rerun()

def update_daylycard():
    model = load_genmodel()
    title = model.generate_content('Dame un solo titulo para un articulo de blog sobre algun tema de programacion en python en texto plano sin nada adicional')
    bdy = model.generate_content(f'Dame un articulo de blog sobre {title.text} de no mas de 50 palabras en texto plano solo el cuerpo del articulo sin el titulo')
    st.session_state.daylycard = {'title':title.text,'body':bdy.text,'day':datetime.date.today().day,'month':datetime.date.today().strftime("%B")}
    st.rerun()


if 'docspage' not in st.session_state:
    st.session_state.docspage = [xata.query("Documento", {
    "columns": ["autor", "titulo", "banner_pic.url",'tags','tipo','shortdesc','xata.createdAt'],
    "page": {
        "size": 6
    }}
    )]


if 'daylycard' not in st.session_state:
    model = load_genmodel()
    title = model.generate_content('Dame un solo titulo para un articulo de blog sobre algun tema de programacion en texto plano sin nada adicional')
    bdy = model.generate_content(f'Dame un articulo de blog sobre {title.text} de no mas de 50 palabras en texto plano solo el cuerpo del articulo sin el titulo')
    st.session_state.daylycard = {'title':title.text,'body':bdy.text,'day':datetime.date.today().day,'month':datetime.date.today().strftime("%B")}
##---------------------------------Navbar---------------------------------
if 'auth_state' not  in st.session_state:
    menu_data = [
    {'icon': "far fa-copy", 'label':"Docs",'ttip':"Documentación de la Plataforma"},
    {'id':'About','icon':"bi bi-question-circle",'label':"FAQ",'ttip':"Preguntas Frecuentes"},
    {'id':'contact','icon':"bi bi-envelope",'label':"Contacto",'ttip':"Contáctanos"},
    ]
    logname = 'Iniciar Sesión'
else:
    if st.session_state['userinfo']['rol'] == "Administrador" or st.session_state['userinfo']['rol'] == "Profesor" or st.session_state['userinfo']['rol'] == "Moderador":
        #Navbar para administradores, Profesores y Moderadores
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':' subid11','icon': "bi bi-flower1", 'label':"Basicos"},
            {'id':'subid22','icon': "fa fa-paperclip", 'label':"Intermedios"},
            {'id':'subid33','icon': "bi bi-emoji-dizzy", 'label':"Avanzados"},
            {'id':'subid44','icon': "bi bi-gear", 'label':"Editor"}
        ]},
        {'id':'contest','icon': "bi bi-trophy", 'label':"Concursos"},
        {'icon': "bi bi-graph-up", 'label':"Analisis de Datos",'ttip':"Herramientas de Analisis de Datos"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Docs",'ttip':"Articulos e Información",
        'submenu':[
            {'id':'subid55','icon': "bi bi-gear", 'label':"Editor" }]
        },
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests", 'submenu':[
            {'label':"Todos", 'icon': "bi bi-search",'id':'alltests'},
            {'label':"Basicos 1", 'icon': "🐛"},
            {'icon':'🐍','label':"Intermedios"},
            {'icon':'🐉','label':"Avanzados",},
            {'id':'subid144','icon': "bi bi-gear", 'label':"Editor" }]},
        {'id':'logout','icon': "bi bi-door-open", 'label':"Logout"},#no tooltip message
    ]
    else:
    #Navbar para Estudiantes
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':' subid11','icon': "bi bi-flower1", 'label':"Basicos"},
            {'id':'subid22','icon': "fa fa-paperclip", 'label':"Intermedios"},
            {'id':'subid33','icon': "bi bi-emoji-dizzy", 'label':"Avanzados"},
        ]},
        {'id':'contest','icon': "bi bi-trophy", 'label':"Concursos"},
        {'icon': "bi bi-graph-up", 'label':"Analisis de Datos",'ttip':"Herramientas de Analisis de Datos"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Docs",'ttip':"Articulos e Información"},
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests", 'submenu':[
            {'label':"Todos", 'icon': "bi bi-search",'label':'alltests'},
            {'label':"Basicos", 'icon': "🐛"},
            {'icon':'🐍','label':"Intermedios"},
            {'icon':'🐉','label':"Avanzados",}]},
        {'id':'logout','icon': "bi bi-door-open", 'label':"Logout"},#no tooltip message
    ]
    logname = st.session_state['userinfo']['username']


over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name="Inicio",
    login_name=st.session_state['userinfo']['username'],
    hide_streamlit_markers=False,  # will show the st hamburger as well as the navbar now!
    sticky_nav=True,  # at the top or not
    sticky_mode="sticky",  # jumpy or not-jumpy, but sticky or pinned
    first_select=40,
)


if menu_id == 'Inicio':
  switch_page('Main')

if menu_id == 'subid00':
    switch_page('problems_home')

if menu_id == 'subid44':
    switch_page('problems_editor')

if menu_id == 'code':
    switch_page('code_editor')

if menu_id == 'subid144':
    switch_page('test_editor')

if menu_id == 'logout':
    st.session_state.pop('auth_state')
    st.session_state.pop('userinfo')
    st.session_state.pop('username')
    switch_page('login')

if 'userinfo' in st.session_state:
    if menu_id == st.session_state['userinfo']['username']:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
        switch_page('profile_render')



#------------------------------------------BODY------------------------------------------------------------



headcols = st.columns([0.6,0.4])
with headcols[0]:
    with open('rsc/html/docs_home_header.html') as f:
        st.markdown(f.read(), unsafe_allow_html=True)




headcols[1].markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@500;900&display=swap');
.blogheader {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    }
.blogheader h1 {
    font-family: 'Poppins', sans-serif;
    font-size: 8rem;
    color: #4B4B4B;
    font-weight: 900;
    text-align: center;
    padding-top: 10vh;
    shadow-color: #000000;
    text-shadow: 4px 4px 8px #000000;
    }
@keyframes book-bounce {
  0% {
    transform: translateY(0);
    -webkit-transform: translateY(0);
    -moz-transform: translateY(0);
    -ms-transform: translateY(0);
    -o-transform: translateY(0);
}
  40% {
    transform: translateY(-10px);
  }
  80% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(0);
  }
}
@keyframes shelf-lift {
  0% {
    transform: translateY(0) rotate(0);
  }
  20% {
    transform: translateY(-4px) rotate(10deg);
  }
  40% {
    transform: translateY(-4px) rotate(0);
  }
  40% {
    transform: translateY(-4px) rotate(-10deg);
  }
  80% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(0);
  }
}
.book-shelf:hover {
  cursor: pointer;
}
.book-shelf:hover .book-shelf__book {
  animation: book-bounce 0.4s ease;
  animation-iteration-count: 1;
}
.book-shelf:hover .book-shelf__book--two {
  animation-delay: 0.04s;
}
.book-shelf:hover .book-shelf__book--three {
  animation-delay: 0.08s;
}
.book-shelf:hover .book-shelf__shelf {
  animation: shelf-lift 0.4s ease;
  animation-iteration-count: 1;
  transform-origin: 50% 50%;
}
.book-shelf {
    position: relative;
    padding-top: 10px;
}
</style>
<div class="blogheader">
    <h1>BLOG</h1>
    <svg class="book-shelf" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid" viewBox="0 0 84 94" height="94" width="84">
        <path fill="none" d="M37.612 92.805L4.487 73.71c-2.75-1.587-4.45-4.52-4.45-7.687L.008 27.877c-.003-3.154 1.676-6.063 4.405-7.634L37.558 1.167c2.73-1.57 6.096-1.566 8.835.013l33.124 19.096c2.75 1.586 4.45 4.518 4.45 7.686l.028 38.146c.002 3.154-1.677 6.063-4.406 7.634L46.445 92.818c-2.73 1.57-6.096 1.566-8.834-.013z"/>
        <g class="book-shelf__book book-shelf__book--one" fill-rule="evenodd">
          <path fill="#5199fc" d="M31 29h4c1.105 0 2 .895 2 2v29c0 1.105-.895 2-2 2h-4c-1.105 0-2-.895-2-2V31c0-1.105.895-2 2-2z"/>
          <path fill="#afd7fb" d="M34 36h-2c-.552 0-1-.448-1-1s.448-1 1-1h2c.552 0 1 .448 1 1s-.448 1-1 1zm-2 1h2c.552 0 1 .448 1 1s-.448 1-1 1h-2c-.552 0-1-.448-1-1s.448-1 1-1z"/>
        </g>
        <g class="book-shelf__book book-shelf__book--two" fill-rule="evenodd">
          <path fill="#ff9868" d="M39 34h6c1.105 0 2 .895 2 2v24c0 1.105-.895 2-2 2h-6c-1.105 0-2-.895-2-2V36c0-1.105.895-2 2-2z"/>
          <path fill="#d06061" d="M42 38c1.105 0 2 .895 2 2s-.895 2-2 2-2-.895-2-2 .895-2 2-2z"/>
        </g>
        <g class="book-shelf__book book-shelf__book--three" fill-rule="evenodd">
          <path fill="#ff5068" d="M49 32h2c1.105 0 2 .86 2 1.92v25.906c0 1.06-.895 1.92-2 1.92h-2c-1.105 0-2-.86-2-1.92V33.92c0-1.06.895-1.92 2-1.92z"/>
          <path fill="#d93368" d="M50 35c.552 0 1 .448 1 1v2c0 .552-.448 1-1 1s-1-.448-1-1v-2c0-.552.448-1 1-1z"/>
        </g>
        <g fill-rule="evenodd">
          <path class="book-shelf__shelf" fill="#ae8280" d="M21 60h40c1.105 0 2 .895 2 2s-.895 2-2 2H21c-1.105 0-2-.895-2-2s.895-2 2-2z"/>
          <path fill="#855f6d" d="M51.5 67c-.828 0-1.5-.672-1.5-1.5V64h3v1.5c0 .828-.672 1.5-1.5 1.5zm-21 0c-.828 0-1.5-.672-1.5-1.5V64h3v1.5c0 .828-.672 1.5-1.5 1.5z"/>
        </g>
    </svg>
</div>

''', unsafe_allow_html=True)

st.divider()

cols0 = st.columns([0.3,0.4,0.3])
with cols0[1]:
    st_searchbox(search_function=search_doc, placeholder="Buscar en el blog",label="",key="searchbox-blog")

if st.button('Actualizar'):
    update_pagedocs()
#st.write(st.session_state.docspage)



render_docs(st.session_state.docspage[0]['records'])
#------------------------------------------CARDS------------------------------------------------------------
#today = datetime.date.today()

render_recentdocs(st.session_state.docspage[0]['records'])


#st.session_state.daylycard
render_daylycard(st.session_state.daylycard['title'], st.session_state.daylycard['body'], st.session_state.daylycard['day'], st.session_state.daylycard['month'])

if st.button('Nuevo'):
    update_daylycard()



#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
