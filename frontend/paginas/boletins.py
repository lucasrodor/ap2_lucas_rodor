import streamlit as st
from components.boletim_view import render_boletim_por_aluno
from utils.style import titulo_centralizado, divisor

def render():
    titulo_centralizado("📘 Boletim de Alunos", "h2", cor="#1E90FF")

    titulo_centralizado(" Aqui você pode visualizar o boletim completo de cada aluno, com todas as disciplinas cadastradas e as respectivas notas.",
                        "h5", cor = "#fff")
    divisor()
    st.markdown("""
    
    ### O que é possível fazer:
    - 📄 Ver notas por disciplina
    - ✏️ Editar uma nota existente
    - 🗑️ Excluir uma nota se necessário

    """)
    st.info("Use o seletor abaixo para escolher um aluno e visualizar o boletim individual.")
    divisor()
    render_boletim_por_aluno()
