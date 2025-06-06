import streamlit as st
import requests
import time
from services import api
from utils.style import divisor, aviso_personalizado, espaco

def render_aluno_form():
    titulo = "✏️ Editando Aluno" if st.session_state.get("aluno_id_editando") else "📋 Cadastro de Aluno"
    divisor(titulo)

    espaco(1)

    id_editando = st.session_state.get("aluno_id_editando")
    dados_aluno = api.consultar_aluno(id_editando) if id_editando else {}

    # Inicializar estados
    if "endereco_vizualizacao" not in st.session_state:
        st.session_state["endereco_vizualizacao"] = {}
    if "criar_endereco_payload" not in st.session_state:
        st.session_state["criar_endereco_payload"] = None
    if "consultar_cep" not in st.session_state:
        st.session_state["consultar_cep"] = False

    with st.form("form_aluno"):
        nome = st.text_input("Nome", value=dados_aluno.get("nome_aluno", ""))
        email = st.text_input("Email", value=dados_aluno.get("email", ""))

        cep = st.text_input("CEP", value=dados_aluno.get("cep", {}).get("cep", "") if dados_aluno.get("cep") else "")
        cep_validado = cep.replace("-", "").replace(".", "").replace(" ", "")

        consultar = st.form_submit_button("🔎 Consultar CEP")

        if consultar:
            st.session_state["consultar_cep"] = True
            st.rerun()

        # Processa a consulta de CEP fora do form
        if st.session_state.get("consultar_cep"):
            st.session_state["consultar_cep"] = False  # Reseta o gatilho
            if len(cep_validado) == 8 and cep_validado.isdigit():
                try:
                    via_cep = requests.get(f"https://viacep.com.br/ws/{cep_validado}/json/")
                    if via_cep.status_code == 200 and "erro" not in via_cep.json():
                        data = via_cep.json()
                        endereco = data.get("logradouro", "")
                        cidade = data.get("localidade", "")
                        estado = data.get("uf", "")

                        st.session_state["endereco_vizualizacao"] = {
                            "endereco": endereco,
                            "cidade": cidade,
                            "estado": estado
                        }

                        st.session_state["criar_endereco_payload"] = {
                            "cep": cep_validado,
                            "endereco": endereco,
                            "cidade": cidade,
                            "estado": estado.upper()
                        }

                        aviso_personalizado("Endereço localizado automaticamente via CEP.", tipo="info")
                    else:
                        st.session_state["endereco_vizualizacao"] = {}
                        st.session_state["criar_endereco_payload"] = None
                        aviso_personalizado("CEP não encontrado no ViaCEP.", tipo="aviso")
                except:
                    aviso_personalizado("Erro na conexão com o ViaCEP.", tipo="erro")
            else:
                aviso_personalizado("Digite um CEP válido (8 dígitos).", tipo="aviso")

        # Exibir os dados detectados e confirmação
        endereco_info = st.session_state.get("endereco_vizualizacao", {})
        if endereco_info:
            st.markdown("**📍 Endereço detectado:**")
            st.text(f"Endereço: {endereco_info.get('endereco', '-')}")
            st.text(f"Cidade: {endereco_info.get('cidade', '-')}")
            st.text(f"Estado: {endereco_info.get('estado', '-')}")
            endereco_confirmado = st.radio(
                "Esse endereço está correto?", ["Selecione", "Sim", "Não"], key="endereco_confirmado"
            )
        else:
            endereco_confirmado = "Selecione"

        carro = st.text_input("ID do Carro", value=str(dados_aluno.get("carro", {}).get("id", "")) if dados_aluno.get("carro") else "")

        col1, col2,_ = st.columns([1,1,5])
        with col1:
            salvar = st.form_submit_button("💾 Salvar")
        with col2:
            voltar = st.form_submit_button("↩️ Voltar")

        if voltar:
            st.session_state["modo_cadastro"] = False
            st.session_state["aluno_id_editando"] = None
            st.rerun()

        if salvar:
            if endereco_info and endereco_confirmado != "Sim":
                aviso_personalizado("Por favor, confirme que o endereço está correto antes de salvar.", tipo="aviso")
                st.stop()

            if st.session_state["criar_endereco_payload"]:
                res = api.criar_endereco(st.session_state["criar_endereco_payload"])
                if res.status_code not in [200, 201]:
                    aviso_personalizado("Erro ao cadastrar endereço.", tipo="erro")
                    st.stop()

            payload = {
                "nome_aluno": nome,
                "email": email,
                "cep": cep_validado,
                "carro": int(carro) if carro else None
            }

            sucesso = api.atualizar_aluno(id_editando, payload) if id_editando else api.criar_aluno(payload)

            if sucesso:
                aviso_personalizado("Aluno salvo com sucesso!", tipo="sucesso")
                st.session_state["modo_cadastro"] = False

                # Limpeza segura dos estados temporários
                st.session_state.pop("endereco_vizualizacao", None)
                st.session_state.pop("criar_endereco_payload", None)
                st.session_state.pop("endereco_confirmado", None)

                time.sleep(2)
                st.rerun()
            else:
                aviso_personalizado("Erro ao salvar aluno.", tipo="erro")
