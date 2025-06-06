import streamlit as st
from paginas import home, alunos, notas, boletins, sobre
from utils.style import titulo_centralizado

st.set_page_config(
    page_title="Sistema Escolar",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135755.png", width=100)
st.sidebar.title("📚 Painel Escolar")
pagina = st.sidebar.radio(
    "Navegar para:", ["🏠 Início", "👨‍🎓 Alunos", "📝 Notas", "📘 Boletins", "📄 Sobre o Sistema"])

# Abas principais
if pagina == "🏠 Início":
    home.render()
elif pagina == "👨‍🎓 Alunos":
    alunos.render()
elif pagina == "📝 Notas":
    notas.render()
elif pagina == "📘 Boletins":
    boletins.render()
elif pagina == "📄 Sobre o Sistema":
    sobre.render()


# Rodapé
st.markdown("""
<hr style='margin-top: 3em; border: none; border-top: 1px solid #ccc;'/>
<p style='text-align: center; color: gray; font-size: 14px;'>
    Desenvolvido por <strong>Lucas, Luigi, Julia</strong> · Sistema Escolar v1.0 · Powered by Streamlit
</p>
""", unsafe_allow_html=True)
