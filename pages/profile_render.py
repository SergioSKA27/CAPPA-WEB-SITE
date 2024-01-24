import streamlit as st
from st_xatadb_connection import XataConnection
import datetime
from streamlit_quill import st_quill
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from modules import Card, Dashboard, DataGrid, Editor, Pie, Player, Radar, Timer


xata = st.connection('xata',type=XataConnection)


def get_user(id):
    return xata.get("Usuario", id)


if 'query' in st.session_state and st.session_state.query['Table'] == 'Usuario':
    if 'profile_data' not in st.session_state :
        st.session_state.profile_data = get_user(st.session_state.query['id'])
    else:
        st.session_state.profile_data = get_user(st.session_state.query['id'])
else:
    st.error("404 Not Found")
    st.image("https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif")





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
                        desc = st_quill(placeholder='Mi biografía',html=True,key='quill-profile')
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
                    st.write(desc)
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







