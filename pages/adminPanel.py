import streamlit as st
from st_xatadb_connection import XataConnection
import pandas as pd
import plotly.graph_objects as go
from st_tiny_editor import  tiny_editor
import datetime

xata = st.connection('xata',type=XataConnection)



def get_users():
    try:
        users = xata.query('Usuario',{"columns": [
        "username",
        "password",
        "correo",
        "rol",
        "verificado",
        "rango",
        "score",
        "nombre_completo",
        "fechaNacimiento",
        "sociaLinks",
        "feed"
    ]})
        return users
    except Exception as e:
        st.error(f'Error: {e}')
        return None


def get_cursos():
    try:
        cursos = xata.query("Curso", {
    "columns": [
        "nombre",
        "capacidad",
        "publico",
        "secciones",
        "bio_curso",
        "inscritos"
    ]
    })
        return cursos
    except Exception as e:
        st.error(f'Error: {e}')
        return None


def add_anuncio(anuncio):
    try:
        xata.insert("Anuncio",anuncio)
        st.success('Anuncio agregado')
        st.balloons()
    except Exception as e:
        st.error(f'Error: {e}')
        return None
def update_user(username,update):
    try:
        st.session_state.all_users = get_users()
    except Exception as e:
        st.error(f'Error: {e}')
        return None



if 'user' not in st.session_state or st.session_state.user.is_admin() == False:
    st.switch_page('pages/app.py')

st.page_link('pages/app.py',label='Salir',icon='🚪')
st.title('Panel de Administración')
if 'all_users' not in st.session_state:
    st.session_state.all_users = get_users()

if 'all_cursos' not in st.session_state:
    st.session_state.all_cursos = get_cursos()

st.write('Bienvenido al panel de administración')


st.subheader('Anuncios')
_,anunciocol = st.columns([.8,.2])

if anunciocol.toggle('Agregar Anuncio'):
    with st.form(key='anuncioform'):
        titulo = st.text_input('Título')
        vencimiento = st.date_input('Vencimiento')
        hora = st.time_input('Hora')
        target = st.selectbox('Destino',['Pagina Principal','Curso','Main'],help='Pagina Principal: Aparecerá en la pagina principal,Curso: Aparecerá en la pagina del curso,Main: Aparecerá en la landing page')
        curso = st.selectbox('Seleciona un Curso',[','.join([d['nombre'], d['id']]) for d in st.session_state.all_cursos['records']],help='Solo si el destino es Curso')
        contenido = tiny_editor(st.secrets['TINY_API_KEY'],
                            height=600,
                            key='welcomeeditor',
                            toolbar = 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | emoticons charmap | removeformat',
                            plugins = [
                              "advlist", "anchor", "autolink", "charmap", "code",
                              "help", "image", "insertdatetime", "link", "lists", "media",
                              "preview", "searchreplace", "table", "visualblocks", "accordion",'emoticons',
                              ]
                            )
        accion = st.selectbox('Acción',['Agregar','Preview'],index=1)

        if st.form_submit_button('Aplicar',use_container_width=True):
            if accion == 'Preview'and contenido is not None:
                st.write(contenido,unsafe_allow_html=True)
            else:
                if titulo == "" or contenido == "" or contenido is None:
                    st.error('El título y el contenido no pueden estar vacíos')
                else:
                    valstargets = {'Pagina Principal':'app','Curso':'curso','Main':'main'}
                    data = {
                        'titulo':titulo,
                        'vencimiento':datetime.datetime.combine(vencimiento,hora).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        'target':valstargets[target],
                        'content': contenido,

                    }
                    if target == 'Curso':
                        data['curso'] = curso.split(',')[1]

                    add_anuncio(data)

st.subheader('Usuarios')
st.divider()
df = pd.DataFrame(st.session_state.all_users['records'])


metricscols = st.columns(6)

metricscols[0].metric('Usuarios',df.shape[0])
metricscols[1].metric('Usuarios Verificados',df[df['verificado'] == True].shape[0])
metricscols[2].metric('Profesores',df[df['rol'] == 'Profesor'].shape[0])
metricscols[3].metric('Estudiantes',df[df['rol'] == 'Estudiante'].shape[0])
metricscols[4].metric('Moderadores',df[df['rol'] == 'Moderador'].shape[0])
metricscols[5].metric('Promedio de Score',df['score'].mean())

st.dataframe(df)
plot1 = go.Figure(go.Histogram(x=df['score']))
plot1.update_layout(title='Distribución de Score',xaxis_title='Score',yaxis_title='Frecuencia')

plotcols = st.columns(3)
plotcols[0].plotly_chart(plot1,use_container_width=True)

countrangos = df['rango'].value_counts()
plot2 = go.Figure(go.Pie(labels=countrangos.index,values=countrangos.values))
plot2.update_layout(title='Distribución de Rangos')
plotcols[1].plotly_chart(plot2,use_container_width=True)

countroles = df['rol'].value_counts()
plot3 = go.Figure(go.Pie(labels=countroles.index,values=countroles.values))
plot3.update_layout(title='Distribución de Roles')
plotcols[2].plotly_chart(plot3,use_container_width=True)


st.subheader('Cursos')

dfcursos = pd.DataFrame(st.session_state.all_cursos['records'])
dfcursos.set_index('nombre',inplace=True)

cursocols = st.columns(5)

cursocols[0].metric('Cursos',dfcursos.shape[0])
cursocols[1].metric('Cursos Públicos',dfcursos[dfcursos['publico'] == True].shape[0])
cursocols[2].metric('Cursos Privados',dfcursos[dfcursos['publico'] == False].shape[0])
cursocols[3].metric('Alumnos Inscritos',dfcursos['inscritos'].sum())
cursocols[4].metric('Promedio de inscritos por curso',round(dfcursos['inscritos'].mean(),2))


st.dataframe(dfcursos)

cplotscolumns = st.columns(3)
plot4 = go.Figure(go.Histogram(x=dfcursos['inscritos']))
plot4.update_layout(title='Distribución de Inscripciones',xaxis_title='Inscritos',yaxis_title='Frecuencia')

cplotscolumns[0].plotly_chart(plot4,use_container_width=True)

countpublic = dfcursos['publico'].value_counts()
plot5 = go.Figure(go.Pie(labels=countpublic.index,values=countpublic.values))
plot5.update_layout(title='Distribución de Cursos Públicos')
cplotscolumns[1].plotly_chart(plot5,use_container_width=True)

inscritosporcursos = dfcursos.groupby('nombre').sum()['inscritos']
plot6 = go.Figure(go.Pie(labels=inscritosporcursos.index,values=inscritosporcursos.values))
plot6.update_layout(title='Inscritos por Curso')

cplotscolumns[2].plotly_chart(plot6,use_container_width=True)
