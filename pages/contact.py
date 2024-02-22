import streamlit as st
import hydralit_components as hc



st.set_page_config(layout="wide", page_title='CAPPA', page_icon='rsc/Logos/LOGO_CAPPA.jpg', initial_sidebar_state='collapsed')
st.markdown("""
<style>
[data-testid="collapsedControl"] {
        display: none
    }
#MainMenu, header, footer {visibility: hidden;}
.appview-container .main .block-container
{
    padding-top: 0px;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-bottom: 0px;
}
</style>
""",unsafe_allow_html=True)



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
        sticky_nav=True, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
        first_select=30
    )

if menu_id == 'Inicio':
    st.switch_page('Main.py')

if menu_id == 'Iniciar Sesión':
    st.switch_page('pages/login.py')

if menu_id == 'Blog':
    st.switch_page('pages/docs_home.py')


st.title('📍Información de Contacto')
st.divider()


st.markdown('''

Si tiene alguna pregunta, comentario o inquietud sobre nuestros servicios, estaremos encantados de ayudarle.
A continuación, encontrará diferentes formas de ponerse en contacto con nosotros:

**Correo Electrónico:**

Puede enviarnos un correo electrónico a la siguiente dirección:

- **Correo electrónico:** [mac@acatlan.unam.mx](mailto:mac@acatlan.unam.mx)

Nos esforzamos por responder a todos los correos electrónicos en un plazo de [número de días] días hábiles.
Tenga en cuenta que los tiempos de respuesta pueden variar según el volumen de consultas recibidas.

**Sitio Web:**

También puede visitar nuestra página de contacto en nuestro sitio web oficial. Allí encontrará un formulario de contacto
que puede utilizar para enviarnos sus consultas directamente desde nuestro sitio web. Nuestra página de contacto se
encuentra en el siguiente enlace:

- **Página de contacto:** [https://mac.acatlan.unam.mx/](https://mac.acatlan.unam.mx/)

**Horario de Atención:**

Nuestro horario de atención es de 11 AM a 5 PM. Durante este tiempo, nos esforzamos por responder rápidamente
a todas las consultas recibidas. Si su consulta se realiza fuera de nuestro horario de atención, le responderemos en
el siguiente día hábil.

**Redes Sociales:**

También puede seguirnos en nuestras redes sociales para obtener noticias, actualizaciones y ponerse en contacto con
nosotros de manera informal. Estamos activos en las siguientes plataformas:

- [Instagram](https://www.instagram.com/proyecto_cappa/)
- [Facebook](https://www.facebook.com/profile.php?id=61550249080408)

**Ubicación:**

Si prefiere comunicarse en persona o enviar correspondencia por correo postal, nuestra dirección física es:

**Facultad de Estudios Superiores Acatlán, Programa de Matemáticas Aplicadas y Computación.**

Avenida Alcanfores y San Juan Totoltepec s/n, Sta Cruz Acatlán, 53150 Naucalpan de Juárez, Méx.
''')


with open('rsc/html/footer.html') as foo:
    #components.html(foo.read(),width=1600)
    st.markdown(foo.read(), unsafe_allow_html=True)
