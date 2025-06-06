import streamlit as st
import requests
import time

API_BASE = "http://127.0.0.1:8000/api/administracao"

st.set_page_config(page_title="Gestão de Alunos", layout="centered")
st.title("📚 Painel de Alunos")

# Estado
if "aluno_id_editando" not in st.session_state:
    st.session_state["aluno_id_editando"] = None

if "modo_cadastro" not in st.session_state:
    st.session_state["modo_cadastro"] = False

if "confirmando_delete" not in st.session_state:
    st.session_state["confirmando_delete"] = None

if "busca_nome" not in st.session_state:
    st.session_state["busca_nome"] = ""

if "buscar_agora" not in st.session_state:
    st.session_state["buscar_agora"] = False

if "nota_editando" not in st.session_state:
    st.session_state["nota_editando"] = None


# Campo de busca

st.session_state["busca_nome"] = st.text_input(
    "🔍 Pesquisar aluno", value=st.session_state["busca_nome"]
)

pesquisar, limpar ,vazio, vazio1 = st.columns(4)
with pesquisar:
    if st.button("🔎 Pesquisar"):
        st.session_state["buscar_agora"] = True
        st.rerun()

with limpar:
    if st.button("🧹 Limpar filtro"):
        st.session_state["busca_nome"] = ""
        st.session_state["buscar_agora"] = False
        st.rerun()


# Funções auxiliares
def listar_alunos():
    try:
        res = requests.get(f"{API_BASE}/alunos")
        return res.json() if res.status_code == 200 else []
    except:
        return []

def consultar_aluno(id_aluno):
    try:
        res = requests.get(f"{API_BASE}/consultar-alunos/{id_aluno}")
        return res.json() if res.status_code == 200 else None
    except:
        return None
    
def atualizar_aluno(id_aluno, data):
    try:
        res = requests.put(f"{API_BASE}/atualizar-alunos/{id_aluno}", json=data)
        return res.status_code == 200
    except:
        return False
    
def criar_aluno(payload):
    try:
        res = requests.post(f"{API_BASE}/criar-aluno", json=payload)
        return res.status_code == 200 or res.status_code == 201
    except:
        return False

def deletar_aluno(id_aluno):
    try:
        res = requests.delete(f"{API_BASE}/deletar-aluno/{id_aluno}")
        return res.status_code == 204
    except:
        return False
def listar_notas_do_aluno(aluno_id):
    try:
        res = requests.get(f"{API_BASE}/notas/aluno/{aluno_id}")
        return res.json() if res.status_code == 200 else []
    except:
        return []

def cadastrar_nota(payload):
    try:
        res = requests.post(f"{API_BASE}/notas", json=payload)
        return res.status_code == 200 or res.status_code == 201
    except:
        return False

def deletar_nota(nota_id):
    try:
        res = requests.delete(f"{API_BASE}/notas/{nota_id}")
        return res.status_code == 204
    except:
        return False
    
def atualizar_nota(nota_id, payload):
    try:
        res = requests.put(f"{API_BASE}/notas/{nota_id}", json=payload)
        return res.status_code == 200
    except:
        return False


# Página
st.markdown("---")

if st.button("➕ Cadastrar novo aluno"):
    st.session_state["modo_cadastro"] = True
    st.session_state["aluno_id_editando"] = None
    st.rerun()

