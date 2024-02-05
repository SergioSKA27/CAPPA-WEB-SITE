import streamlit as st
import hydralit_components as hc
from streamlit_lottie import st_lottie
import streamlit_antd_components as sac
from streamlit_extras.switch_page_button import switch_page

#Autor: Sergio Demis Lopez Martinez
#This is the main file for the CAPPA project and will contain the landing page

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


if 'auth_state' not in st.session_state:
    st.session_state.auth_state = False

#---------------------------------Functions---------------------------------------------------------
def pythonlogo():
    """
    The `pythonlogo` function displays the Python logo using SVG code and a CSS file.
    """
    with open('rsc/css/style_PythonLogo.css') as f:
        container1 = st.empty()
        columns1,col2,col3 = st.columns(3)
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        with columns1:
            container1.markdown(
    '''<svg width="40%" height="40%" viewBox="0 0 512 512" xmlns="http://www.w3.org/2000/svg" id="python-logo">
    <path d="m116 296c0-30.328125 24.671875-55 55-55h170c13.785156 0 25-11.214844 25-25v-141c0-41.355469-33.644531-75-75-75h-70c-41.355469 0-75 33.644531-75 75v41h110c8.285156 0 15 6.714844 15 15s-6.714844 15-15 15h-181c-41.355469 0-75 33.644531-75 75v70c0 41.355469 33.644531 75 75 75h41zm105-220c-8.285156 0-15-6.714844-15-15s6.714844-15 15-15 15 6.714844 15 15-6.714844 15-15 15zm0 0" />
    <path d="m437 146h-41v70c0 30.328125-24.671875 55-55 55h-170c-13.785156 0-25 11.214844-25 25v141c0 41.355469 33.644531 75 75 75h70c41.355469 0 75-33.644531 75-75v-41h-110c-8.285156 0-15-6.714844-15-15s6.714844-15 15-15h181c41.355469 0 75-33.644531 75-75v-70c0-41.355469-33.644531-75-75-75zm-146 290c8.285156 0 15 6.714844 15 15s-6.714844 15-15 15-15-6.714844-15-15 6.714844-15 15-15zm0 0" />
    </svg>''',unsafe_allow_html=True
            )


#use this instead
with open('rsc/html/headlogos.html') as f:
    st.markdown(f.read(),unsafe_allow_html=True)
#---------------------------------#
#Navigation Bar


if 'auth_state' not  in st.session_state or st.session_state['auth_state'] == False:
    menu_data = [
    {'icon': "far fa-copy", 'label':"Blog",'ttip':"Articulos e Información",'id':'Blog'},
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
            {'id':'subid44','icon': "bi bi-gear", 'label':"Editor"}
        ]},
        {'id':'contest','icon': "bi bi-trophy", 'label':"Concursos"},
        {'icon': "bi bi-graph-up", 'label':"Analisis de Datos",'ttip':"Herramientas de Analisis de Datos"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Blog",'ttip':"Articulos e Información",
        'submenu':[
            {'id':'doceditor','icon': "bi bi-gear", 'label':"Editor" },
            {'id':'docshome','icon': "bi bi-search", 'label':"Home"}]
        },
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
        sticky_nav=False, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
    )


if st.session_state['auth_state']:
    if st.session_state['userinfo']['rol'] == "Administrador" or st.session_state['userinfo']['rol'] == "Profesor" or st.session_state['userinfo']['rol'] == "Moderador":
        if menu_id == 'subid00':
            switch_page('problems_home')
        if menu_id == 'subid44':
            switch_page('problems_editor')

        if menu_id == 'docshome':
            switch_page('docs_home')

        if menu_id == 'doceditor':
            switch_page('doc_editor')

        if menu_id == 'subid144':
            switch_page('test_editor')

    else:
        if menu_id == 'Problemas':
            switch_page('problems_home')

        if menu_id == 'Blog':
            switch_page('docs_home')


if menu_id == 'Iniciar Sesión':
    switch_page('login')

if menu_id == 'Analisis de Datos':
    switch_page('data_analysis_home')

if menu_id == 'Blog':
    switch_page('docs_home')

if menu_id == 'code':
    switch_page('code_editor')

if menu_id == 'logout':
    st.session_state.pop('auth_state')
    st.session_state.pop('userinfo')
    st.session_state.pop('username')
    switch_page('login')

