import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
import pandas as pd
import hydralit_components as hc
from streamlit_extras.switch_page_button import switch_page
# Adjust the width of the Streamlit page
st.set_page_config(layout="wide", page_title='CAPPA', page_icon='rsc/Logos/LOGO_CAPPA.jpg', initial_sidebar_state='collapsed')

# Establish communication between pygwalker and streamlit


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
  padding: 1rem 1rem 1rem;
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


if st.session_state['userinfo']['rol'] == "Administrador" or st.session_state['userinfo']['rol'] == "Profesor" or st.session_state['userinfo']['rol'] == "Moderador":
    menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':'subid44','icon': "bi bi-gear", 'label':"Editor"}
        ]},
        {'id':'contest','icon': "bi bi-trophy", 'label':"Concursos"},
        {'icon': "bi bi-graph-up", 'label':"Analisis de Datos",'ttip':"Herramientas de Analisis de Datos"},
        {'id':'spreadsheet','icon': "bi bi-file-earmark-richtext", 'label':"Mitosheet",
        'ttip':"Herramientas de Analisis de Datos"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Blog",'ttip':"Articulos e Información",
        'submenu':[
            {'id':'doceditor','icon': "bi bi-gear", 'label':"Editor" },
            {'id':'docshome','icon': "bi bi-search", 'label':"Home"}]
        },
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests", 'submenu':[
            {'label':"Todos", 'icon': "bi bi-search",'id':'alltests'},
            {'id':'subid144','icon': "bi bi-gear", 'label':"Editor" }]},
        {'id':'logout','icon': "bi bi-door-open", 'label':"Cerrar Sesión"}
    ]
else:
    menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",'id':'Problemas'},
        {'id':'contest','icon': "bi bi-trophy", 'label':"Concursos"},
        {'icon': "bi bi-graph-up", 'label':"Analisis de Datos",'ttip':"Herramientas de Analisis de Datos"},
        {'id':'spreadsheet','icon': "bi bi-file-earmark-richtext", 'label':"Mitosheet",
        'ttip':"Herramientas de Analisis de Datos"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Blog",'ttip':"Articulos e Información"},
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests"},
        {'id':'logout','icon': "bi bi-door-open", 'label':"Cerrar Sesión"}
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
        first_select=40
    )


if menu_id == 'Inicio':
  switch_page('Main')

if menu_id == 'code':
    switch_page('code_editor')

if menu_id == 'Analisis de Datos':
    switch_page('data_analysis_home')


if menu_id == 'logout':
    st.session_state.pop('auth_state')
    st.session_state.pop('userinfo')
    st.session_state.pop('username')
    switch_page('login')


if menu_id == st.session_state['userinfo']['username']:
    if 'query' not in st.session_state:
        st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
    else:
        st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
    switch_page('profile_render')

if st.session_state['userinfo']['rol'] == "Administrador" or st.session_state['userinfo']['rol'] == "Profesor" or st.session_state['userinfo']['rol'] == "Moderador":
    if menu_id == 'subid144':
        switch_page('test_editor')

    if menu_id == 'doceditor':
        switch_page('doc_editor')

    if menu_id == 'docshome':
        switch_page('docs_home')

    if menu_id == 'subid44':
        switch_page('problems_editor')

    if menu_id == 'subid00':
        switch_page('problems_home')
else:
    if menu_id == 'docs':
        switch_page('docs_home')

    if menu_id == 'Problemas':
        switch_page('problems_home')


#---------------------------------Body---------------------------------
st.title("Mitosheet Sandbox")
st.divider()
datasetspths = [
    'Default',
    ]
data = st.selectbox("Selecciona un Dataset", datasetspths,)


if data == 'Default':
    datas = 'https://raw.githubusercontent.com/plotly/datasets/master/tesla-stock-price.csv'
else:
    if  data.endswith('.csv'):
        datas = pd.read_csv(data)
    elif data.endswith('.xlsx'):
        datas = pd.read_excel(data)

new_dfs, code = spreadsheet(datas)

if st.checkbox('Mostrar Dataframes'):
    for k , df in new_dfs.items():
        st.dataframe(df,use_container_width=True)

st.subheader('Código de Python generado')
st.code(code)


#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