if st.session_state["modo_cadastro"]:
    st.subheader("➕ Novo Aluno")

    with st.form("form_cadastro"):
        nome = st.text_input("Nome")
        email = st.text_input("Email")

        # ========= CEP ============
        cep = st.text_input("CEP")
        cep_validado = cep.replace("-", "").replace(".", "").replace(" ", "")

        endereco_auto = {}
        if len(cep_validado) == 8 and cep_validado.isdigit():
            try:
                resposta = requests.get(f"https://viacep.com.br/ws/{cep_validado}/json/")
                if resposta.status_code == 200:
                    data = resposta.json()
                    if "erro" not in data:
                        endereco_auto = {
                            "cep": cep_validado,
                            "endereco": data.get("logradouro", ""),
                            "cidade": data.get("localidade", ""),
                            "estado": data.get("uf", "")
                        }
                        st.success("Endereço preenchido automaticamente.")
                    else:
                        st.warning("CEP não encontrado na base do ViaCEP.")
                else:
                    st.error("Erro ao consultar o ViaCEP.")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
            novo_endereco = st.text_input("Endereço", value=endereco_auto.get("endereco", ""), key="novo_endereco_cadastro")
            nova_cidade = st.text_input("Cidade", value=endereco_auto.get("cidade", ""), key="nova_cidade_cadastro")
            novo_estado = st.text_input("Estado (UF)", value=endereco_auto.get("estado", ""), max_chars=2, key="novo_estado_cadastro")
            if novo_endereco and nova_cidade and novo_estado:
                criar_endereco_payload = {
                    "cep": cep_validado,
                    "endereco": novo_endereco,
                    "cidade": nova_cidade,
                    "estado": novo_estado.upper()
                }


        # ========= CARRO ============
        carro = st.text_input("ID do Carro")
        criar_carro_payload = None
        carro_id_definitivo = carro

        if carro:
            try:
                res_carro = requests.get(f"{API_BASE}/carros/{carro}")
                if res_carro.status_code != 200:
                    st.warning("Carro não encontrado. Preencha os dados abaixo para cadastrar:")
                    fabricante = st.text_input("Fabricante", key="novo_fabricante_cadastro")
                    modelo = st.text_input("Modelo", key="novo_modelo_cadastro")
                    especificacao = st.text_input("Especificação", key="nova_especificacao_cadastro")

                    if fabricante and modelo:
                        criar_carro_payload = {
                            "fabricante": fabricante,
                            "modelo": modelo,
                            "especificacao": especificacao or None
                        }
                    else:
                        st.info("Preencha fabricante e modelo para cadastrar o carro.")
            except:
                st.error("Erro ao verificar o carro.")
                st.stop()

        # ========= BOTÃO FINAL ============
        submit = st.form_submit_button("📥 Cadastrar")
        if submit:
            # Criar endereço se necessário
            if criar_endereco_payload:
                res = requests.post(f"{API_BASE}/enderecos", json=criar_endereco_payload)
                if res.status_code not in [200, 201]:
                    st.error("Erro ao cadastrar endereço.")
                    st.stop()

            # Criar carro se necessário
            if criar_carro_payload:
                res = requests.post(f"{API_BASE}/carros", json=criar_carro_payload)
                if res.status_code in [200, 201]:
                    carro_id_definitivo = res.json()["id"]
                else:
                    st.error("Erro ao cadastrar carro.")
                    st.stop()

            payload = {
                "nome_aluno": nome,
                "email": email,
                "cep": cep_validado,
                "carro": int(carro_id_definitivo) if carro_id_definitivo else None
            }

            sucesso = criar_aluno(payload)
            if sucesso:
                st.success("✅ Aluno cadastrado com sucesso!")
                st.session_state["modo_cadastro"] = False
                st.rerun()
            else:
                st.error("❌ Erro ao cadastrar aluno.")


if st.session_state["aluno_id_editando"] is None:
    st.subheader("📋 Lista de Alunos")

    alunos = listar_alunos()
    busca = st.session_state["busca_nome"].strip().lower()

    if st.session_state["buscar_agora"]:
        if busca:
            alunos = [a for a in alunos if busca in a["nome_aluno"].lower()]
        else:
            # Se clicou em pesquisar, mas não digitou nada → mostra todos
            alunos = listar_alunos()    
    else:
        # Se não clicou em pesquisar → mostra todos
        alunos = listar_alunos()

    for aluno in alunos:
        with st.expander(f"{aluno['id']} - {aluno['nome_aluno']}"):
            st.write(f"📧 Email: {aluno.get('email', '-')}")
            
            # CEP
            cep_raw = aluno.get("cep")
            if cep_raw:
                st.write(f"🏠 CEP: {cep_raw['cep']}")
                endereco = f"{cep_raw['endereco']}, {cep_raw['cidade']} - {cep_raw['estado']}"
                st.markdown(f"🏡 **Endereço:** {endereco}")
            else:
                st.write("🏠 CEP: -")
                st.markdown("🏡 **Endereço:** -")
            
            # Carro
            carro_raw = aluno.get("carro")
            if carro_raw:
                carro_info = f"{carro_raw['fabricante']} {carro_raw['modelo']} - {carro_raw['especificacao']}"
                st.markdown(f"🚗 **Carro:** {carro_info}")
            else:
                st.markdown("🚗 **Carro:** -")

            if st.button("✏️ Editar", key=f"editar_{aluno['id']}"):
                st.session_state["aluno_id_editando"] = aluno["id"]
                st.session_state["modo_cadastro"] = False
                st.rerun()
                
            if st.session_state["confirmando_delete"] == aluno["id"]:
                st.warning("Tem certeza que deseja deletar este aluno?")
                vazio, vazio1, confirmar, cancelar ,vazio2, vazio3 = st.columns(6)
                with confirmar:
                    if st.button("✅ Sim", key=f"confirmar_{aluno['id']}"):
                        sucesso = deletar_aluno(aluno["id"])
                        if sucesso:
                            st.success("Aluno deletado com sucesso!")
                            st.session_state["confirmando_delete"] = None
                            st.rerun()
                        else:
                            st.error("Erro ao deletar.")
                with cancelar:
                    if st.button("❌ Não", key=f"cancelar_{aluno['id']}"):
                        st.session_state["confirmando_delete"] = None
                        st.rerun()
            else:
                if st.button("🗑️ Deletar", key=f"deletar_{aluno['id']}"):
                    st.session_state["confirmando_delete"] = aluno["id"]
                    st.rerun()


