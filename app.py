"""
Entrada principal — redireciona ao formulário do aluno
"""
import streamlit as st

st.set_page_config(
    page_title="Rehagro · Customer Success",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.switch_page("pages/1_Formulario.py")
