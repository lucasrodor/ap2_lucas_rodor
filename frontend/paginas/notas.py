import streamlit as st
from components.nota_form import render_nota_form
from utils.style import titulo_centralizado, divisor, texto_destaque

def render():
    titulo_centralizado("📝 Cadastro de Notas", "h2", cor="#1e90ff")

    titulo_centralizado("Nesta página você pode registrar as notas dos alunos em suas respectivas disciplinas.",
                        "h5", cor = "#fff")
    divisor()
    st.markdown("""
    
    ### Como usar:
    1. Selecione o aluno
    2. Escolha a disciplina
    3. Informe a nota
    4. Clique em "Cadastrar Nota"

    ⚠️ O sistema impede a duplicação de notas para a mesma disciplina.
    """)
    divisor()
    render_nota_form()
