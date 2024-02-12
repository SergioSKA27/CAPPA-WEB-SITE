import time
import streamlit as st
import hydralit_components as hc
from streamlit_extras.switch_page_button import switch_page
from types import SimpleNamespace
from streamlit_quill import st_quill
from streamlit import session_state as state
from streamlit_elements import elements, event, lazy, mui, sync
from streamlit_extras.switch_page_button import switch_page
from st_xatadb_connection import XataConnection
from streamlit_tags import st_tags
import google.generativeai as genai
import extra_streamlit_components as stx
from st_xatadb_connection import XataConnection
from Clases import Usuario,Autenticador

from modules import Card, Dashboard, Editor,  Timer,Player
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
genai.configure(api_key=st.secrets['GEN_AI_KEY'])

if 'auth_state' not in st.session_state or not ( st.session_state['userinfo']['rol'] == "Administrador" or st.session_state['userinfo']['rol'] == "Profesor" or st.session_state['userinfo']['rol'] == "Moderador"):
    switch_page('login')

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


@st.cache_resource
def load_genmodel():
    return genai.GenerativeModel('gemini-pro')

def ask_AI():
    model = load_genmodel()
    response = ''
    with st.container(border=True):
        question = st.text_area('Escribe tu petición',help='Escribe tu petición para generar un documento',height=250)
        if st.button(label='Generar Documento ✨'):
            with st.spinner("Generando documento..."):
                response = model.generate_content(question)
    return response



def merge_text(text: list):
    return "\n".join(text)

def format_code(code: str, lang: str):
    return f"```{lang}\n{code}\n```"

def format_video(url: str):
    return f"```video\n{url}\n```"

st.title('Editor de Documentos')
st.divider()


if 'gtoast' not in state:
    state.gtoast = 0

if 'tabs' not in state:
    state.tabs = ["Editor de texto", 'Código','Video']

if 'doc_sections' not in state:
    state.doc_sections = {}

if 'videolinks' not in state:
    state.videolinks = []

if state.gtoast == 1:
    st.toast("Puedes ver el gráfico en la pestaña de código")
    state.gtoast = 2


@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager()


cookie_manager = get_manager()
auth = Autenticador(xata,cookie_manager)

if auth() == False:
    auth.validate_cookie()
    if auth() == False:
        st.switch_page("pages/login.py")




##---------------------------------Navbar---------------------------------
if auth():
    #st.session_state['userinfo']
    if st.session_state.user.is_admin() or st.session_state.user.is_teacher() or st.session_state.user.is_moderator():
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':'subid44','icon': "bi bi-journal-code", 'label':"Editor"}
        ]},
        {'id':'courses','icon': "bi bi-journal-bookmark", 'label':"Cursos",'ttip':"Cursos de Programación y Ciencia de Datos en CAPPA"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Blog",'ttip':"Articulos e Información"},
        {'id':'doceditor','icon': "bi bi-file-earmark-richtext", 'label':"Editor" },
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests", 'submenu':[
            {'label':"Todos", 'icon': "bi bi-search",'id':'alltests'},
            {'id':'subid144','icon': "bi bi-gear", 'label':"Editor" }]},
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
        {'id':'doceditor','icon': "bi bi-file-earmark-richtext", 'label':"Editor" },
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
    home_name="Inicio",
    login_name=None,
    hide_streamlit_markers=False,  # will show the st hamburger as well as the navbar now!
    sticky_nav=True,  # at the top or not
    sticky_mode="sticky",  # jumpy or not-jumpy, but sticky or pinned
    first_select=40,
    )


    if menu_id == 'Inicio':
      st.switch_page('pages/app.py')

    if menu_id == 'code':
        st.switch_page('pages/code_editor')

    if menu_id == "docs":
            st.switch_page("pages/docs_home.py")

    if menu_id == 'logout':
        st.session_state.auth_state = False
        st.session_state.userinfo = None
        st.session_state.user = None
        st.session_state.username = None
        auth.delete_valid_cookie()
        with st.spinner('Cerrando Sesión...'):
            time.sleep(2)
        st.switch_page('pages/login.py')

    if menu_id == st.session_state['userinfo']['username']:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
        switch_page('profile_render')



    if st.session_state.user.is_admin() or st.session_state.user.is_teacher():

        if menu_id == 'subid00':
            switch_page('problems_home')

        if menu_id == 'subid44':
            st.switch_page('pages/problems_editor')


        if menu_id == 'subid144':
            st.switch_page('pages/test_editor')


        if menu_id == 'docshome':
            st.switch_page('pages/docs_home')

    else:
        if menu_id == "Problemas":
            st.switch_page("pages/problems_home.py")






