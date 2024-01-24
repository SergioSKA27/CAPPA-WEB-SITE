import streamlit as st
import hydralit_components as hc
from streamlit_extras.switch_page_button import switch_page
import pages.modules.test_edit as test_e
from streamlit_toggle import st_toggle_switch
import numpy as np
#Autor: Sergio Lopez



#Autor: Sergio Lopez

#--------------------------------------------- page config ---------------------------------------------
#basic page configuration
st.set_page_config(
    page_title='CAPA',
    page_icon="rsc/Logos/LOGO_CAPPA.jpg",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': """# Web Site Club de Algoritmia Avanzada en Python.
                        Todos los derechos reservados 2023, CAPA."""
    }
)

st.markdown('''
<style>
[data-testid="collapsedControl"] {
        display: none
    }

#MainMenu, header, footer {visibility: hidden;}
.st-emotion-cache-152jn8i {
  position: absolute;
  background: rgb(244, 235, 232);
  color: rgb(49, 51, 63);
  inset: 0px;
    top: 0px;
  overflow: hidden;
  top: 0px;
}
.st-emotion-cache-z5fcl4 {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    padding-bottom: 0;
  }
</style>
''', unsafe_allow_html=True)



if 'auth_state' not in st.session_state or st.session_state['auth_state'] == False or st.session_state['userinfo']['rol'] == 'Estudiante':
    #Si no esta autenticado o es estudiante, redirigir a la pagina de Inicio
    switch_page('Main')

#---------------------------------Navbar---------------------------------
if 'auth_state' not  in st.session_state:
    menu_data = [
    {'icon': "far fa-copy", 'label':"Docs",'ttip':"Documentación de la Plataforma"},
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
            {'id':' subid11','icon': "bi bi-flower1", 'label':"Basicos"},
            {'id':'subid22','icon': "fa fa-paperclip", 'label':"Intermedios"},
            {'id':'subid33','icon': "bi bi-emoji-dizzy", 'label':"Avanzados"},
            {'id':'subid44','icon': "bi bi-gear", 'label':"Editor"}
        ]},
        {'id':'contest','icon': "bi bi-trophy", 'label':"Concursos"},
        {'icon': "bi bi-graph-up", 'label':"Analisis de Datos",'ttip':"Herramientas de Analisis de Datos"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Docs",'ttip':"Articulos e Información",
        'submenu':[
            {'id':'subid55','icon': "bi bi-gear", 'label':"Editor" }]
        },
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests", 'submenu':[
            {'label':"Todos", 'icon': "bi bi-search",'id':'alltests'},
            {'label':"Basicos 1", 'icon': "🐛"},
            {'icon':'🐍','label':"Intermedios"},
            {'icon':'🐉','label':"Avanzados",},
            {'id':'subid144','icon': "bi bi-gear", 'label':"Editor" }]},
        {'id':'logout','icon': "bi bi-door-open", 'label':"Logout"},#no tooltip message
    ]
    else:
        menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':' subid11','icon': "bi bi-flower1", 'label':"Basicos"},
            {'id':'subid22','icon': "fa fa-paperclip", 'label':"Intermedios"},
            {'id':'subid33','icon': "bi bi-emoji-dizzy", 'label':"Avanzados"},
        ]},
        {'id':'contest','icon': "bi bi-trophy", 'label':"Concursos"},
        {'icon': "bi bi-graph-up", 'label':"Analisis de Datos",'ttip':"Herramientas de Analisis de Datos"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Docs",'ttip':"Articulos e Información"},
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests", 'submenu':[
            {'label':"Todos", 'icon': "bi bi-search",'label':'alltests'},
            {'label':"Basicos", 'icon': "🐛"},
            {'icon':'🐍','label':"Intermedios"},
            {'icon':'🐉','label':"Avanzados",}]},
        {'id':'logout','icon': "bi bi-door-open", 'label':"Logout"},#no tooltip message
    ]
    logname = st.session_state['userinfo']['username']

over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Inicio',
        login_name=st.session_state['userinfo']['username'],
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
        first_select=60,
    )


if menu_id == 'Inicio':
  switch_page('Main')

if menu_id == 'subid00':
    switch_page('problems_home')

if menu_id == 'subid44':
    switch_page('problems_editor')

if menu_id == 'code':
    switch_page('code_editor')



if menu_id == 'logout':
    st.session_state.pop('auth_state')
    st.session_state.pop('userinfo')
    st.session_state.pop('username')
    switch_page('login')

if 'userinfo' in st.session_state:
    if menu_id == st.session_state['userinfo']['username']:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state['username']}
        switch_page('profile_render')

#------------------------------------- body ---------------------------------------------------------
st.title('Editor de tests 📝')

#st.text(st.session_state)
test =st.text_input('Ingrese el nombre del test','Test uno')
t = test_e.test(test)
if 'test' not in st.session_state:
    st.session_state['test']= t
else:
    if st.session_state['test'].test_name != test:
        st.session_state['test'].test_name = test

cols = st.columns([.8,.2])


with cols[0]:
    level = st.slider('Nivel del test',1,10)

if 'level-test' not in st.session_state:
  st.session_state['level-test'] = level
else:
  st.session_state['level-test'] = level


if 'qnum' not in st.session_state:
  st.session_state['qnum'] = 0

if 'questions_data' not in st.session_state:
  st.session_state['questions_data'] = []





edcols = st.columns([.5,.5])
with edcols[1]:
    t = st.selectbox('Seleccione el tipo de pregunta que desea agregar',('opcion multiple','selccion multiple','entrada libre','codigo','ordenacion'),key='s'+str(st.session_state['qnum']))

if t == 'opcion multiple':
  st.write('## Ingrese el texto de la pregunta '+str(st.session_state['qnum']+1))
  question_text = st.text_area('Texto de la pregunta','Pregunta?', height=100,key='text'+str(st.session_state['qnum']))
  st.warning('**Nota:** Seleccione unicamente una respuesta correcta')
  col =st.columns(3)
  answ_num = col[0].number_input('**Ingrese el numero de respuestas**', min_value=1, max_value=5,key='num'+str(st.session_state['qnum']))
  ans = []
  correct_ans = 0
  for i in range(answ_num):
    st.write('Ingrese el texto de la respuesta '+str(i+1))
    correcta = st_toggle_switch('Respuesta correcta',key='ans'+str(i)+str(st.session_state['qnum']))
    if correcta:
      correct_ans = i
    answer_text = st.text_area('Texto de la respuesta','Respuesta '+str(i+1), height=50,key='answ'+str(i)+str(st.session_state['qnum']))
    ans.append(answer_text)
  quest= {
    'question_text':question_text,
    'answers':np.random.permutation(np.array(ans)),
    'correct_answer':correct_ans,
    'qtype': 'multiple'
    }


if t == 'selccion multiple':
  st.write('## Ingrese el texto de la pregunta '+str(st.session_state['qnum']))
  question_text = st.text_area('Texto de la pregunta','Pregunta?', height=100,key='text'+str(st.session_state['qnum']))
  col =st.columns(3)
  answ_num = col[0].number_input('**Ingrese el numero de respuestas**', min_value=1, max_value=5,key='num'+str(st.session_state['qnum']))
  ans = []
  correct_ans = []
  for i in range(answ_num):
    st.write('Ingrese el texto de la respuesta '+str(i+1))
    correcta = st_toggle_switch('Respuesta correcta',key='ans'+str(i)+str(st.session_state['qnum']))
    if correcta:
      correct_ans.append(i)
    answer_text = st.text_area('Texto de la respuesta','Respuesta '+str(i+1), height=50,key='answ'+str(i)+str(st.session_state['qnum']))
    ans.append(answer_text)
  quest = {
    'question_text':question_text,
    'answers':ans,
    'correct_answer':correct_ans,
    'qtype': 'checkbox'
    }

if t == 'ordenacion':
  st.write('## Ingrese el texto de la pregunta '+str(st.session_state['qnum']))
  question_text = st.text_area('Texto de la pregunta','Pregunta?', height=100,key='text'+str(st.session_state['qnum']))
  col =st.columns(3)
  answ_num = col[0].number_input('**Ingrese el numero de respuestas**', min_value=1, max_value=100,key='num'+str(st.session_state['qnum']))
  ans = []
  correct_ans = []
  st.write('Ingrese las repuestas en orden ')
  for i in range(answ_num):
    st.write('Ingrese el texto de la respuesta '+str(i+1))
    answer_text = st.text_area('Texto de la respuesta','Respuesta '+str(i+1), height=50,key='answ'+str(i)+str(st.session_state['qnum']))
    ans.append(answer_text)
  quest = {
    'question_text':question_text,
    'answers':ans,
    'correct_answer':ans,
    'qtype': 'order'
    }

if t == 'entrada libre':
  st.write('## Ingrese el texto de la pregunta '+str(st.session_state['qnum']))
  question_text = st.text_area('Texto de la pregunta','Pregunta?', height=100,key='text'+str(st.session_state['qnum']))
  col =st.columns(3)
  leftoev = st.checkbox('Dejar para evaluar')
  answ = st.text_area('Ingresa la respuesta exacta(o una expresion regular)',r'\b{palabra|python}\b', height=100,key='text'+str(st.session_state['qnum']+1))

  if leftoev:
    quest = {
    'question_text':question_text,
    'answers':'',
    'correct_answer':'left to evalute',
    'qtype': 'text'
    }
  else:
    quest = {
    'question_text':question_text,
    'answers':answ,
    'correct_answer':answ,
    'qtype': 'text'
    }

if st.button('Añadir pregunta'):
    st.session_state['questions_data'].append(quest)
    st.session_state['qnum'] += 1
    st.rerun()

st.write(st.session_state['questions_data'])
st.write('# Preview')
for i in range(st.session_state['qnum']):
    st.divider()
    st.write('## Pregunta ' +str(i+1))
    st.write(st.session_state['questions_data'][i]['question_text'])
    if st.session_state['questions_data'][i]['qtype'] == 'multiple':
        st.write('Selecciona la respuesta correcta')
        st.radio('**Respuesta correcta**',options=st.session_state['questions_data'][i]['answers'],label_visibility='collapsed',key='radio'+str(i))
        st.write('Respuesta correcta: ', st.session_state['questions_data'][i]['correct_answer'])
    if st.session_state['questions_data'][i]['qtype'] == 'checkbox':
        st.write('Selecciona la respuesta correcta')
        chcks = []
        for t in range(len(st.session_state['questions_data'][i]['answers'])):
            chcks.append(st.checkbox(st.session_state['questions_data'][i]['answers'][t],key='chck'+str(t)+str(i)))
        st.write('Respuestas correctas: ', st.session_state['questions_data'][i]['correct_answer'])

    if st.session_state['questions_data'][i]['qtype'] == 'text':
        st.write('Ingresa la respuesta')
        st.text_area('Respuesta', height=50,key='text'+str(i))
        st.write('Respuestas correctas: ', st.session_state['questions_data'][i]['correct_answer'])

    if st.session_state['questions_data'][i]['qtype'] == 'order':
        st.write('Ingresa las respuestas en orden')
        st.multiselect('Respuestas',options=st.session_state['questions_data'][i]['answers'],key='mult'+str(i))
        st.write('Respuestas correctas(en orden): ', st.session_state['questions_data'][i]['correct_answer'])

    if st.button('Eliminar pregunta',key='del'+str(i)):
        del st.session_state['questions_data'][i]
        st.session_state['qnum'] -= 1
        st.rerun()



#---------------------------------Footer---------------------------------
with open('rsc/html/minimal_footer.html') as f:
    st.markdown(f.read(), unsafe_allow_html=True)
