import streamlit as st
import hydralit_components as hc
import base64
from streamlit_lottie import st_lottie
import streamlit_antd_components as sac

st.set_page_config(layout="wide", page_title='CAPPA', page_icon='rsc/Logos/LOGO_CAPPA.jpg')
st.markdown("""
<style>
body {
background-color: #e5e5f7;

}

[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}

.st-emotion-cache-z5fcl4 {
    padding-left: 1rem;
    padding-right: 1rem;
}
.st-emotion-cache-z5fcl4 {
  width: 100%;
  padding: 0rem 1rem 1rem;
    padding-right: 1rem;
    padding-left: 1rem;
  min-width: auto;
  max-width: initial;
}

</style>

""",unsafe_allow_html=True)


#---------------------------------#
#Functions
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


def show_logos():
    """
    The `show_logos` function displays the Python logo and the name of a Python club using SVG code and a CSS file.
    """


    columns1,col2,col3 = st.columns([0.2,0.6,0.2])

    with col2:
        st.markdown('''
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
            .fancy {
              position: relative;
              white-space: nowrap;

              &:after {
                --deco-height: 0.3125em;
                content: "";
                position: absolute;
                left: 0;
                right: 0;
                bottom: calc(var(--deco-height) * -0.625);
                height: var(--deco-height);
                background-image: url("data:image/svg+xml,%3Csvg width='100' height='64' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cg clip-path='url(%23a)'%3E%3Cpath d='M-17 30.5C-1 22 72-4 54 13 37.9 28.2-2.5 57.5 16 55.5s72-29 104-40' stroke='%233670a0' stroke-width='10'/%3E%3C/g%3E%3Cdefs%3E%3CclipPath id='a'%3E%3Cpath fill='%23fff' d='M0 0h100v64H0z'/%3E%3C/clipPath%3E%3C/defs%3E%3C/svg%3E%0A");
                background-size: auto 100%;
                background-repeat: round;
                background-position: 0em;
              }
            }

        </style>

        <div style="text-align: center;">
            <h2 style="font-family: 'Bebas Neue';font-size: 50px;">
            <span class="fancy">Club de Programación en Python Avanzado</span>
            </h2>

        </div>

        ''',unsafe_allow_html=True)
        #st.write('## Club de Algoritmia en Python Avanzado' )
    with columns1:
        st.image('rsc/Logos/FESA_LOGO.png',use_column_width=True)
        #file_ = open("rsc/Logos/FESA_LOGO.png",'rb')
        #contents = file_.read()
        #data_url = base64.b64encode(contents).decode("utf-8")
        #file_.close()
        #st.markdown(
        #        f'<div style="text-align: center;"><img src="data:image/gif;base64,{data_url}" alt="logo-fes-mac"></div>',
        #        unsafe_allow_html=True,
        #        )
    with col3:
        pythonlogo()


show_logos()
#---------------------------------#
#Navigation Bar

menu_data = [
    {'icon': "💻",'label':"Problemas",
    'submenu':[
    {'id': 'subid00','icon':'🔍','label':'Todos'},
    {'id':' subid11','icon': "fa fa-paperclip", 'label':"Basicos"},
    {'id':'subid22','icon': "fa fa-database", 'label':"Intermedios"},
    {'id':'subid33','icon': "💀", 'label':"Avanzados"},
    {'id':'subid44','icon': "🔧", 'label':"Editor"}
    ]},
    {'id':'contest','icon': "🏆", 'label':"Concursos"},
    {'icon': "📊", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
    {'id':'docs','icon': "📚", 'label':"Docs"},
    {'id':'code','icon': "👨‍💻", 'label':"Editor de Código"},
    {'icon': "📝",'label':"Tests", 'submenu':[
    {'label':"Basicos 1", 'icon': "🐛"},
    {'icon':'🐍','label':"Intermedios"},
    {'icon':'🐉','label':"Avanzados",},
    {'id':'subid144','icon': "🔧", 'label':"Editor" }]},
    {'id':'About','icon':"❓",'label':"FAQ"},
    {'id':'contact','icon':"📩",'label':"Contacto"},
    {'id':'logout','icon': "🚪", 'label':"Logout"},#no tooltip message

    ]



over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Inicio',
        login_name='Admin',
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=False, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
    )
