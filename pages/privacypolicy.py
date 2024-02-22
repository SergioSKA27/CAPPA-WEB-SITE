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
    {'id':'privacy','icon':"bi bi-shield-lock",'label':"Políticas de Privacidad",'ttip':"Políticas de Privacidad"},
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
        first_select=10
    )

if menu_id == 'Inicio':
    st.switch_page('Main.py')

if menu_id == 'Iniciar Sesión':
    st.switch_page('pages/login.py')

if menu_id == 'Blog':
    st.switch_page('pages/docs_home.py')


st.title('🔐Políticas de Privacidad')
st.divider()


st.markdown('''


**Última actualización: Febrero 22, 2024**

Nosotros Club Académico de Programación en Python Avanzado opera el sitio web https://cappa-web-site.streamlit.app/ .

Esta página le informa sobre nuestras políticas con respecto a la recopilación, uso y divulgación de datos personales cuando utiliza nuestro Servicio y las opciones que tiene asociadas a esos datos.

Utilizamos sus datos para proporcionar y mejorar el Servicio. Al utilizar el Servicio, usted acepta la recopilación y el uso de información de acuerdo con esta política.

**Recopilación y uso de información**

Recopilamos varios tipos diferentes de información con diversos fines para proporcionar y mejorar nuestro Servicio.

**Tipos de datos recopilados**

**Datos personales**

Al utilizar nuestro Servicio, es posible que le solicitemos que nos proporcione cierta información de identificación personal que puede incluir, entre otros, su dirección de correo electrónico, nombre, número de teléfono y otros datos ("Datos personales").

**Uso de datos**

Utilizamos los datos recopilados para diversos fines, que incluyen:

- Proporcionar y mantener nuestro Servicio
- Notificarle sobre cambios en nuestro Servicio
- Permitirle participar en funciones interactivas de nuestro Servicio cuando decida hacerlo
- Proporcionar asistencia al cliente
- Recopilar análisis o información valiosa para que podamos mejorar nuestro Servicio
- Monitorizar el uso de nuestro Servicio
- Detectar, prevenir y abordar problemas técnicos

**Transferencia de datos**

Su información, incluidos los Datos personales, puede transferirse a, y mantenirse en, computadoras ubicadas fuera de su estado, provincia, país u otra jurisdicción gubernamental donde las leyes de protección de datos pueden diferir de las de su jurisdicción.

Si usted se encuentra fuera de [jurisdicción], y elige proporcionarnos información, tenga en cuenta que transferimos los datos, incluidos los Datos personales, a [jurisdicción] y que allí los procesamos.

Su consentimiento a esta Política de privacidad seguido de su envío de dicha información representa su acuerdo con dicha transferencia.

**Divulgación de datos**

**Requisitos legales**

Podemos divulgar sus Datos personales si creemos de buena fe que dicha acción es necesaria para:

- Cumplir con una obligación legal
- Proteger y defender los derechos o propiedades del Club Académico de Programación en Python Avanzado
- Prevenir o investigar posibles irregularidades relacionadas con el Servicio
- Proteger la seguridad personal de los usuarios del Servicio o del público
- Protegernos contra la responsabilidad legal

**Seguridad de los datos**

La seguridad de sus datos es importante para nosotros, pero recuerde que ningún método de transmisión a través de Internet o método de almacenamiento electrónico es 100% seguro. Si bien nos esforzamos por utilizar medios comercialmente aceptables para proteger sus Datos personales, no podemos garantizar su seguridad absoluta.

**Enlaces a otros sitios**

Nuestro Servicio puede contener enlaces a otros sitios que no son operados por nosotros. Si hace clic en un enlace de un tercero, será dirigido al sitio de ese tercero. Le recomendamos encarecidamente que revise la Política de privacidad de cada sitio que visite.

No tenemos control ni asumimos responsabilidad por el contenido, las políticas de privacidad o las prácticas de sitios o servicios de terceros.

**Cambios en esta política de privacidad**

Podemos actualizar nuestra Política de privacidad de vez en cuando. Le notificaremos cualquier cambio publicando la nueva Política de privacidad en esta página.

Le recomendamos que revise periódicamente esta Política de privacidad para cualquier cambio. Los cambios a esta Política de privacidad son efectivos cuando se publican en esta página.

**Contacto**

Si tiene alguna pregunta sobre esta Política de privacidad, puede ponerse en contacto con nosotros:

- Por correo electrónico: mac@acatlan.unam.mx
- Visitando esta página en nuestro sitio web: https://mac.acatlan.unam.mx/

''')


with open('rsc/html/footer.html') as foo:
    #components.html(foo.read(),width=1600)
    st.markdown(foo.read(), unsafe_allow_html=True)
