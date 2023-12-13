import streamlit as st
import hydralit_components as hc
import base64

st.set_page_config(layout="wide", page_title='CAPPA', page_icon='🐍')
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
                  background-image: url("data:image/svg+xml,%3Csvg width='100' height='64' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cg clip-path='url(%23a)'%3E%3Cpath d='M-17 30.5C-1 22 72-4 54 13 37.9 28.2-2.5 57.5 16 55.5s72-29 104-40' stroke='%2300FDCF' stroke-width='10'/%3E%3C/g%3E%3Cdefs%3E%3CclipPath id='a'%3E%3Cpath fill='%23fff' d='M0 0h100v64H0z'/%3E%3C/clipPath%3E%3C/defs%3E%3C/svg%3E%0A");
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



over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#002B7A'}
menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Inicio',
        login_name='Admin',
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=False, #at the top or not
        sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
    )



