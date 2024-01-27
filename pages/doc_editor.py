import streamlit as st
import hydralit_components as hc
from streamlit_extras.switch_page_button import switch_page
from types import SimpleNamespace
from streamlit_quill import st_quill
from streamlit import session_state as state
from streamlit_elements import elements, event, lazy, mui, sync
from streamlit_extras.switch_page_button import switch_page
from st_xatadb_connection import XataConnection
from streamlit_tags import st_tags


from modules import Card, Dashboard, Editor,  Timer
#Autor: Sergio Lopez



def merge_text(text: list):
    return "\n".join(text)

def format_code(code: str, lang: str):
    return f"```{lang}\n{code}\n```"

st.title('Editor de Problemas 👨‍💻')
st.divider()


if 'gtoast' not in state:
    state.gtoast = 0

if state.gtoast == 1:
    st.toast("Puedes ver el gráfico en la pestaña de código")
    state.gtoast = 2


pname =st.text_input('Titulo del Documento',placeholder="Principios de Programación en Python")

doc_types = ["Artículo", "Tutorial", "Video"]

doc_type = st.selectbox("Tipo de Documento", doc_types)

tabs = st.tabs(["Editor de texto", 'Código'])
with tabs[0]:
    desc = ''
    with st.form(key='my_form'):
        desc = st_quill(placeholder='Contenido del Documento',html=True,key='quill-docs')
        editcols = st.columns([0.8,0.2])
        with editcols[1]:
            savedesc = st.form_submit_button(label='Preview',use_container_width=True)
        if savedesc:
            st.markdown("##### Preview")
            st.markdown(desc, unsafe_allow_html=True)
with tabs[1]:
    if "w_docs" not in state:
        board = Dashboard()
        w = SimpleNamespace(
            dashboard=board,
            editor=Editor(
                board,
                0,
                0,
                8,
                6,
            )
        )
        state.w_docs = w
        w.editor.add_tab("Código Markdown", "# Hola Mundo!", "markdown")
    else:
        w = state.w_docs
    with st.container(border=True):
        cols= st.columns([0.8,0.2])
        with cols[0]:
            with elements("workspace"):
                event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
                with w.dashboard(rowHeight=57):
                    w.editor()
        with cols[1]:
            with st.form(key='lang_form'):
                lang = st.selectbox("Selecciona un lenguage", ["Python", "JavaScript", "Java", "C", "Cpp", "C#", "HTML", "CSS", "SQL",
    "R", "Rust", "Go", "PHP", "TypeScript", "Ruby", "Swift", "Kotlin", "Scala", "Julia", "Dart", "Haskell", "Lua",
    "Perl", "Objective-C", "MATLAB","Markdown", "JSON", "YAML", "Dockerfile", "GraphQL", "Handlebars", "LaTeX",
    "Groovy", "PowerShell", "VBScript", "Clojure", "Elixir", "F#", "Fortran", "OCaml",
    "Pascal", "Racket", "Scheme", "Bash", "Assembly", "CoffeeScript", "Erlang", "Haxe", "Nim", "OCaml", "Prolog",
    "PureScript", "Reason", "Scratch", "Solidity", "Tcl", "Vim", "XML", "YAML"])

                if st.form_submit_button(label="Añadir Tab"):
                    if f"Código {lang}" not in w.editor._tabs:
                        w.editor.add_tab(f"Código {lang}", '', lang.lower())
                        w.editor.add_tab(f"Código {lang}", '', lang.lower())
                    else:
                        k = 1
                        while f"Código {lang} {k}" in w.editor._tabs:
                            k += 1

                        w.editor.add_tab(f"Código {lang} {k}", '', lang.lower())
                    st.rerun()
            with st.form(key='tab_form'):
                deltab = st.selectbox("Eliminar Tab", ["Selecciona un tab"] + list(w.editor._tabs.keys()))
                if st.form_submit_button(label="Eliminar Tab"):
                    if deltab != "Selecciona un tab" and len(w.editor._tabs) > 1:
                        del w.editor._tabs[deltab]
                        st.rerun()
            if st.button("Añadir Gráfica",use_container_width=True):
                if "Gráfico" not in w.editor._tabs:
                     w.editor.add_tab("Gráfica",'''
    digraph D {

  subgraph cluster_p {
    label = "Parent";

    subgraph cluster_c1 {
      label = "Child one";
      a;

      subgraph cluster_gc_1 {
        label = "Grand-Child one";
         b;
      }
      subgraph cluster_gc_2 {
        label = "Grand-Child two";
          c;
          d;
      }

    }

    subgraph cluster_c2 {
      label = "Child two";
      e;
    }
  }
}
''', "dot")
                else:
                    k = 1
                    while f"Gráfico {k}" in w.editor._tabs:
                        k += 1
                    w.editor.add_tab(f"Gráfica {k}", '', "dot")
                st.rerun()



        ptabs = st.tabs(w.editor._tabs.keys())
        for i, tab in enumerate(w.editor._tabs.keys()):
            with ptabs[i]:
                if "Markdown" in tab:
                    st.write(w.editor.get_content(tab))
                elif  "Gráfica" in tab:
                    st.graphviz_chart(w.editor.get_content(tab))
                else:
                    st.code(w.editor.get_content(tab), language=tab.split(" ")[1].lower())



layout = st.multiselect("Selecciona las seciones del documento en orden",['Editor de texto']+list(w.editor._tabs.keys()))

if layout:
    lay = []
    for i, l in enumerate(layout):
        if l == "Editor de texto":
            st.markdown(desc, unsafe_allow_html=True)
            lay.append(desc)
        elif "Gráfica" in l:
            st.graphviz_chart(w.editor.get_content(l))
            lay.append(format_code(w.editor.get_content(l), "dot"))
        else:
            st.code(w.editor.get_content(l), language=l.split(" ")[1].lower())


