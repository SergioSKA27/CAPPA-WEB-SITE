import time
import streamlit as st
from st_xatadb_connection import XataConnection
import hydralit_components as hc
import streamlit_antd_components as sac
import datetime
import google.generativeai as genai
import markdown
import re
from streamlit_elements import media, elements,mui
import extra_streamlit_components as stx

from Clases import Usuario,Autenticador

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
    padding-left: 0.75rem;
    padding-right: 0.75rem;
    padding-bottom: 0;
  }
</style>
''', unsafe_allow_html=True)


def format_date(date):
    dt = date.split('-')
    meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre', 'Octubre','Noviembre','Diciembre']

    return f'{dt[2]} de {meses[int(dt[1])-1]} del {dt[0]}'


def split_parts(doc):
    parts = doc.split('```')
    return parts

def render_part(part, graphs, videos):
    if part is None:
        return

    LANGUAGES  = ['python','javascript','java','c','c++','c#','html','css','sql','php','ruby','go','kotlin','swift','dart','r','rust','typescript','shell','powershell','perl','lua','scala','groovy','haskell','f#','elixir','clojure','racket','julia','nim','crystal','cobol','fortran','ada','lisp','scheme','prolog','erlang','ocaml','reason','coffeescript','v','verilog','vhdl','systemverilog','logos','dot','video']

    if 'video' in part and any([v in part for v in videos]):
        p1 = part.split('\n')
        with elements(p1[1]):
            with mui.Box(sx={'display':'flex','justify-content':'center', 'align-items':'center'}):
                media.Player(url=p1[1],controls=False)
    elif 'dot' in part and any([g in part for g in graphs]):
        gcol = st.columns([0.3,0.4,0.3])
        p1 = part.split('\n')
        with gcol[1]:
            st.graphviz_chart(p1[1])
    else:
        split = part.split('\n')

        if split[0] in LANGUAGES:
            st.code('\n'.join(split[1:]),language=split[0])
        else:
            st.markdown(part,unsafe_allow_html=True)




if 'query' not in st.session_state:
    st.switch_page('pages/docs_home.py')

@st.cache_data
def extrac_videolinks(doc):
    return re.findall(r'```video\n(.*?)```',doc,re.DOTALL)
@st.cache_data
def extrac_code(doc):
    return re.findall(r'```[a-zA-Z]*\n(.*?)```',doc,re.DOTALL)

@st.cache_data
def extrac_dot(doc):
    return re.findall(r'```dot\n(.*?)```',doc,re.DOTALL)

def get_manager():
    return stx.CookieManager()



if st.session_state.query['Table'] ==  'Documento':
    if 'doctorender' not in st.session_state:
        st.session_state.doctorender = xata.get('Documento',st.session_state.query['id'],columns=[
        'autor.nombre_completo',
        "titulo",
        "tags",
        "content",
        "tipo",
        "xata.createdAt"
    ])
    else:
        #if st.session_state.doctorender['id'] != st.session_state.query['id']:
        st.session_state.doctorender = xata.get('Documento',st.session_state.query['id'],columns=[
        'autor.nombre_completo',
        "titulo",
        "tags",
        "content",
        "tipo",
        "xata.createdAt"
    ])


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
    #st.session_state['userinfo']
    if st.session_state.user.is_admin() or st.session_state.user.is_teacher():
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
        {'label':"Articulo",'icon':"bi bi-file-earmark-richtext",'id':'renderdoc'},
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
    else:
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",'id':'Problemas'},
        {'id':'courses','icon': "bi bi-journal-bookmark", 'label':"Cursos",'ttip':"Cursos de Programación y Ciencia de Datos en CAPPA"},
        {'id':'Blog','icon': "bi bi-file-earmark-richtext", 'label':"Blog",'ttip':"Articulos e Información"},
        {'label':"Articulo",'icon':"bi bi-file-earmark-richtext",'id':'renderdoc'},
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests"},
        {'id':st.session_state.user.usuario,'icon': "bi bi-person", 'label':st.session_state.user.usuario,
        'submenu':[
            {'label':"Perfil", 'icon': "bi bi-person",'id':st.session_state.user.usuario},
            {"id": "pcourses", "icon": "bi bi-journal-bookmark", "label": "Mis Cursos"},

            {"id": "logout", "icon": "bi bi-door-open", "label": "Cerrar Sesión"},
        ]}
    ]
    fs = 40
    logname = None
else:
    menu_data = [
    {'icon': "far fa-copy", 'label':"Blog",'ttip':"Articulos e Información",'id':'Blog'},
    {'label':"Articulo",'icon':"bi bi-file-earmark-richtext",'id':'renderdoc'},
    {'id':'About','icon':"bi bi-question-circle",'label':"FAQ",'ttip':"Preguntas Frecuentes"},
    {'id':'contact','icon':"bi bi-envelope",'label':"Contacto",'ttip':"Contáctanos"},
    ]
    fs = 20



over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name="Inicio",
    login_name='Iniciar Sesión' if not auth() else None,
    hide_streamlit_markers=False,  # will show the st hamburger as well as the navbar now!
    sticky_nav=True,  # at the top or not
    sticky_mode="sticky",  # jumpy or not-jumpy, but sticky or pinned
    first_select=fs,
)

if menu_id == "Inicio":
    st.switch_page("pages/app.py")

if menu_id == 'Iniciar Sesión':
    st.switch_page('pages/login.py')

if menu_id == 'code':
    st.switch_page('pages/code_editor.py')

if menu_id == 'logout':
    st.session_state.auth_state = False
    st.session_state.userinfo = None
    st.session_state.user = None
    st.session_state.username = None
    cookie_manager.delete('Validado')
    st.session_state.logout = True


if auth() :
    if st.session_state.user.is_admin() or st.session_state.user.is_teacher():
        if menu_id == 'subid00':
            st.switch_page('pages/problems_home.py')
        if menu_id == 'subid44':
            st.switch_page('pages/problems_editor.py')

        if menu_id == 'doceditor':
            st.switch_page('pages/doc_editor.py')

        if menu_id == 'docshome':
            st.switch_page('pages/docs_home.py')

        if menu_id == 'subid144':
            st.switch_page('pages/test_editor.py')

    else:
        if menu_id == 'Problemas':
            st.switch_page('pages/problems_home.py')
        if menu_id == 'Blog':
            st.switch_page('pages/docs_home.py')

    if menu_id == st.session_state.user.usuario:
            if 'query' not in st.session_state:
                st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
            else:
                st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
            st.switch_page('pages/profile_render.py')




#---------------------------------Body---------------------------------
colors = ['blue','red','green','purple','orange','cyan','magenta','geekblue','gold','lime','volcano','yellow','pink','grey','darkblue','darkred','darkgreen','darkpurple','darkorange','darkcyan','darkmagenta','darkgeekblue','darkgold','darklime','darkvolcano','darkyellow','darkpink','darkgrey','lightblue','lightred','lightgreen','lightpurple','lightorange','lightcyan','lightmagenta','lightgeekblue','lightgold','lightlime','lightvolcano','lightyellow','lightpink','lightgrey']

#st.write(st.session_state.doctorender['content'].split('```'))

#st.write(extrac_videolinks(st.session_state.doctorender['content']))
#st.write(extrac_code(st.session_state.doctorender['content']))


videos = extrac_videolinks(st.session_state.doctorender['content'])

graphs = extrac_dot(st.session_state.doctorender['content'])

st.title(st.session_state.doctorender['titulo'])
st.caption(f"{format_date(st.session_state.doctorender['xata']['createdAt'][0:10])}, {st.session_state.doctorender['autor']['nombre_completo']}")

tgs = [sac.Tag(label=tag,color=colors[i%len(colors)]) for i,tag in enumerate(st.session_state.doctorender['tags'])]
sac.tags(tgs,align='start')
st.divider()

for i,part in enumerate(split_parts(st.session_state.doctorender['content'])):
    render_part(part,graphs,videos)

#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
