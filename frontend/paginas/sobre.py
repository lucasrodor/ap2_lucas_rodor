import streamlit as st
from utils.style import titulo_centralizado, divisor, texto_destaque, espaco

def render():
    titulo_centralizado("📄 Sobre o Sistema", "h2", cor="#1e90ff")
    titulo_centralizado("""
        Este sistema foi desenvolvido com o objetivo de facilitar a gestão acadêmica de alunos, notas e disciplinas. 
        Ele foi projetado para oferecer simplicidade, desempenho e experiência de usuário agradável, atendendo desde projetos educacionais até contextos reais de pequenas instituições de ensino.
    ""","h5", cor = "#fff")
    divisor()
    divisor("🧰 Tecnologias Utilizadas")
    st.markdown("""
    - 🐍 **Python**
    - 🔧 **Django REST + Django Ninja (backend)**
    - ⚡ **Streamlit (frontend)**
    - 💽 **MYSQL** como banco de dados
    - 🎨 Estilo customizado com CSS inline + componentes visuais adaptados
    """)
    divisor()
    divisor("🚀 Funcionalidades Implementadas")
    st.markdown("""
    - Cadastro, edição e exclusão de alunos
    - Validação de CEPs com integração automática via API
    - Registro e controle de veículos dos alunos
    - Cadastro e edição de disciplinas
    - Registro e edição de notas por aluno/disciplina
    - Boletim por aluno com exibição interativa
    - Prevenção de duplicidade de notas
    - Interface modularizada com navegação por abas
    """)

    divisor()
    divisor("📈 Possíveis Evoluções")
    st.markdown("""
    - Exportação de boletins em PDF
    - Dashboard analítico por aluno
    - Login e autenticação de usuários
    - Permissões para diferentes tipos de acesso (admin/professor/aluno)
    """)

    divisor()
    divisor("👨‍💻 Desenvolvedor")
    st.markdown("""
    - Projeto criado por Lucas Rodor** 🎓
    - Contato: github.com/lucasrodor
    """)

    st.markdown("---")
    st.success("Obrigado por explorar o sistema! Use o menu lateral para navegar entre os módulos.")
