import streamlit as st
import streamlit.components.v1 as components
import base64
from streamlit_extras.echo_expander import echo_expander
import hydralit_components as hc
from streamlit_extras.switch_page_button import switch_page
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from st_keyup import st_keyup
from streamlit_toggle import st_toggle_switch


#Types of questions
#multiple, selction, checkbox,code, order


class test:
  def __init__(self,test_name):
    self.test_name = test_name
    self.qnumber = 0
    self.questions_data = {}

  def add_question(self):
    t = st.selectbox('Seleccione el tipo de pregunta que desea agregar',('opcion multiple','selccion multiple','entrada libre','codigo','ordenacion'),key='s'+str(self.qnumber))

    if t == 'opcion multiple':
      st.write('## Ingrese el texto de la pregunta '+str(self.qnumber))
      question_text = st.text_area('Texto de la pregunta','Pregunta?', height=100,key='text'+str(self.qnumber))

      col =st.columns(5)
      answ_num = col[0].number_input('**Ingrese el numero de respuestas**', min_value=1, max_value=5,key='num'+str(self.qnumber))
      ans = []
      correct_ans = 0
      for i in range(answ_num):
        st.write('Ingrese el texto de la respuesta '+str(i+1))
        correcta = st_toggle_switch('Respuesta correcta',key='ans'+str(i)+str(self.qnumber))
        if correcta:
          correct_ans = i
        answer_text = st.text_area('Texto de la respuesta','Respuesta '+str(i+1), height=50,key='answ'+str(i)+str(self.qnumber))
        ans.append(answer_text)


      self.questions_data[self.qnumber] = {
        'question_text':question_text,
        'answers':ans,
        'correct_answer':correct_ans,
        'qtype': 'multiple'
      }

      self.preview_question(self.qnumber)

      self.qnumber += 1

    if t == 'selccion multiple':
      st.write('## Ingrese el texto de la pregunta '+str(self.qnumber))
      question_text = st.text_area('Texto de la pregunta','Pregunta?', height=100,key='text'+str(self.qnumber))

      col =st.columns(5)
      answ_num = col[0].number_input('**Ingrese el numero de respuestas**', min_value=1, max_value=5,key='num'+str(self.qnumber))
      ans = []
      correct_ans = []
      for i in range(answ_num):
        st.write('Ingrese el texto de la respuesta '+str(i+1))
        correcta = st_toggle_switch('Respuesta correcta',key='ans'+str(i)+str(self.qnumber))
        if correcta:
          correct_ans.append(i)
        answer_text = st.text_area('Texto de la respuesta','Respuesta '+str(i+1), height=50,key='answ'+str(i)+str(self.qnumber))
        ans.append(answer_text)


      self.questions_data[self.qnumber] = {
        'question_text':question_text,
        'answers':ans,
        'correct_answer':correct_ans,
        'qtype': 'checkbox'
      }

      self.preview_question(self.qnumber)

      self.qnumber += 1




  def preview_question(self,qnumber):
    st.write('# Preview')

    st.write(self.questions_data[qnumber]['question_text'])
    if self.questions_data[qnumber]['qtype'] == 'multiple':
      st.write('Selecciona la respuesta correcta')
      st.radio('**Respuesta correcta**',options=self.questions_data[qnumber]['answers'],label_visibility='collapsed',key='radio'+str(qnumber))
      st.write('Respuesta correcta: ', self.questions_data[qnumber]['correct_answer'])
    if self.questions_data[qnumber]['qtype'] == 'checkbox':
      st.write('Selecciona la respuesta correcta')
      chcks = []
      for i in range(len(self.questions_data[qnumber]['answers'])):
        chcks.append(st.checkbox(self.questions_data[qnumber]['answers'][i],key='chck'+str(i)+str(qnumber)))

      st.write('Respuestas correcta: ', self.questions_data[qnumber]['correct_answer'])