#---------------------------------Toast---------------------------------

if "aitoast" not in state:
    state.aitoast = 0

if state.aitoast == 1:
    st.toast("Respuesta añadida con éxito puedes verla en la pestaña de código",icon="👾")
    state.aitoast = 0


#---------------------------------Body---------------------------------
pname =st.text_input('Titulo del Documento',placeholder="Principios de Programación en Python")

tags = st_tags([], suggestions=['Python', 'Básico', 'Intermedio', 'Avanzado'],
                label='Etiquetas', maxtags=10,text='Presiona enter para añadir una etiqueta',)

doc_types = ["Artículo", "Tutorial", "Video"]

bannerimage = st.file_uploader("Imagen de Portada", type=["png", "jpg", "jpeg"])

if bannerimage is not None:
    st.image(bannerimage, width=300)

desc_basic = st.text_area('Ingresa un resumen para mostrar en la página principal')

doc_type = st.selectbox("Tipo de Documento", doc_types)

#---------------------------------Editor---------------------------------
tabs = st.tabs(state.tabs)
with tabs[0]:
    desc = ''
    with st.form(key='my_form'):

        editcols = st.columns([0.8,0.2])
        with editcols[0]:
            desc = st_quill(placeholder='Contenido del Documento',html=True,key='quill-docs')
        with editcols[1]:
            action = st.selectbox("Acción", ["Preview", "Añadir Sección"])
            savedesc = st.form_submit_button(label=':floppy_disk: '
            ,use_container_width=True)
        if savedesc:
            if action == "Añadir Sección":
                if desc != '':
                    k = 1
                    while f"Sección {k}" in state.doc_sections:
                        k += 1
                    state.doc_sections[f"Sección {k}"] = desc
                    st.success("Sección añadida")
            else:
                st.markdown("##### Preview")
                st.markdown(desc, unsafe_allow_html=True)
with tabs[1]:
    if "w_docs" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            editor=Editor(
                board,
                0,
                0,
                10,
                8,
            )
        )
        state.w_docs = w
        w.editor.add_tab("Código Markdown", "# Hola Mundo!", "markdown")
    else:
        w = state.w_docs
    with st.container(border=True):
        cols= st.columns([0.8,0.2])
        with cols[0]:
            with elements("workspace"):
                event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
                with w.dashboard(rowHeight=57):
                    w.editor()
        with cols[1]:
            with st.form(key='lang_form'):
                lang = st.selectbox("Selecciona un lenguage", ["Python", "JavaScript", "Java", "C", "Cpp", "C#", "HTML", "CSS", "SQL",
    "R", "Rust", "Go", "PHP", "TypeScript", "Ruby", "Swift", "Kotlin", "Scala", "Julia", "Dart", "Haskell", "Lua",
    "Perl", "Objective-C", "MATLAB","Markdown", "JSON", "YAML", "Dockerfile", "GraphQL", "Handlebars", "LaTeX",
    "Groovy", "PowerShell", "VBScript", "Clojure", "Elixir", "F#", "Fortran", "OCaml",
    "Pascal", "Racket", "Scheme", "Bash", "Assembly", "CoffeeScript", "Erlang", "Haxe", "Nim", "OCaml", "Prolog",
    "PureScript", "Reason", "Scratch", "Solidity", "Tcl", "Vim", "XML", "YAML"])

                if st.form_submit_button(label="Añadir Tab"):
                    if f"Código {lang}" not in w.editor._tabs:
                        w.editor.add_tab(f"Código {lang}", '', lang.lower())
                        w.editor.add_tab(f"Código {lang}", '', lang.lower())
                    else:
                        k = 1
                        while f"Código {lang} {k}" in w.editor._tabs:
                            k += 1

                        w.editor.add_tab(f"Código {lang} {k}", '', lang.lower())
                    st.rerun()
            with st.form(key='tab_form'):
                deltab = st.selectbox("Eliminar Tab", ["Selecciona un tab"] + list(w.editor._tabs.keys()))
                if st.form_submit_button(label="Eliminar Tab"):
                    if deltab != "Selecciona un tab" and len(w.editor._tabs) > 1:
                        del w.editor._tabs[deltab]
                        st.rerun()
            if st.button("Añadir Gráfica",use_container_width=True):
                if "Gráfico" not in w.editor._tabs:
                     w.editor.add_tab("Gráfica",'''
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
''', "dot")
                else:
                    k = 1
                    while f"Gráfico {k}" in w.editor._tabs:
                        k += 1
                    w.editor.add_tab(f"Gráfica {k}", '', "dot")
                st.rerun()



        ptabs = st.tabs(w.editor._tabs.keys())
        for i, tab in enumerate(w.editor._tabs.keys()):
            with ptabs[i]:
                if "Markdown" in tab:
                    st.write(w.editor.get_content(tab))
                elif  "Gráfica" in tab:
                    st.graphviz_chart(w.editor.get_content(tab))
                elif "Respuesta" in tab:
                    st.markdown(w.editor.get_content(tab), unsafe_allow_html=True)
                else:
                    st.code(w.editor.get_content(tab), language=tab.split(" ")[1].lower())
