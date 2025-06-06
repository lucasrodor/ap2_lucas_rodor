import streamlit as st
from services import api
import time
from utils.style import aviso_personalizado, divisor, espaco,titulo_centralizado

def render_nota_form():
    titulo = "📥 Cadastro de Nota"
    titulo_centralizado(f"{titulo}", "h3", cor="#fff")
    espaco(1)

    alunos = api.listar_alunos()
    disciplinas = api.listar_disciplinas()

    if not alunos:
        aviso_personalizado("Nenhum aluno cadastrado.", tipo="aviso")
        return

    if not disciplinas:
        aviso_personalizado("Nenhuma disciplina cadastrada.", tipo="aviso")
        return

    nomes_alunos = [f"{a['id']} - {a['nome_aluno']}" for a in alunos]
    nomes_disciplinas = [f"{d['id']} - {d['nome_disciplina']}" for d in disciplinas]

    sel_aluno = st.selectbox("Aluno", nomes_alunos, key="select_aluno_nota")
    sel_disc = st.selectbox("Disciplina", nomes_disciplinas, key="select_disciplina_nota")

    id_aluno = int(sel_aluno.split(" - ")[0])
    id_disciplina = int(sel_disc.split(" - ")[0])

    nota_valor = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1, key="nota_input")

    if st.button("💾 Cadastrar Nota"):
        notas_existentes = api.listar_notas_do_aluno(id_aluno)
        ja_tem_nota = any(n["disciplina"]["id"] == id_disciplina for n in notas_existentes)

        if ja_tem_nota:
            aviso_personalizado("Este aluno já possui uma nota para esta disciplina.", tipo="aviso")
        else:
            payload = {
                "aluno": id_aluno,
                "disciplina": id_disciplina,
                "nota": nota_valor
            }
            sucesso = api.cadastrar_nota(payload)
            if sucesso:
                aviso_personalizado("Nota cadastrada com sucesso!", tipo="sucesso")
                time.sleep(1.5)
                st.rerun()
            else:
                aviso_personalizado("Erro ao cadastrar nota.", tipo="erro")
