import streamlit as st
from st_xatadb_connection import XataConnection
import datetime
from streamlit_quill import st_quill
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from modules import Card, Dashboard, DataGrid, Editor, Pie, Player, Radar, Timer
import hydralit_components as hc
from streamlit_extras.switch_page_button import switch_page



#---------------------------------Page config---------------------------------
st.set_page_config(layout="wide", page_title="Perfil",initial_sidebar_state="collapsed", page_icon="rsc/Logos/LOGO_CAPPA.jpg")

xata = st.connection('xata',type=XataConnection)
st.markdown('''
<style>
[data-testid="collapsedControl"] {
        display: none
    }
#MainMenu, header, footer {visibility: hidden;}
.st-emotion-cache-ocqkz7 {
  display: flex;
  flex-wrap: wrap;
  -moz-box-flex: 1;
  flex-grow: 1;
  -moz-box-align: stretch;
  align-items: stretch;
  gap: 0rem;
  padding-top: 2rem;
}
.st-emotion-cache-z5fcl4 {
  padding-left: 0.5rem;
  padding-right: 0.5rem;
  padding-bottom: 0;
}
.appview-container .main .block-container {
  padding-top: 1rem;
  padding-right: 0.5rem;
  padding-left: 0.5rem;
  padding-bottom: 0rem;
}
</style>
''', unsafe_allow_html=True)

if 'auth_state' not  in st.session_state or st.session_state['auth_state'] == False:
    #Si no hay un usuario logeado, se muestra la pagina de login
    switch_page('login')


#---------------------------------Funciones---------------------------------
def get_user(id):
    return xata.get("Usuario", id)




#---------------------------------Variables de estado---------------------------------
if 'query' in st.session_state and st.session_state.query['Table'] == 'Usuario':
    if 'profile_data' not in st.session_state :
        st.session_state.profile_data = get_user(st.session_state.query['id'])
    else:
        st.session_state.profile_data = get_user(st.session_state.query['id'])
else:
    st.error("404 Not Found")
    st.image("https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif")




if 'auth_state' not  in st.session_state:
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
        first_select=80
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



#---------------------------------Body---------------------------------
cols = st.columns([0.3,0.7])

with cols[0]:
    #st.write(st.session_state.profile_info)

    st.markdown(f"""
    <img src="{st.session_state.profile_data['avatar']['url']}" alt="profile picture" width="200" height="200"  style="border-radius:50%;">
    """, unsafe_allow_html=True)

    st.subheader(f"@{st.session_state.profile_data['username']}")
    st.caption(f"{'「✔ ᵛᵉʳᶦᶠᶦᵉᵈ」' if st.session_state.profile_data['verificado'] else ''}")
    st.caption(f"{st.session_state.profile_data['rol']}")
    st.caption(f"""
        <a href="mailto:{st.session_state.profile_data['correo']}">{st.session_state.profile_data['correo']}</a>
        """, unsafe_allow_html=True)

    st.markdown(f"""

        **Nombre:**

        {st.session_state.profile_data['nombre_completo']}

        **Fecha de nacimiento:**

        {st.session_state.profile_data['fechaNacimiento'][:10]}

        **Ranking:** {st.session_state.profile_data['rango']}

        **Puntos:** {st.session_state.profile_data['score']}
    """)
    if st.session_state.profile_data['id'] == st.session_state.username:
        if st.checkbox("Editar perfil"):
            with st.form(key='profile_edit_form'):
                st.caption('Edite los campos que desee cambiar')
                navatar = st.file_uploader("Avatar", type=['png','jpg','jpeg'])
                name = st.text_input("Nombre completo", value=st.session_state.profile_data['nombre_completo'])
                birth = st.date_input("Fecha de nacimiento", value=datetime.datetime.strptime(st.session_state.profile_data['fechaNacimiento'][:10], '%Y-%m-%d'))
                submit = st.form_submit_button("Guardar cambios")
    if st.session_state.userinfo['rol'] == 'Administrador' and st.session_state.profile_data['rol'] != 'Administrador':
        nrol = st.selectbox("Editar Rol", options=['Moderador','Profesor','Estudiante'])


with cols[1]:
    with st.container(border=True):
        c0 = st.columns([0.7,0.3])

        c0[0].subheader("Biografía")

        if st.session_state.profile_data['id'] == st.session_state.username:
            if c0[1].checkbox("Editar biografía"):
                tabs = st.tabs(["Editor de texto", 'Markdown'])
                with tabs[0]:
                    with st.form(key='my_form'):
                        desc = st_quill(placeholder='Mi biografía',html=True,key='quill-profile',
                        value=st.session_state.profile_data['feed'] if 'feed' in st.session_state.profile_data else '')
                        editcols = st.columns([0.8,0.2])

                        with editcols[1]:
                            savedesc = st.form_submit_button(label='Preview',use_container_width=True)

                        if savedesc:
                            st.markdown("##### Preview")
                            st.markdown(desc, unsafe_allow_html=True)
                with tabs[1]:
                    if "w_profile" not in state:
                        board = Dashboard()
                        w = SimpleNamespace(
                            dashboard=board,
                            editor=Editor(
                                board,
                                0,
                                0,
                                8,
                                6,
                            )
                        )
                        state.w_profile = w
                        if 'feed' in st.session_state.profile_data:
                            w.editor.add_tab("Markdown", st.session_state.profile_data['feed'], "markdown")
                        else:
                            w.editor.add_tab("Markdown", "# Hola Mundo!", "markdown")


                    else:
                        w = state.w_profile

                    with elements("workspace"):
                        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
                        with w.dashboard(rowHeight=57):
                            w.editor()
                            desc = w.editor.get_content("Markdown")

                    st.subheader("Preview")
                    st.markdown(desc, unsafe_allow_html=True)



                savedesc = st.button("Guardar cambios")
                if savedesc:
                    #st.write(desc)
                    try:
                        result = xata.update("Usuario", st.session_state.username, {"feed": desc})
                        st.success("Cambios guardados")
                        st.write(result)
                        st.session_state.profile_data = get_user(st.session_state.query['id'])
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al guardar cambios: {e}")

        if 'feed' in st.session_state.profile_data:
            st.markdown(st.session_state.profile_data['feed'], unsafe_allow_html=True)






#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)