else:
    aluno_id = st.session_state["aluno_id_editando"]
    aluno = consultar_aluno(aluno_id)

    if aluno:
        st.subheader(f"✏️ Editar Aluno: {aluno['nome_aluno']}")
        # fora do form
        cep_valor = aluno["cep"]["cep"] if aluno.get("cep") else ""
        carro_id_valor = str(aluno["carro"]["id"]) if aluno.get("carro") else ""

        with st.form("form_aluno"):

            nome = st.text_input("Nome", aluno["nome_aluno"])
            email = st.text_input("Email", aluno.get("email") or "")

            cep = st.text_input("CEP", cep_valor)
            cep_validado = cep.replace("-", "").replace(".", "").replace(" ", "")
            endereco = aluno.get("cep")

            # ======== CEP não encontrado, pedir dados ===================
            criar_endereco_payload = None
            if cep_validado:
                try:
                    res = requests.get(f"{API_BASE}/enderecos/{cep_validado}")
                    if res.status_code != 200:
                        st.warning("CEP não encontrado. Preencha o novo endereço.")
                        novo_endereco = st.text_input("Novo Endereço", key="novo_endereco")
                        nova_cidade = st.text_input("Nova Cidade", key="nova_cidade")
                        novo_estado = st.text_input("Novo Estado (UF)", max_chars=2, key="novo_estado")

                        if novo_endereco and nova_cidade and novo_estado:
                            criar_endereco_payload = {
                                "cep": cep_validado,
                                "endereco": novo_endereco,
                                "cidade": nova_cidade,
                                "estado": novo_estado.upper()
                            }
                        else:
                            st.info("Preencha todos os campos do endereço para cadastrar.")
                except:
                    st.error("Erro ao validar CEP.")

            # =========== ID do carro ============
            carro_id_valor = str(aluno["carro"]["id"]) if aluno.get("carro") else ""
            carro = st.text_input("ID do Carro", carro_id_valor)

            criar_carro_payload = None
            carro_id_definitivo = carro
            if carro:
                try:
                    res = requests.get(f"{API_BASE}/carros/{carro}")
                    if res.status_code != 200:
                        st.warning("Carro não encontrado. Preencha os dados do novo carro.")
                        fabricante = st.text_input("Fabricante do carro", key="novo_fabricante")
                        modelo = st.text_input("Modelo do carro", key="novo_modelo")
                        especificacao = st.text_input("Especificação", key="nova_especificacao")

                        if fabricante and modelo:
                            criar_carro_payload = {
                                "fabricante": fabricante,
                                "modelo": modelo,
                                "especificacao": especificacao or None
                            }
                        else:
                            st.info("Preencha fabricante e modelo para cadastrar o carro.")
                except:
                    st.error("Erro ao validar o carro.")

            # ========== BOTÃO DO FORMULÁRIO ==========
            submit = st.form_submit_button("💾 Salvar")

            if submit:
                # Criar endereço se necessário
                if criar_endereco_payload:
                    res = requests.post(f"{API_BASE}/enderecos", json=criar_endereco_payload)
                    if res.status_code not in [200, 201]:
                        st.error("Erro ao cadastrar endereço.")
                        st.stop()

                # Criar carro se necessário
                if criar_carro_payload:
                    res = requests.post(f"{API_BASE}/carros", json=criar_carro_payload)
                    if res.status_code in [200, 201]:
                        carro_id_definitivo = res.json()["id"]
                    else:
                        st.error("Erro ao cadastrar carro.")
                        st.stop()

                payload = {
                    "nome_aluno": nome,
                    "email": email,
                    "cep": cep_validado,
                    "carro": int(carro_id_definitivo) if carro_id_definitivo else None
                }

                sucesso = atualizar_aluno(aluno["id"], payload)
                if sucesso:
                    st.success("✅ Aluno atualizado com sucesso!")
                    st.session_state["aluno_id_editando"] = None
                    st.rerun()
                else:
                    st.error("❌ Erro ao atualizar.")

