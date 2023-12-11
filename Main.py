import streamlit as st
import hydralit_components as hc

st.set_page_config(layout="wide")
st.markdown("""
<style>
body {
background-color: #e5e5f7;

}

[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}

</style>

""",unsafe_allow_html=True)




menu_data = [
    {'icon': "fa-solid fa-radar",'label':"Problemas", 'submenu':[{'id':' subid11','icon': "fa fa-paperclip", 'label':"Basicos"},{'id':'subid12','icon': "fa fa-database", 'label':"Intermedios"},{'id':'subid13','icon': "💀", 'label':"Avanzados"},{'id':'subid14','icon': "🔧", 'label':"Editor"}]},
    {'id':'contest','icon': "🏆", 'label':"Concursos"},
    {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
    {'id':'docs','icon': "far fa-copy", 'label':"Docs"},
    {'id':'code','icon': "👨‍💻", 'label':"Editor de Código"},
    {'icon': "fa-solid fa-radar",'label':"Tests", 'submenu':[{'label':"Basicos 1", 'icon': "🐛"},{'icon':'🐍','label':"Intermedios"},{'icon':'🐉','label':"Avanzados",},{'id':'subid144','icon': "🔧", 'label':"Editor" }]},
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
