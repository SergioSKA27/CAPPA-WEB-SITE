import streamlit as st
from st_xatadb_connection import XataConnection
import hydralit_components as hc
from streamlit_extras.switch_page_button import switch_page
import streamlit_antd_components as sac
import datetime
import google.generativeai as genai
import markdown


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
    return [parts[i] for i in range(len(parts)) if len(parts[i]) > 0 and '```' not in parts[i]]

def render_part(part):
    if part is None:
        return
    langs = ["Python", "JavaScript", "Java", "C", "Cpp", "C#", "HTML", "CSS", "SQL",
    "R", "Rust", "Go", "PHP", "TypeScript", "Ruby", "Swift", "Kotlin", "Scala", "Julia", "Dart", "Haskell", "Lua",
    "Perl", "Objective-C", "MATLAB","Markdown", "JSON", "YAML", "Dockerfile", "GraphQL", "Handlebars", "LaTeX",
    "Groovy", "PowerShell", "VBScript", "Clojure", "Elixir", "F#", "Fortran", "OCaml",
    "Pascal", "Racket", "Scheme", "Bash", "Assembly", "CoffeeScript", "Erlang", "Haxe", "Nim", "OCaml", "Prolog",
    "PureScript", "Reason", "Scratch", "Solidity", "Tcl", "Vim", "XML", "YAML"]

    htmltags = ['<p>', '<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>', '<ul>', '<ol>', '<li>', '<blockquote>', '<hr>',
    '<br>', '<a>', '<img>', '<table>', '<thead>', '<tbody>', '<tr>', '<th>', '<td>', '<pre>', '<code>', '<em>',
    '<strong>', '<del>', '<sup>', '<sub>', '<iframe>', '<script>', '<style>', '<div>', '<span>', '<input>', '<button>',
    '<label>', '<select>', '<option>', '<form>', '<textarea>', '<svg>', '<canvas>', '<audio>', '<video>', '<math>',
    '<figure>', '<figcaption>', '<noscript>', '<header>', '<footer>', '<main>', '<section>', '<article>', '<aside>',
    '<nav>', '<details>', '<summary>', '<dialog>', '<template>', '<slot>']

    if 'video' in part:
        vcol = st.columns([0.3,0.4,0.3])
        p1 = part.split('\n')
        with vcol[1]:
            st.video(p1[1])
    elif any([lang.lower() in part for lang in langs]) and (not any([tag in part for tag in htmltags]) and 'html' not in part.lower()):
        p1 = part.split('\n')

        st.code('\n'.join(p1[1:]),language=p1[0].lower())
    elif 'dot' in part:
        p1 = part.split('\n')
        st.graphviz_chart('\n'.join(p1[1:]))
    else:
        st.markdown(part,unsafe_allow_html=True)
if 'query' not in st.session_state:
    switch_page('docs_home.py')

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




##---------------------------------Navbar---------------------------------
if 'auth_state' not  in st.session_state or st.session_state['auth_state'] == False:
    menu_data = [
    {'icon': "far fa-copy", 'label':"Blog",'ttip':"Articulos e Información",'id':'Blog'},
    {'label':"Articulo",'icon':"bi bi-file-earmark-richtext",'id':'renderdoc'},
    {'id':'About','icon':"bi bi-question-circle",'label':"FAQ",'ttip':"Preguntas Frecuentes"},
    {'id':'contact','icon':"bi bi-envelope",'label':"Contacto",'ttip':"Contáctanos"},
    ]
    logname = 'Iniciar Sesión'
    fs = 20
