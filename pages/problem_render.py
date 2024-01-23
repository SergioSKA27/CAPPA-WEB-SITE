import streamlit as st
import hydralit_components as hc
from streamlit_extras.switch_page_button import switch_page
from code_editor import code_editor
import subprocess
import tracemalloc
from types import SimpleNamespace
from time import perf_counter
from streamlit_profiler import Profiler
from streamlit_quill import st_quill
from streamlit import session_state as state
from streamlit_elements import elements, event, lazy, mui, sync
from streamlit_extras.switch_page_button import switch_page
from streamlit_profiler import Profiler
from st_xatadb_connection import XataConnection

from modules import Card, Dashboard, DataGrid, Editor, Pie, Player, Radar, Timer
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
