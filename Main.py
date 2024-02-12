import streamlit as st
import hydralit_components as hc
from streamlit_lottie import st_lottie
import streamlit_antd_components as sac
from streamlit_extras.switch_page_button import switch_page
from streamlit_calendar import calendar
import datetime


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

#---------------------------------  Variables de Sesión ---------------------------------------------------------
if 'auth_state' not in st.session_state:
    st.session_state.auth_state = False

if 'username' not in st.session_state:
    st.session_state.username = None

if 'userinfo' not in st.session_state:
    st.session_state.userinfo = None

if 'user' not in st.session_state:
    st.session_state.user = None

#---------------------------------Funciones---------------------------------------------------------



#---------------------------------Logos---------------------------------------------------------
with open('rsc/html/headlogos.html') as f:
    st.markdown(f.read(),unsafe_allow_html=True)

#---------------------------------Navigation Bar---------------------------------------------------------



menu_data = [
    {'icon': "far fa-copy", 'label':"Blog",'ttip':"Articulos e Información",'id':'Blog'},
    {'id':'About','icon':"bi bi-question-circle",'label':"FAQ",'ttip':"Preguntas Frecuentes"},
    {'id':'contact','icon':"bi bi-envelope",'label':"Contacto",'ttip':"Contáctanos"},
    ]
logname = 'Iniciar Sesión'


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

if menu_id == 'Iniciar Sesión':
    st.switch_page('pages/login.py')

if menu_id == 'Blog':
    st.switch_page('pages/docs_home.py')

if st.session_state.auth_state:
    st.switch_page('pages/app.py')
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


#Calendario de Eventos

st.header('Calendario')

mode = st.selectbox(
        "Calendar Mode:",
        (
            "daygrid",
            "timegrid",
            "timeline",
            "resource-daygrid",
            "resource-timegrid",
            "resource-timeline",
            "list",
            "multimonth",
        ),
    )

events = [
        {
            "title": "Event 1",
            "color": "#FF6C6C",
            "start": "2024-02-07",
            "end": "2024-02-07",
            "resourceId": "a",
        },
        {
            "title": "Event 2",
            "color": "#FFBD45",
            "start": "2023-10-01",
            "end": "2023-10-10",
            "resourceId": "b",
        },
        {
            "title": "Event 3",
            "color": "#FF4B4B",
            "start": "2023-09-20",
            "end": "2023-09-20",
            "resourceId": "c",
        },
        {
            "title": "Event 4",
            "color": "#FF6C6C",
            "start": "2023-09-20",
            "end": "2023-09-20",
            "resourceId": "d",
        },
        {
            "title": "Event 5",
            "color": "#FFBD45",
            "start": "2023-09-20",
            "end": "2023-09-22",
            "resourceId": "e",
        },
        {
            "title": "Event 6",
            "color": "#FF4B4B",
            "start": "2023-07-28",
            "end": "2023-07-20",
            "resourceId": "f",
        },
        {
            "title": "Event 7",
            "color": "#FF4B4B",
            "start": "2023-07-01T08:30:00",
            "end": "2023-07-01T10:30:00",
            "resourceId": "a",
        },
        {
            "title": "Event 8",
            "color": "#3D9DF3",
            "start": "2023-07-01T07:30:00",
            "end": "2023-07-01T10:30:00",
            "resourceId": "b",
        },
        {
            "title": "Event 9",
            "color": "#3DD56D",
            "start": "2023-07-02T10:40:00",
            "end": "2023-07-02T12:30:00",
            "resourceId": "c",
        },
        {
            "title": "Event 10",
            "color": "#FF4B4B",
            "start": "2023-07-15T08:30:00",
            "end": "2023-07-15T10:30:00",
            "resourceId": "d",
        },
        {
            "title": "Event 11",
            "color": "#3DD56D",
            "start": "2023-07-15T07:30:00",
            "end": "2023-07-15T10:30:00",
            "resourceId": "e",
        },
        {
            "title": "Event 12",
            "color": "#3D9DF3",
            "start": "2023-07-21T10:40:00",
            "end": "2023-07-21T12:30:00",
            "resourceId": "f",
        },
        {
            "title": "Event 13",
            "color": "#FF4B4B",
            "start": "2023-07-17T08:30:00",
            "end": "2023-07-17T10:30:00",
            "resourceId": "a",
        },
        {
            "title": "Event 14",
            "color": "#3D9DF3",
            "start": "2023-07-17T09:30:00",
            "end": "2023-07-17T11:30:00",
            "resourceId": "b",
        },
        {
            "title": "Event 15",
            "color": "#3DD56D",
            "start": "2023-07-17T10:30:00",
            "end": "2023-07-17T12:30:00",
            "resourceId": "c",
        },
        {
            "title": "Event 16",
            "color": "#FF6C6C",
            "start": "2023-07-17T13:30:00",
            "end": "2023-07-17T14:30:00",
            "resourceId": "d",
        },
        {
            "title": "Event 17",
            "color": "#FFBD45",
            "start": "2023-07-17T15:30:00",
            "end": "2023-07-17T16:30:00",
            "resourceId": "e",
        },
    ]
calendar_resources = [
        {"id": "a", "building": "Building A", "title": "Room A"},
        {"id": "b", "building": "Building A", "title": "Room B"},
        {"id": "c", "building": "Building B", "title": "Room C"},
        {"id": "d", "building": "Building B", "title": "Room D"},
        {"id": "e", "building": "Building C", "title": "Room E"},
        {"id": "f", "building": "Building C", "title": "Room F"},
    ]

calendar_options = {
        "editable": "false",
        "navLinks": "true",
        "resources": calendar_resources,
    }

if "resource" in mode:
    if mode == "resource-daygrid":
        calendar_options = {
                **calendar_options,
                "initialDate": datetime.date.today().strftime("%Y-%m-%d"),
                "initialView": "resourceDayGridDay",
                "resourceGroupField": "building",
            }
    elif mode == "resource-timeline":
        calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
                },
                "initialDate": datetime.date.today().strftime("%Y-%m-%d"),
                "initialView": "resourceTimelineDay",
                "resourceGroupField": "building",
            }
    elif mode == "resource-timegrid":
            calendar_options = {
                **calendar_options,
                "initialDate": datetime.date.today().strftime("%Y-%m-%d"),
                "initialView": "resourceTimeGridDay",
                "resourceGroupField": "building",
            }
    else:
        if mode == "daygrid":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "dayGridDay,dayGridWeek,dayGridMonth",
                },
                "initialDate": datetime.date.today().strftime("%Y-%m-%d"),
                "initialView": "dayGridMonth",
            }
        elif mode == "timegrid":
            calendar_options = {
                **calendar_options,
                "initialView": "timeGridWeek",
            }
        elif mode == "timeline":
            calendar_options = {
                **calendar_options,
                "headerToolbar": {
                    "left": "today prev,next",
                    "center": "title",
                    "right": "timelineDay,timelineWeek,timelineMonth",
                },
                "initialDate": datetime.date.today().strftime("%Y-%m-%d"),
                "initialView": "timelineMonth",
            }
        elif mode == "list":
            calendar_options = {
                **calendar_options,
                "initialDate": datetime.date.today().strftime("%Y-%m-%d"),
                "initialView": "listMonth",
            }
        elif mode == "multimonth":
            calendar_options = {
                **calendar_options,
                "initialView": "multiMonthYear",
            }

calstate = calendar(
        events=events,
        options=calendar_options,
        key=mode,
    )
#st.write(calstate)
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
