import streamlit as st
from st_xatadb_connection import XataConnection
import datetime
from streamlit_quill import st_quill
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from modules import Card, Dashboard, DataGrid, Editor, Pie, Player, Radar, Timer
import hydralit_components as hc
import extra_streamlit_components as stx
import time
import asyncio
from Clases import Usuario,Autenticador
from streamlit_searchbox import st_searchbox


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


#---------------------------------Funciones---------------------------------
def get_user(idd):
    return xata.get("Usuario", idd)

def search_usuario(s: str):
    try:
        result = xata.search_on_table('Usuario',{"query": s, "fuzziness": 0, "prefix": "phrase"})
        return result['records']
    except:
        return []

def get_username(user):
    idf = xata.query("Usuario",{"columns":["id"],"filter":{"username":{"$is" : user}}})
    if 'records' in idf and len(idf['records']) > 0:
        return idf['records'][0]['id']

def get_manager():
    return stx.CookieManager()

async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')


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

cookie = cookie_manager.get('query')

if cookie is None and ('query' in st.session_state and cookie != st.session_state.query) :
    cookie_manager.set('query',st.session_state.query)
    with st.spinner('Cargando Perfil...'):
        time.sleep(5)




if auth():
    #st.session_state['userinfo']
    if st.session_state.user is not None and (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
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
            first_select=60
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

    if  menu_id == 'courses':
        st.switch_page('pages/CoursesHome.py')



    if st.session_state.user is not None and (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
        if menu_id == 'subid144':
            st.switch_page('pages/test_editor.py')

        if menu_id == 'doceditor':
            st.switch_page('pages/doc_editor.py')

        if menu_id == 'docshome':
            st.switch_page('pages/docs_home.py')

        if menu_id == 'subid44':
            st.switch_page('pages/problems_editor.py')

        if menu_id == 'subid00':
            st.switch_page('pages/problems_home.py')

    else:
        if menu_id == 'docs':
            st.switch_page('pages/docs_home.py')

        if menu_id == 'Problemas':
            st.switch_page('pages/problems_home.py')
else:
    asyncio.run(show_message_error())
    st.stop()



#---------------------------------Variables de estado---------------------------------
if 'query' in st.session_state and st.session_state.query['Table'] == 'Usuario':
    if 'profile_data' not in st.session_state :
        try:
            st.session_state.profile_data = get_user(st.session_state.query['id'])
        except Exception as e:
            st.error("404 Not Found")
            st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
            with st.expander("Detalles del error"):
                st.error(e)
            st.stop()
    else:
        try:
            st.session_state.profile_data = get_user(st.session_state.query['id'])
        except Exception as e:
            st.error("404 Not Found")
            st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
            with st.expander("Detalles del error"):
                st.error(e)
            st.stop()

elif 'table' in st.query_params and 'id' in st.query_params:
    if st.query_params['table'] == 'Usuario':
        q = {'Table':st.query_params['table'],'id':st.query_params['id']}
        st.session_state.query = q
        try:
            st.session_state.profile_data = get_user(st.query_params['id'])
        except Exception as e:
            st.error("404 Not Found")
            st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
            with st.expander("Detalles del error"):
                st.error(e)
            st.stop()
else:
    qcookie = cookie_manager.get('query')
    if qcookie is not None:
        st.session_state.query = qcookie
        try:
            st.session_state.profile_data = get_user(st.session_state.query['id'])
        except Exception as e:
            st.error("404 Not Found")
            st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
            with st.expander("Detalles del error"):
                st.error(e)
    else:
        st.error("404 Not Found")
        st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
        st.stop()







#---------------------------------Body---------------------------------


_,returnprofile = st.columns([0.8,0.2])

with returnprofile:
    bplace = st.empty()
    if st.session_state.profile_data['id'] != st.session_state.user.key:
        if bplace.button("Regresar a mi perfil",use_container_width=True):
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
            st.rerun()


cols = st.columns([0.3,0.7])


#---------------------------------Sidebar---------------------------------
with cols[0]:
    #st.write(st.session_state.profile_info)
    if 'avatar' not in st.session_state.profile_data:
            st.markdown(f"""<img src="{"https://source.unsplash.com/200x200/?python"}" alt="profile picture" width="200" height="200"  style="border-radius:50%;">
    """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <img src="{st.session_state.profile_data['avatar']['url']}" alt="profile picture" width="200" height="200"  style="border-radius:50%;">
        """, unsafe_allow_html=True)

    st.subheader(f"@{st.session_state.profile_data['username']}")
    st.caption(f"{st.session_state.profile_data['rol']}")
    st.caption(f"{'「✔ ᵛᵉʳᶦᶠᶦᵉᵈ」' if st.session_state.profile_data['verificado'] else ''}")
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
    #-------------------------------Editar perfil---------------------------------
    if st.session_state.user is not None and st.session_state.profile_data['id'] == st.session_state.user.key:
        if st.checkbox("Editar perfil"):
            with st.form(key='profile_edit_form'):
                st.caption('Edite los campos que desee cambiar')
                navatar = st.file_uploader("Avatar", type=['png','jpg','jpeg'])
                name = st.text_input("Nombre completo", value=st.session_state.profile_data['nombre_completo'])
                birth = st.date_input("Fecha de nacimiento", value=datetime.datetime.strptime(st.session_state.profile_data['fechaNacimiento'][:10], '%Y-%m-%d'))

                udata = {}

                if name != st.session_state.profile_data['nombre_completo']:
                    udata['nombre_completo'] = name

                if birth != datetime.datetime.strptime(st.session_state.profile_data['fechaNacimiento'][:10], '%Y-%m-%d'):
                    udata['fechaNacimiento'] = birth.strftime("%Y-%m-%dT%H:%M:%SZ")

                submit = st.form_submit_button("Guardar cambios")

                if submit:
                    try:
                        res = xata.update("Usuario", st.session_state.profile_data['id'], udata)
                        st.success("Cambios guardados")
                    except Exception as e:
                        st.error(f"Error al guardar cambios: {e}")

                    if navatar:
                        try:
                            resimg = xata.upload_file("Usuario", st.session_state.profile_data['id'], "avatar", navatar.read(), navatar.type)
                            st.success("Avatar actualizado")
                        except Exception as e:
                            st.error(f"Error al actualizar avatar: {e}")

    if st.session_state.user is not None and st.session_state.user.is_admin() and st.session_state.profile_data['rol'] != 'Administrador' :
        nrol = st.selectbox("Editar Rol", options=['Moderador','Profesor','Estudiante'],index=2)

        if nrol != st.session_state.profile_data['rol']:
            if st.button("Cambiar Rol"):
                try:
                    res = xata.update("Usuario", st.session_state.profile_data['id'], {"rol": nrol})
                    st.success("Rol actualizado")
                except Exception as e:
                    st.error(f"Error al actualizar rol: {e}")

#---------------------------------Biografía---------------------------------
with cols[1]:
    with st.container(border=True):
        c0 = st.columns([0.7,0.3])

        c0[0].subheader("Biografía")

        if st.session_state.user is not None and st.session_state.profile_data['id'] == st.session_state.user.key:
            #-------------------------------Editar biografía---------------------------------
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

                    with elements("profile_editor"):
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

        #-------------------------------Mostrar biografía---------------------------------
        if 'feed' in st.session_state.profile_data:
            st.markdown(st.session_state.profile_data['feed'], unsafe_allow_html=True)





_,searchcol = st.columns([0.3,0.7])
with searchcol:
    search = None
    with st.form(key='search_form',clear_on_submit=True):
        seacols = st.columns([0.8,0.2],gap='large')
        with seacols[0]:
            search = st.text_input("Buscar Usuario",placeholder="Buscar Usuario",label_visibility='collapsed',key='search')
        with seacols[1]:
            searchbtn = st.form_submit_button("Buscar",use_container_width=True)

    if search is not None and search != '':
        results = search_usuario(search)
        #st.write(results)
    else:
        results =  []


    placeholres= st.empty()
    with placeholres.container():
        for result in results:
            with st.expander(f"{result['username']}"):
                prfvols  = st.columns([0.8,0.2],gap='large')
                with prfvols[0]:
                    st.write(f"**Nombre**: {result['nombre_completo']}")
                    st.write(f"**Rol**: {result['rol']}")
                with prfvols[1]:
                    if st.button("Ver perfil",key=result['id'],use_container_width=True):
                        st.session_state.query = {'Table':'Usuario','id':result['id']}
                        st.rerun()
        if len(results) > 0:
            if st.button('Cerrar',use_container_width=True):
                placeholres.empty()

#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)

