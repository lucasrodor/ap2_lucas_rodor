import streamlit as st
from services import api
import time
from utils.style import aviso_personalizado, divisor, titulo_centralizado

def render_boletim_por_aluno():
    alunos = api.listar_alunos()
    if not alunos:
        aviso_personalizado("Nenhum aluno cadastrado.", tipo="aviso")
        return

    nomes_alunos = [f"{a['id']} - {a['nome_aluno']}" for a in alunos]
    sel_aluno = st.selectbox("Selecione o aluno", nomes_alunos, key="aluno_boletim")
    aluno_id = int(sel_aluno.split(" - ")[0])
    nome_aluno = [a["nome_aluno"] for a in alunos if a["id"] == aluno_id][0]
    divisor()
    titulo_centralizado(f"📘 Boletim de: {nome_aluno}", "h3", cor="#fff")

    notas = api.listar_notas_do_aluno(aluno_id)
    if not notas:
        aviso_personalizado("Este aluno ainda não possui notas.", tipo="info")
        return

    for nota in notas:
        with st.expander(f"{nota['disciplina']['nome_disciplina']} - Nota: {nota['nota']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"Carga Horária: {nota['disciplina']['carga']}h")
                st.write(f"Semestre: {nota['disciplina']['semestre']}")
            with col2:
                if st.session_state.get("nota_editando") == nota["id"]:
                    nova_nota = st.number_input(
                        "Nova Nota",
                        value=float(nota["nota"]) if nota["nota"] else 0.0,
                        min_value=0.0,
                        max_value=10.0,
                        step=0.5,
                        key=f"nota_input_{nota['id']}"
                    )
                    if st.button("💾 Salvar", key=f"salvar_nota_{nota['id']}"):
                        payload = {
                            "aluno": nota["aluno"]["id"],
                            "disciplina": nota["disciplina"]["id"],
                            "nota": nova_nota
                        }
                        sucesso = api.atualizar_nota(nota["id"], payload)
                        if sucesso:
                            aviso_personalizado("Nota atualizada com sucesso!", tipo="sucesso")
                            st.session_state["nota_editando"] = None
                            time.sleep(1)
                            st.rerun()
                        else:
                            aviso_personalizado("Erro ao atualizar nota.", tipo="erro")
                    if st.button("❌ Cancelar", key=f"cancelar_nota_{nota['id']}"):
                        st.session_state["nota_editando"] = None
                        st.rerun()
                else:
                    if st.button("✏️ Editar Nota", key=f"editar_nota_{nota['id']}"):
                        st.session_state["nota_editando"] = nota["id"]
                        st.rerun()
                    if st.button("🗑️ Excluir Nota", key=f"del_nota_{nota['id']}"):
                        sucesso = api.deletar_nota(nota['id'])
                        if sucesso:
                            aviso_personalizado("Nota excluída com sucesso!", tipo="sucesso")
                            st.rerun()
                        else:
                            aviso_personalizado("Erro ao excluir nota.", tipo="erro")
