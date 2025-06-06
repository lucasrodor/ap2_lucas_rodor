import streamlit as st
from utils.style import titulo_centralizado, divisor, texto_destaque, espaco

def render():
    titulo_centralizado("🎓 Bem-vindo ao Sistema Escolar", "h1", cor="#1E90FF")
    titulo_centralizado("""
    Este painel foi desenvolvido para facilitar a gestão de alunos,
                        o lançamento de notas e o acompanhamento do desempenho escolar em um ambiente simples, moderno e eficiente.
    """, "h5", cor = "#fff")

    divisor()
    titulo_centralizado("📌 O que você pode fazer aqui", "h3", cor = "#fff")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("✅ **Cadastrar alunos** com seus dados e informações de endereço e veículo")
        st.markdown("✅ **Editar ou remover** alunos existentes")
        st.markdown("✅ **Registrar notas** por disciplina")
    with col2:
        st.markdown("✅ **Visualizar boletins completos** de cada aluno")
        st.markdown("✅ Acompanhar **notas por disciplina e semestre**")
        st.markdown("✅ Interface simples, responsiva e com carregamento rápido")
    espaco()
    st.info("Use o menu lateral para navegar entre as funcionalidades do sistema. 🚀")
