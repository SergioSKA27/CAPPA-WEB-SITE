import streamlit as st
import hydralit_components as hc
import pages.modules.test_edit as test_e
import numpy as np
from Clases import Autenticador, Usuario
import extra_streamlit_components as stx
from st_xatadb_connection import XataConnection
import time
import asyncio
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

xata = st.connection('xata',type=XataConnection)
st.markdown('''
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
''', unsafe_allow_html=True)

if 'auth_state' not in st.session_state:
    st.session_state.auth_state = False

if 'username' not in st.session_state:
    st.session_state.username = None

if 'userinfo' not in st.session_state:
    st.session_state.userinfo = None

if 'user' not in st.session_state:
    st.session_state.user = None


if 'logout' not in st.session_state:
    st.session_state.logout = False

async def show_message_error():
    await asyncio.sleep(1)
    st.error("Inicia Sesión para acceder a esta página")
    st.image("https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif")
    st.page_link('pages/login.py',label='Regresar a la Página de Inicio',icon='🏠')

def get_manager():
    return stx.CookieManager()

if st.session_state.logout:
    with st.spinner('Cerrando Sesión...'):
        time.sleep(2)
    st.session_state.logout = False
    st.switch_page('pages/login.py')

cookie_manager = get_manager()
auth = Autenticador(xata,cookie_manager)
valcookie = cookie_manager.get('Validado')
if auth() == False and valcookie is not None:
    auth.validate_cookie(valcookie)
    st.rerun()
#---------------------------------Navbar---------------------------------
if auth():
    #st.session_state['userinfo']
	if st.session_state.user is not None and (st.session_state.user.is_admin() or st.session_state.user.is_teacher()):
		menu_data = [
        {'icon': "bi bi-cpu",'label':"Problemas",'ttip':"Problemas de Programación",
        'submenu':[
            {'id': 'subid00','icon':'bi bi-search','label':'Todos'},
            {'id':'subid44','icon': "bi bi-journal-code", 'label':"Editor"}
        ]},
        {'id':'courses','icon': "bi bi-journal-bookmark", 'label':"Cursos",'ttip':"Cursos de Programación y Ciencia de Datos en CAPPA"},
        {'id':'docs','icon': "bi bi-file-earmark-richtext", 'label':"Blog",'ttip':"Articulos e Información",
        'submenu':[
            {'id':'doceditor','icon': "bi bi-file-earmark-richtext", 'label':"Editor" },
            {'id':'docshome','icon': "bi bi-search", 'label':"Home"}]
        },
        {'id':'code','icon': "bi bi-code-square", 'label':"Editor de Código"},
        {'icon': "bi bi-pencil-square",'label':"Tests",'id':'alltests'},
        {'id':'subid144','icon': "bi bi-card-checklist", 'label':"Editor" },
        {'id':st.session_state.user.usuario,'icon': "bi bi-person", 'label':st.session_state.user.usuario,
        'submenu':[
            {'label':"Perfil", 'icon': "bi bi-person",'id':st.session_state.user.usuario},
            {"id": "logout", "icon": "bi bi-door-open", "label": "Cerrar Sesión"},
        ]}

    ]
	elif st.session_state.user is not None:
		st.error('403 No tienes permisos para acceder a esta página')
		st.image('https://media1.tenor.com/m/e2vs6W_PzLYAAAAd/cat-side-eye.gif')
		st.page_link('pages/app.py',label='Regresar a la Página de Inicio',icon='🏠')
		st.stop()



	over_theme = {'txc_inactive': '#FFFFFF','menu_background':'#3670a0'}
	menu_id = hc.nav_bar(
        menu_definition=menu_data,
        override_theme=over_theme,
        home_name='Inicio',
        login_name=None,
        hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
        sticky_nav=True, #at the top or not
        sticky_mode='sticky', #jumpy or not-jumpy, but sticky or pinned
        first_select=60,
    )
else:
    asyncio.run(show_message_error())
    st.stop()

if menu_id == 'Inicio':
  	st.switch_page('pages/app.py')

if menu_id == 'subid00':
    st.switch_page('pages/problems_home.py')

if menu_id == 'subid44':
    st.switch_page('pages/problems_editor.py')

if menu_id == 'code':
	st.switch_page('pages/code_editor.py')

if menu_id == 'doceditor':
    st.switch_page('pages/doc_editor.py')

if menu_id == 'docshome':
	st.switch_page('pages/docs_home.py')

if  menu_id == 'courses':
    st.switch_page('pages/CoursesHome.py')


if menu_id == 'logout':
    st.session_state.auth_state = False
    st.session_state.userinfo = None
    st.session_state.user = None
    st.session_state.username = None
    cookie_manager.delete('Validado')
    st.session_state.logout = True

if st.session_state.user is not None and menu_id == st.session_state.user.usuario:
        if 'query' not in st.session_state:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        else:
            st.session_state.query = {'Table':'Usuario','id':st.session_state.user.key}
        st.switch_page('pages/profile_render.py')

#------------------------------------- body ---------------------------------------------------------
st.title('Editor de tests 📝')

#st.text(st.session_state)
test =st.text_input('Ingrese el nombre del test',placeholder='Test uno')
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
    correcta = st.toggle('Respuesta correcta',key='ans'+str(i)+str(st.session_state['qnum']))
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
    correcta = st.toggle('Respuesta correcta',key='ans'+str(i)+str(st.session_state['qnum']))
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
