import streamlit as st
from components.aluno_form import render_aluno_form
from components.aluno_card import render_aluno_cards
from utils.style import titulo_centralizado, divisor, espaco, texto_destaque

def render():
    titulo_centralizado("👨‍🎓 Cadastro e Gestão de Alunos", "h2", cor="#1e90ff")
    titulo_centralizado("""Aqui você pode adicionar novos alunos editar os dados de cadastro e consultar
    a lista de estudantes registrados.""", "h5", cor = "#fff")

    _,_,col1,_,_ = st.columns(5)
    with col1:
        if st.button("➕ Novo Aluno", use_container_width=True):
            st.session_state["modo_cadastro"] = True
            st.session_state["aluno_id_editando"] = None
    
    divisor()

    divisor("🔎 Buscar ou Gerenciar Alunos")
    if st.session_state.get("modo_cadastro", False):
        render_aluno_form()
    else:
        render_aluno_cards()    