if 'userinfo' in st.session_state and st.session_state.userinfo is not None:
    if menu_id == st.session_state['userinfo']['username']:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
        switch_page('profile_render')


#---------------------------------#
#Welcome Message
cols0 = st.columns([0.6,0.4])
with cols0[0]:
    with open('rsc/html/Main-Banner1.html') as f:
        st.markdown(f.read(), unsafe_allow_html=True)

with cols0[1]:
    st_lottie('https://lottie.host/140704e5-be12-4599-9a87-c945ab953df4/7qF25McNau.json',quality='low')




sac.divider(label='',align='center')
#---------------------------------#
#Caracteristicas del sitio
with open('rsc/css/MainBanners.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.markdown('''
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Mosk:wght@400;700&display=swap">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
    h4 {
      text-align: center;
      font-family: 'Bebas Neue' ;
      color: #333;
      font-size: 2.1rem;
    }
</style>
<div style="padding-top: 1rem; padding-bottom: 1rem;">
<h4>
Descubre la Esencia de Nuestra Plataforma<br> Características que Transforman tu Experiencia de Programación
</h4>
</div>
''',unsafe_allow_html=True)
st.markdown('''
<style>
.warning-message {
    display: none; /* Oculta el mensaje por defecto */
    background-color: #ffcccb; /* Color de fondo del mensaje de advertencia */
    padding: 10px;
    text-align: center;
}

/* Media query para pantallas pequeñas */
@media only screen and (max-width: 600px) {
    .warning-message {
        display: block; /* Muestra el mensaje en pantallas pequeñas */
    }
}
</style>
<div class="warning-message">
    <p>Esta aplicación está optimizada para computadoras. Te recomendamos utilizar una pantalla más grande para una mejor experiencia.</p>
</div>
''', unsafe_allow_html=True)
sac.divider(label='Características',align='center',icon='rocket',)
st.markdown('''
<h4>Problemas<br> Sumérgete en un mundo de desafíos y mejora tus habilidades con nuestra amplia gama de problemas</h4>
<p style="text-align: center;font-family: 'Raleway';font-size: 1rem;">
    Descubre el placer de resolver problemas y mejora constantemente tu habilidad para abordar desafíos cada vez más
    complejos.<br>
    ¡Prepárate para el viaje emocionante de la resolución de problemas en nuestro espacio de desarrollo
    y desafíos en programación!

</p>
''',unsafe_allow_html=True)
cols1 = st.columns([0.7,0.3])

with cols1[0]:
    with open('rsc/html/Main-Banner2.html') as f:
        st.markdown(f.read(),unsafe_allow_html=True)

somelottie ='https://lottie.host/c41a8ef4-fc04-4219-a774-163c87c6c677/2q1ZVNlPDJ.json'
with cols1[1]:
    st_lottie('https://lottie.host/5295a4fe-7a58-4245-a71a-5be321a45b6a/IdGdn1WOgB.json',quality='low')
    st_lottie('https://lottie.host/20ba4be7-6b85-4613-a152-d77cb8b1a787/vQygOL7QiX.json',quality='low')

sac.divider(label='',align='center',icon='code')

st.markdown('''
<h4 style="padding-top: 1rem; padding-bottom: 1rem;">
Editor de Código<br> Tu Lugar de Poder en el Club de Programación en Python Avanzado
</h4>
<p style="text-align: center;font-family: 'Raleway';font-size: 1rem;">
En el corazón de nuestro Club reside el Editor de Código, una herramienta potente y versátil que redefine tu experiencia
de programación en Python.Diseñado específicamente para miembros del Club de Programación en Python Avanzado, nuestro
Editor ofrece una variedad de funciones y recursos para ayudarte a crear y editar código de manera eficiente y efectiva.
</p>
''',unsafe_allow_html=True)
cols2 = st.columns([0.3,0.7])

with cols2[0]:
    st_lottie('https://lottie.host/bb7b964f-b151-48d4-902c-f8ff5e1ea037/H2O7NOxRVS.json',quality='low')
    #st_lottie('https://lottie.host/6af7721f-9350-4ace-8260-fbc4b3c273ad/xpkqV3aV5y.json',quality='high')

with cols2[1]:
    with open('rsc/html/Main-Banner3.html') as f:
        st.markdown(f.read(),unsafe_allow_html=True)

sac.divider(label='',align='center',icon='award')

st.markdown('''
<h4 style="padding-top: 1rem; padding-bottom: 1rem;">
Concursos.<br> Tu Fórmula para la Excelencia en el Club de Programación en Python Avanzado
</h4>
<p style="text-align: center;font-family: 'Raleway';font-size: 1rem;">
Embárcate en emocionantes desafíos y demuestra tu destreza participando en nuestros concursos regulares y eventos especiales<br>
¡Prepárate para la adrenalina de la competición y la oportunidad de destacar entre tus compañeros programadores!
</p>''' ,unsafe_allow_html=True)
cols3 = st.columns([0.7,0.3])

with cols3[0]:
    with open('rsc/html/Main-Banner4.html') as f:
        st.markdown(f.read(),unsafe_allow_html=True)

with cols3[1]:
    st_lottie('https://lottie.host/485e2469-22e7-4353-80a1-4d688f651122/xQtn67pMsN.json',quality='low')


sac.divider(label='',align='center',icon='file-earmark-check')
st.markdown('''
<h4 style="padding-top: 1rem; padding-bottom: 1rem;">
Tests<br> Desafía tus límites y evalúa tu progreso con nuestras categorías de pruebas adaptadas a tu nivel de habilidad
</h4>
<p style="text-align: center;font-family: 'Raleway';font-size: 1rem;">
¡Explora las pruebas, mide tu progreso y disfruta del emocionante viaje de mejora continua en nuestro espacio de desarrollo y desafíos en programación!
</p>''' ,unsafe_allow_html=True)
cols4 = st.columns([0.3,0.7])

with cols4[0]:
    st_lottie('https://lottie.host/81503e18-2c4d-4d1e-b84b-89b3d8352bf5/tsXAtOeFAc.json',quality='low')


with cols4[1]:
    with open('rsc/html/Main-Banner5.html') as f:
        st.markdown(f.read(),unsafe_allow_html=True)


sac.divider(label='',align='center',icon='journal-code')
st.markdown('''
<h4 style="padding-top: 1rem; padding-bottom: 1rem;">
Docs<br>Sumérgete en el conocimiento y mejora tus habilidades accediendo a nuestra documentación completa
</h4>
<p style="text-align: center;font-family: 'Raleway';font-size: 1rem;">
¡Haz de nuestra documentación tu compañera constante en tu viaje de aprendizaje y mejora continua!
</p>''' ,unsafe_allow_html=True)


cols5 = st.columns([0.7,0.3])

with cols5[0]:
    with open('rsc/html/Main-Banner6.html') as f:
        st.markdown(f.read(),unsafe_allow_html=True)

with cols5[1]:
    st_lottie('https://lottie.host/8adfe114-21e6-496e-bb67-308fb9e64e43/8JTbugAlit.json',quality='low',loop=False)




#---------------------------------#
#Galeria de Imagenes
sac.divider(label='',align='center',icon='image')
with open('rsc/html/gallery.html') as f:
    st.markdown(f.read(),unsafe_allow_html=True)








#------------------------------------- Footer ---------------------------------------------------------
sac.divider(label='',align='center',icon='share')



x = sac.tags(
    [
        sac.Tag(
            label="Contacto",
            icon="person-lines-fill",
            color="#3670a0",
            link="https://ant.design/components/tag",
            bordered=True
        ),
        sac.Tag(
            label="Instagram",
            icon="instagram",
            color="magenta",
            link="https://www.instagram.com/proyecto_cappa/",
        ),
        sac.Tag(
            label="Facebook",
            icon="facebook",
            color="geekblue",
            link="https://www.facebook.com/profile.php?id=61550249080408",
        ),
    ],
    format_func="title",
    align="center",
)

opt = sac.tabs([
sac.TabsItem(label='Información'),
sac.TabsItem(label='Contacto',icon='phone'),
sac.TabsItem(label='Política de Privacidad',icon='lock'),
sac.TabsItem(label='Términos y Condiciones',icon='file-earmark-text'),
sac.TabsItem(label='FAQ',icon='question-circle'),
],position='bottom',align='center',return_index=True)


with open('rsc/html/footer.html') as foo:
    #components.html(foo.read(),width=1600)
    st.markdown(foo.read(), unsafe_allow_html=True)