else:
    #st.session_state['userinfo']
    if st.session_state['userinfo']['rol'] == "Administrador" or st.session_state['userinfo']['rol'] == "Profesor" or st.session_state['userinfo']['rol'] == "Moderador":
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':'subid44','icon': "bi bi-gear", 'label':"Editor"}
        ]},
        {'id':'contest','icon': "bi bi-trophy", 'label':"Concursos"},
        {'icon': "bi bi-graph-up", 'label':"Analisis de Datos",'ttip':"Herramientas de Analisis de Datos"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Blog",'ttip':"Articulos e Información",
        'submenu':[
            {'id':'doceditor','icon': "bi bi-gear", 'label':"Editor" },
            {'id':'docshome','icon': "bi bi-search", 'label':"Home"}]
        },
        {'label':"Articulo",'icon':"bi bi-file-earmark-richtext",'id':'renderdoc'},
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests", 'submenu':[
            {'label':"Todos", 'icon': "bi bi-search",'id':'alltests'},
            {'id':'subid144','icon': "bi bi-gear", 'label':"Editor" }]},
        {'id':'logout','icon': "bi bi-door-open", 'label':"Cerrar Sesión"},
    ]
    else:
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",'id':'Problemas'},
        {'id':'contest','icon': "bi bi-trophy", 'label':"Concursos"},
        {'icon': "bi bi-graph-up", 'label':"Analisis de Datos",'ttip':"Herramientas de Analisis de Datos"},
        {'id':'Blog','icon': "bi bi-file-earmark-richtext", 'label':"Blog",'ttip':"Articulos e Información"},
        {'label':"Articulo",'icon':"bi bi-file-earmark-richtext",'id':'renderdoc'},
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests"},
        {'id':'logout','icon': "bi bi-door-open", 'label':"Cerrar Sesión"}
    ]
    logname = st.session_state['userinfo']['username']
    fs = 50

over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name="Inicio",
    login_name=logname,
    hide_streamlit_markers=False,  # will show the st hamburger as well as the navbar now!
    sticky_nav=True,  # at the top or not
    sticky_mode="sticky",  # jumpy or not-jumpy, but sticky or pinned
    first_select=fs,
)

if menu_id == "Inicio":
    switch_page("Main")

if menu_id == 'Iniciar Sesión':
    switch_page('login')

if menu_id == 'Analisis de Datos':
    switch_page('data_analysis_home')

if menu_id == 'code':
    switch_page('code_editor')

if menu_id == 'logout':
    st.session_state.pop('auth_state')
    st.session_state.pop('userinfo')
    st.session_state.pop('username')
    switch_page('login')



if st.session_state['auth_state']:
    if st.session_state['userinfo']['rol'] == "Administrador" or st.session_state['userinfo']['rol'] == "Profesor" or st.session_state['userinfo']['rol'] == "Moderador":
        if menu_id == 'subid00':
            switch_page('problems_home')
        if menu_id == 'subid44':
            switch_page('problems_editor')

        if menu_id == 'doceditor':
            switch_page('doc_editor')

        if menu_id == 'docshome':
            switch_page('docs_home')

        if menu_id == 'subid144':
            switch_page('test_editor')

    else:
        if menu_id == 'Problemas':
            switch_page('problems_home')
        if menu_id == 'Blog':
            switch_page('docs_home')


if 'userinfo' in st.session_state and st.session_state.userinfo is not None:
    if menu_id == st.session_state['userinfo']['username']:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
        switch_page('profile_render')





#---------------------------------Body---------------------------------
colors = ['blue','red','green','purple','orange','cyan','magenta','geekblue','gold','lime','volcano','yellow','pink','grey','darkblue','darkred','darkgreen','darkpurple','darkorange','darkcyan','darkmagenta','darkgeekblue','darkgold','darklime','darkvolcano','darkyellow','darkpink','darkgrey','lightblue','lightred','lightgreen','lightpurple','lightorange','lightcyan','lightmagenta','lightgeekblue','lightgold','lightlime','lightvolcano','lightyellow','lightpink','lightgrey']

st.write(st.session_state.doctorender['content'].split('```'))

st.title(st.session_state.doctorender['titulo'])
st.caption(f"{format_date(st.session_state.doctorender['xata']['createdAt'][0:10])}, {st.session_state.doctorender['autor']['nombre_completo']}")

tgs = [sac.Tag(label=tag,color=colors[i%len(colors)]) for i,tag in enumerate(st.session_state.doctorender['tags'])]
sac.tags(tgs,align='start')
st.divider()
with st.container(border=True):
    for part in split_parts(st.session_state.doctorender['content']):
        st.markdown(part)


#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
