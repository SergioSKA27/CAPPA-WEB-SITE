import streamlit as st
import hydralit_components as hc
from streamlit_lottie import st_lottie
import streamlit_antd_components as sac
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(layout="wide", page_title='CAPPA', page_icon='rsc/Logos/LOGO_CAPPA.jpg', initial_sidebar_state='collapsed')
st.markdown("""
<style>
body {
background-color: #f4ebe8;

}

[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}

.st-emotion-cache-z5fcl4 {
  width: 100%;
  padding: 0rem 1rem 1rem;
    padding-right: 0.5rem;
    padding-left: 0.5rem;
    padding-bottom: 0.5rem;
  min-width: auto;
  max-width: initial;

}
</style>
""",unsafe_allow_html=True)




#---------------------------------#
#Navigation Bar


if 'auth_state' not  in st.session_state or st.session_state['auth_state'] == False:
    menu_data = [
    {'icon': "far fa-copy", 'label':"Docs",'ttip':"Documentación de la Plataforma"},
    {'id':'About','icon':"bi bi-question-circle",'label':"FAQ",'ttip':"Preguntas Frecuentes"},
    {'id':'contact','icon':"bi bi-envelope",'label':"Contacto",'ttip':"Contáctanos"},
    ]
    logname = 'Iniciar Sesión'
else:
    #st.session_state['userinfo']
    if st.session_state['userinfo']['rol'] == "Administrador" or st.session_state['userinfo']['rol'] == "Profesor" or st.session_state['userinfo']['rol'] == "Moderador":
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
        home_name='Inicio',
        login_name=logname,
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
        first_select=30
    )
if menu_id == "Inicio":
    switch_page("Main")

if menu_id == 'Iniciar Sesión':
    switch_page('login')

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

with open("rsc/html/DataAHomeBanner.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

st.divider()

cols = st.columns(2)

with cols[0]:
    with st.container(border=True):
        st.image('https://user-images.githubusercontent.com/8137814/221879671-70379d15-81ac-44b9-b267-a8fa3842a0d9.png',use_column_width=True)
        st.caption('''
**Simplificando el Análisis de Datos con PyGWalker**

En el cambiante mundo del análisis de datos, la eficiencia y la simplicidad son fundamentales. Ingresa PyGWalker,
una herramienta revolucionaria que transforma datos crudos en aplicaciones de visualización interactiva con solo una
línea de código. Lo que distingue a PyGWalker es su compromiso de hacer que el análisis de datos sea accesible
y escalable, simplificando tareas complejas con un conjunto de funciones poderosas.
''')
        if st.button('Prueba PyGWalker 📊',use_container_width=True):
            switch_page('pgwalker_sandbox')

with cols[1]:
    with st.container(border=True):
        st.image('https://blog.streamlit.io/content/images/2023/08/Announcement.svg',use_column_width=True)
        st.caption('''
**Mito: Potenciando tus Hojas de Cálculo en la Universidad**

Explora Mito, la herramienta que lleva tus hojas de cálculo a un nuevo nivel. En el entorno universitario,
simplifica la edición de hojas de cálculo y genera código Python automáticamente con cada ajuste en Mito.
Describe tus cambios en inglés simple y deja que Mito traduzca todo a código. Transforma tus procesos de manera rápida
y eficiente con Mito.

**Características Principales**

- **Edición de Hojas de Cálculo Simplificada**.

- **Generación Instantánea de Código Python**.

- **Accesible para Todos**.

- **Transforma tus Datos con IA**.

''')
        if st.button('Prueba Mito 📈',use_container_width=True):
            switch_page('spreadsheets_sandbox')
#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
