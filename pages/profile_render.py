import streamlit as st
from st_xatadb_connection import XataConnection


xata = st.connection('xata',type=XataConnection)


def get_user(id):
    return xata.get("Usuario", id)



if 'query' in st.session_state and st.session_state.query['Table'] == 'Usuario':
    if 'profile_info' not in st.session_state:
        st.session_state.profile_info = get_user(st.session_state.query['id'])
    else:
        st.session_state.profile_info = get_user(st.session_state.query['id'])
else:
    st.error("404 Not Found")
    st.image("https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif")





cols = st.columns([0.3,0.7])

with cols[0]:
    #st.write(st.session_state.profile_info)

    st.markdown(f"""
    <img src="{st.session_state.profile_info['avatar']['url']}" alt="profile picture" width="200" height="200"  style="border-radius:50%;">
    """, unsafe_allow_html=True)

    st.subheader(f"@{st.session_state.profile_info['username']}")
    st.caption(f"{'「✔ ᵛᵉʳᶦᶠᶦᵉᵈ」' if st.session_state.profile_info['verificado'] else ''}")
    st.caption(f"{st.session_state.profile_info['rol']}")
    st.caption(f"""
        <a href="mailto:{st.session_state.profile_info['correo']}">{st.session_state.profile_info['correo']}</a>
        """, unsafe_allow_html=True)

    st.markdown(f"""

        **Nombre:**

        {st.session_state.profile_info['nombre_completo']}

        **Fecha de nacimiento:**

        {st.session_state.profile_info['fechaNacimiento'][:10]}

        **Ranking:** {st.session_state.profile_info['rango']}

        **Puntos:** {st.session_state.profile_info['score']}
    """)
