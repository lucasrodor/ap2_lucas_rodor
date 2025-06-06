import streamlit as st
from services import api
import time
from utils.style import divisor, aviso_personalizado

def render_aluno_cards():
    st.subheader("📋 Lista de Alunos")

    # Campo de busca com estado
    if "busca_nome" not in st.session_state:
        st.session_state["busca_nome"] = ""

    if "confirmando_delete_aluno" not in st.session_state:
        st.session_state["confirmando_delete_aluno"] = None


    if "buscar_agora" not in st.session_state:
        st.session_state["buscar_agora"] = False

    st.session_state["busca_nome"] = st.text_input(
        "🔍 Pesquisar por nome do aluno", value=st.session_state["busca_nome"]
    )


    if st.button("🔎 Pesquisar"):
        st.session_state["buscar_agora"] = True
        st.rerun()

    if st.button("🧹 Limpar filtro"):
        st.session_state["busca_nome"] = ""
        st.session_state["buscar_agora"] = False
        st.rerun()

    divisor()

    alunos = api.listar_alunos()

    if st.session_state["buscar_agora"]:
        busca = st.session_state["busca_nome"].strip().lower()
        if busca:
            alunos = [a for a in alunos if busca in a["nome_aluno"].lower()]

    if not alunos:
        aviso_personalizado("Nenhum aluno encontrado.", tipo="info")
        return

    for aluno in alunos:
        with st.expander(f"{aluno['id']} - {aluno['nome_aluno']}"):
            st.write(f"📧 Email: {aluno.get('email', '-')}")

            cep_raw = aluno.get("cep")
            if cep_raw:
                endereco = f"{cep_raw['endereco']}, {cep_raw['cidade']} - {cep_raw['estado']}"
                st.write(f"🏠 CEP: {cep_raw['cep']}")
                st.write(f"📍 Endereço: {endereco}")
            else:
                st.write("🏠 Endereço: -")

            carro_raw = aluno.get("carro")
            if carro_raw:
                info = f"{carro_raw['fabricante']} {carro_raw['modelo']} - {carro_raw.get('especificacao', '-')}"
                st.write(f"🚗 Carro: {info}")
            else:
                st.write("🚗 Carro: -")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("✏️ Editar", key=f"editar_{aluno['id']}"):
                    st.session_state["aluno_id_editando"] = aluno["id"]
                    st.session_state["modo_cadastro"] = True
                    st.rerun()
            with col2:
                if st.session_state["confirmando_delete_aluno"] == aluno["id"]:
                    st.warning("Tem certeza que deseja deletar este aluno?")
                    col_confirmar, col_cancelar = st.columns(2)
                    with col_confirmar:
                        if st.button("✅ Confirmar", key=f"confirma_delete_{aluno['id']}"):
                            sucesso = api.deletar_aluno(aluno["id"])
                            if sucesso:
                                aviso_personalizado("Aluno deletado com sucesso!", tipo="sucesso")
                                st.session_state["confirmando_delete_aluno"] = None
                                time.sleep(1.5)
                                st.rerun()
                            else:
                                aviso_personalizado("Erro ao deletar aluno.", tipo="erro")
                    with col_cancelar:
                        if st.button("❌ Cancelar", key=f"cancela_delete_{aluno['id']}"):
                            st.session_state["confirmando_delete_aluno"] = None
                            st.rerun()
                else:
                    if st.button("🗑️ Deletar", key=f"deletar_{aluno['id']}"):
                        st.session_state["confirmando_delete_aluno"] = aluno["id"]
                        st.rerun()