st.markdown("---")
st.subheader("➕ Cadastrar Nota")

# Buscar alunos
try:
    alunos = listar_alunos()
except:
    alunos = []

if alunos:
    nomes_alunos = [f"{a['id']} - {a['nome_aluno']}" for a in alunos]
    sel_aluno = st.selectbox("Aluno", nomes_alunos, key="select_aluno_cadastro_nota")
    id_aluno = int(sel_aluno.split(" - ")[0])

    # Buscar disciplinas
    try:
        res = requests.get(f"{API_BASE}/disciplinas")
        disciplinas = res.json() if res.status_code == 200 else []
    except:
        disciplinas = []

    if disciplinas:
        nomes_disciplinas = [f"{d['id']} - {d['nome_disciplina']}" for d in disciplinas]
        sel_disc = st.selectbox("Disciplina", nomes_disciplinas, key="select_disciplina_cadastro_nota")
        id_disciplina = int(sel_disc.split(" - ")[0])

        nota_valor = st.number_input("Nota", min_value=0.0, max_value=10.0, step=0.1, key="nota_input_cadastro")

        if st.button("💾 Cadastrar Nota"):
            # Verificar se já existe nota para esse aluno e disciplina
            notas_existentes = listar_notas_do_aluno(id_aluno)
            ja_tem_nota = any(n["disciplina"]["id"] == id_disciplina for n in notas_existentes)

            if ja_tem_nota:
                st.warning("Este aluno já possui uma nota cadastrada para essa disciplina.")
            else:
                payload = {
                    "aluno": id_aluno,
                    "disciplina": id_disciplina,
                    "nota": nota_valor
                }
                sucesso = cadastrar_nota(payload)
                if sucesso:
                    st.success("Nota cadastrada com sucesso!")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.error("Erro ao cadastrar nota.")

    else:
        st.warning("Nenhuma disciplina cadastrada.")
else:
    st.warning("Nenhum aluno encontrado.")


st.markdown("---")
st.subheader("📘 Boletim de Aluno")

# Selecionar aluno
alunos = listar_alunos()
if alunos:
    nomes_alunos = [f"{a['id']} - {a['nome_aluno']}" for a in alunos]
    sel_aluno = st.selectbox("Selecione o aluno para ver o boletim", nomes_alunos, key="aluno_boletim")
    aluno_id = int(sel_aluno.split(" - ")[0])
    nome_aluno = [a["nome_aluno"] for a in alunos if a["id"] == aluno_id][0]
    
    st.markdown(f"### 📄 Boletim de: **{nome_aluno}**")

    notas = listar_notas_do_aluno(aluno_id)
    if notas:
        for nota in notas:
            with st.expander(f"{nota['disciplina']['nome_disciplina']} - Nota: {nota['nota']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Carga Horária: {nota['disciplina']['carga']}h")
                    st.write(f"Semestre: {nota['disciplina']['semestre']}")
                with col2:
                    if st.session_state["nota_editando"] == nota["id"]:
                        nova_nota = st.number_input(
                            "Nova Nota",
                            value=float(nota["nota"]) if nota["nota"] else 0.0,
                            min_value=0.0,
                            max_value=10.0,
                            step=0.8,
                            key=f"nota_input_{nota['id']}"
                        )
                        if st.button("💾 Salvar", key=f"salvar_nota_{nota['id']}"):
                            payload = {
                                "aluno": nota["aluno"]["id"],
                                "disciplina": nota["disciplina"]["id"],
                                "nota": nova_nota
                            }
                            sucesso = atualizar_nota(nota["id"], payload)
                            if sucesso:
                                st.success("Nota atualizada com sucesso!")
                                time.sleep(1.5) 
                                st.session_state["nota_editando"] = None
                                st.rerun()
                            else:
                                st.error("Erro ao atualizar nota.")
                        if st.button("❌ Cancelar", key=f"cancelar_nota_{nota['id']}"):
                            st.session_state["nota_editando"] = None
                            st.rerun()
                    else:
                        if st.button("✏️ Editar Nota", key=f"editar_nota_{nota['id']}"):
                            st.session_state["nota_editando"] = nota["id"]
                            st.rerun()
                        if st.button("🗑️ Excluir Nota", key=f"del_nota_{nota['id']}"):
                            sucesso = deletar_nota(nota['id'])
                            if sucesso:
                                st.success("Nota excluída com sucesso!")
                                st.rerun()
                            else:
                                st.error("Erro ao excluir nota.")
    else:
        st.info("Este aluno ainda não possui notas.")