with tabs[2]:
    if "w_video" not in state:
        board = Dashboard()
        wv = SimpleNamespace(
            dashboard=board,
            player=Player(
                board,
                0,
                0,
                10,
                6,
            )
        )
        state.w_video = wv
    else:
        wv = state.w_video

    with st.container(border=True):
        with elements("video"):
            with wv.dashboard(rowHeight=57):
                wv.player()
        st.caption("Para añadir un video, copia el link del video y reprodúcelo en el reproductor para tener una vista previa.")
        st.caption("Una vez que estés satisfecho con el video, presiona el botón de añadir video para añadirlo al documento.")
        if st.button("Añadir Video"):
            if wv.player._url not in state.videolinks:
                state.videolinks.append(wv.player._url)

asiscols = st.columns([0.7,0.3])

if asiscols[1].checkbox("Preguntar al Asistente de IA 👾 "):
    r = ask_AI()
    if r != '':
        k = 1
        while f'Respuesta {k}'  in w.editor._tabs:
            k += 1
        w.editor.add_tab(f'Respuesta {k}', r.text, "markdown")
        state.aitoast = 1
        st.rerun()


st.subheader("Layout del Documento")
layout = st.multiselect("Selecciona las seciones del documento en orden",list(w.editor._tabs.keys())+[f"Link {k}" for k in range(len(state.videolinks))]+list(state.doc_sections.keys()))

if layout:
    lay = []
    for i, l in enumerate(layout):
        if "Sección" in l:
            st.markdown(state.doc_sections[l], unsafe_allow_html=True)
            lay.append(state.doc_sections[l])
        elif "Gráfica" in l:
            st.graphviz_chart(w.editor.get_content(l))
            lay.append(format_code(w.editor.get_content(l), "dot"))
        elif "Markdown" in l:
            st.markdown(w.editor.get_content(l), unsafe_allow_html=True)
            lay.append(w.editor.get_content(l))
        elif "Link" in l:
            colv = st.columns([0.2,0.6,0.2])
            colv[1].video(state.videolinks[int(l.split(" ")[1])],)
            lay.append(format_video(state.videolinks[int(l.split(" ")[1])]))
        elif "Respuesta" in l:
            st.markdown(w.editor.get_content(l), unsafe_allow_html=True)
            lay.append(w.editor.get_content(l))
        else:
            st.code(w.editor.get_content(l), language=l.split(" ")[1].lower())
            lay.append(format_code(w.editor.get_content(l), l.split(" ")[1].lower()))

    merged = merge_text(lay)

    subcols = st.columns([0.3,0.4,0.3])
    if subcols[1].button("Subir Documento",use_container_width=True):
        if pname != '' and merged != '' and tags != []:
            try:
                r = xata.insert("Documento", {
                "titulo": pname,
                "tags": tags,
                "content": merged,
                "tipo": doc_type,
                "autor": st.session_state['username'],
                "shortdesc": desc_basic,
                })
                st.success("Documento subido con éxito")
                st.balloons()
                st.write(r)
                state.doc_sections = {}
                state.videolinks = []
                del state.w_docs
            except Exception as e:
                st.error(f'Error al subir el documento: {e}')

            if bannerimage is not None:
                try:
                    r = xata.upload_file("Documento",r['id'],'banner_pic',bannerimage.read(),content_type=bannerimage.type)
                    st.success("Imagen subida con éxito")
                    st.balloons()
                    st.write(r)
                except Exception as e:
                    st.error(f'Error al subir la imagen: {e}')


#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
