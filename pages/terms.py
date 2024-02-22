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
    {'id':'terms','icon':"bi bi-file-earmark-text",'label':"Términos y Condiciones",'ttip':"Términos y Condiciones"},
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


st.title('Términos y Condiciones de Uso')


st.markdown('''
Última actualización: Febrero 22, 2024

Por favor, lea estos Términos y Condiciones de Uso ("Términos", "Términos y Condiciones") cuidadosamente antes de
utilizar el sitio web https://cappa-web-site.streamlit.app/ (en adelante, el "Servicio") operado por Club Académico de
Programación en Python Avanzado ("nosotros", "nos" o "nuestro").

Su acceso y uso del Servicio están condicionados a su aceptación y cumplimiento de estos Términos. Estos Términos se
aplican a todos los visitantes, usuarios y otras personas que accedan o utilicen el Servicio.

Al acceder o utilizar el Servicio, usted acepta estar sujeto a estos Términos. Si no está de acuerdo con alguna parte
de los términos, entonces no podrá acceder al Servicio.

**Cuentas**

Cuando crea una cuenta con nosotros, debe proporcionarnos información precisa, completa y actualizada en todo momento.
El incumplimiento de esta obligación constituye una violación de los Términos, que puede resultar en la terminación
inmediata de su cuenta en nuestro Servicio.

Usted es responsable de salvaguardar la contraseña que utiliza para acceder al Servicio y de cualquier actividad o
acción realizada bajo su contraseña, ya sea con nuestra contraseña o con una contraseña de un servicio de terceros.

Usted acepta no divulgar su contraseña a terceros. Debe notificarnos inmediatamente después de tomar conocimiento de
cualquier violación de seguridad o uso no autorizado de su cuenta.

**Enlaces a otros sitios web**

Nuestro Servicio puede contener enlaces a sitios web de terceros o servicios que no son propiedad ni están controlados
por el Club Académico de Programación en Python Avanzado.

El Club Académico de Programación en Python Avanzado no tiene control ni asume responsabilidad alguna por el contenido,
las políticas de privacidad o las prácticas de sitios web o servicios de terceros. Además, reconoce y acepta que el Club
Académico de Programación en Python Avanzado no será responsable, directa o indirectamente, por cualquier daño o pérdida
causada o supuestamente causada por o en conexión con el uso o la dependencia de dicho contenido, bienes o servicios
disponibles en o a través de tales sitios web o servicios.

Le recomendamos encarecidamente que lea los términos y condiciones y las políticas de privacidad de cualquier sitio web
o servicio de terceros que visite.

**Terminación**

Podemos terminar o suspender su cuenta inmediatamente, sin previo aviso ni responsabilidad, por cualquier motivo,
incluido, entre otros, si usted incumple los Términos.

Al terminar su cuenta, su derecho a usar el Servicio cesará inmediatamente. Si desea terminar su cuenta, simplemente
puede dejar de usar el Servicio.

**Limitación de responsabilidad**

En ningún caso el Club Académico de Programación en Python Avanzado, ni sus directores, empleados, socios, agentes,
proveedores o afiliados, serán responsables de ningún daño indirecto, incidental, especial, consecuente o punitivo,
incluidos, entre otros, la pérdida de beneficios, datos, uso, buena voluntad u otras pérdidas intangibles, que surjan de

(i) su acceso o uso o incapacidad para acceder o usar el Servicio

(ii) cualquier conducta o contenido de terceros en el Servicio

(iii) cualquier contenido obtenido del Servicio

(iv) acceso no autorizado, uso o alteración de sus transmisiones o contenido, ya sea que se base en garantía,
contrato, agravio (incluida negligencia) o cualquier otra teoría legal, independientemente de si hemos sido
informados o no de la posibilidad de tales daños, e incluso si se encuentra un remedio limitado en su defecto.

**Ley aplicable**

Estos Términos se regirán e interpretarán de acuerdo con las leyes de [jurisdicción], sin tener en cuenta sus
disposiciones sobre conflictos de leyes.

Nuestra falta de hacer cumplir cualquier derecho o disposición de estos Términos no se considerará una renuncia a
esos derechos. Si alguna disposición de estos Términos es considerada inválida o inaplicable por un tribunal, las
disposiciones restantes de estos Términos seguirán vigentes. Estos Términos constituyen el acuerdo completo entre
nosotros con respecto a nuestro Servicio, y reemplazan y reemplazan cualquier acuerdo anterior que podamos tener
entre nosotros con respecto al Servicio.

**Cambios**

Nos reservamos el derecho, a nuestra sola discreción, de modificar o reemplazar estos Términos en cualquier momento
. Si una revisión es importante, intentaremos proporcionar al menos 30 días de aviso previo antes de que los nuevos
términos entren en vigencia. Lo que constituye un cambio material se determinará a nuestra sola discreción.

Al continuar accediendo o utilizando nuestro Servicio después de que esas revisiones entren en vigencia, usted
acepta estar sujeto a los términos revisados. Si no está de acuerdo con los nuevos términos, por favor deje de usar el Servicio.

**Contacto**

Si tiene alguna pregunta sobre estos Términos, por favor contáctenos:

- Por correo electrónico: mac@acatlan.unam.mx
- Visitando esta página en nuestro sitio web: https://mac.acatlan.unam.mx/

''')


with open('rsc/html/footer.html') as foo:
    #components.html(foo.read(),width=1600)
    st.markdown(foo.read(), unsafe_allow_html=True)