menu_id
#---------------------------------#
#Welcome Message
cols0 = st.columns([0.6,0.4])
with cols0[0]:
    with open('rsc/html/Main-Banner1.html') as f:
        st.markdown(f.read(), unsafe_allow_html=True)

with cols0[1]:
    st_lottie('https://lottie.host/140704e5-be12-4599-9a87-c945ab953df4/7qF25McNau.json',loop=False,quality='high')




sac.divider(label='',align='center',dashed=True)
#---------------------------------#
#Caracteristicas del sitio

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
sac.divider(label='Características',align='center',bold=True,icon='rocket',)
st.markdown('''
<h4>Explora Desaf&iacute;os</h4>
<p style="text-align: center;font-family: cursive;font-size: 1rem;">
    Bienvenido a nuestra secci&oacute;n de Desaf&iacute;os, dise&ntilde;ada para satisfacer todas tus inquietudes de programaci&oacute;n.
    Aqu&iacute;, encontrar&aacute;s una variedad de problemas adaptados a todos los niveles de habilidad, desde principiantes
    hasta expertos. Nuestra plataforma te invita a sumergirte en el emocionante mundo de la resoluci&oacute;n de problemas de
    programaci&oacute;n.<br>
    <span class="fancy">
    &iexcl;Aqu&iacute; est&aacute; lo que te ofrecemos!
    </span>
</p>
''',unsafe_allow_html=True)
cols1 = st.columns([0.7,0.3])

with cols1[0]:
    with open('rsc/html/Main-Banner2.html') as f:
        st.markdown(f.read(),unsafe_allow_html=True)

somelottie ='https://lottie.host/c41a8ef4-fc04-4219-a774-163c87c6c677/2q1ZVNlPDJ.json'
with cols1[1]:
    st_lottie('https://lottie.host/5295a4fe-7a58-4245-a71a-5be321a45b6a/IdGdn1WOgB.json',quality='high')
    st_lottie('https://lottie.host/20ba4be7-6b85-4613-a152-d77cb8b1a787/vQygOL7QiX.json',quality='high')
#------------------------------------- Footer ---------------------------------------------------------
sac.divider(label='Redes Sociales',align='center',bold=True,icon='share')
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

with open('rsc/html/footer.html') as foo:
    #components.html(foo.read(),width=1600)
    st.markdown(foo.read(), unsafe_allow_html=True)

x = '''
¡Por supuesto! Aquí tienes una descripción para tu página principal basada en el contenido:

---

¡Bienvenido a nuestro Espacio de Desarrollo y Desafíos en Programación! Explora un mundo de posibilidades con nuestras emocionantes funciones y recursos.

**Menú de Navegación:**
- **Problemas:** Encuentra desafíos para todos los niveles, desde los más básicos hasta los más avanzados. Incluso puedes editar y resolver problemas en nuestro Editor integrado.
  - Todos los Problemas
  - Problemas Básicos
  - Problemas Intermedios
  - Problemas Avanzados
  - Editor de Código

- **Concursos:** ¡Demuestra tus habilidades compitiendo en nuestros concursos y desafíos especiales!

- **Dashboard:** Obtén información valiosa sobre tu progreso y desempeño en un vistazo.

- **Docs:** Accede a nuestra documentación completa para aprender y mejorar tus habilidades.

- **Editor de Código:** Experimenta y crea con nuestro editor de código interactivo.

- **Tests:** Desafíate a ti mismo con una variedad de pruebas clasificadas por dificultad.
  - Pruebas Básicas
  - Pruebas Intermedias
  - Pruebas Avanzadas
  - Editor de Pruebas

- **FAQ:** Encuentra respuestas a preguntas frecuentes y descubre más sobre nuestra plataforma.

- **Contacto:** ¿Necesitas ayuda o tienes comentarios? Contáctanos, ¡estamos aquí para ayudar!

- **Logout:** Cierra sesión cuando hayas terminado tus sesiones.

Explora, aprende y desafía tus límites en nuestro club. ¡Es hora de codear con pasión y creatividad!

---

Esta descripción destaca las diversas secciones y características disponibles en tu página principal, invitando a los usuarios a sumergirse en el mundo de la programación y los desafíos que tu plataforma ofrece. ¡Espero que encuentres útil esta descripción!
'''
