import requests

API_BASE = "http://127.0.0.1:8000/api/administracao"

# --- Alunos ---
def listar_alunos():
    res = requests.get(f"{API_BASE}/alunos")
    return res.json() if res.status_code == 200 else []

def consultar_aluno(id_aluno):
    res = requests.get(f"{API_BASE}/consultar-alunos/{id_aluno}")
    return res.json() if res.status_code == 200 else None

def criar_aluno(data):
    res = requests.post(f"{API_BASE}/criar-aluno", json=data)
    return res.status_code in [200, 201]

def atualizar_aluno(id_aluno, data):
    res = requests.put(f"{API_BASE}/atualizar-alunos/{id_aluno}", json=data)
    return res.status_code == 200

def deletar_aluno(id_aluno):
    res = requests.delete(f"{API_BASE}/deletar-aluno/{id_aluno}")
    return res.status_code == 204
    #retorna falando que deu certo mas não retorna nenhum dado por isso 204

# --- Endereços ---
def consultar_endereco(cep):
    return requests.get(f"{API_BASE}/enderecos/{cep}")

def criar_endereco(data):
    return requests.post(f"{API_BASE}/enderecos", json=data)

# --- Carros ---
def consultar_carro(carro_id):
    return requests.get(f"{API_BASE}/carros/{carro_id}")

def criar_carro(data):
    return requests.post(f"{API_BASE}/carros", json=data)

# --- Notas ---
def listar_notas_do_aluno(aluno_id):
    res = requests.get(f"{API_BASE}/notas/aluno/{aluno_id}")
    return res.json() if res.status_code == 200 else []

def cadastrar_nota(data):
    res = requests.post(f"{API_BASE}/notas", json=data)
    return res.status_code in [200, 201]

def atualizar_nota(id_nota, data):
    res = requests.put(f"{API_BASE}/notas/{id_nota}", json=data)
    return res.status_code == 200

def deletar_nota(id_nota):
    res = requests.delete(f"{API_BASE}/notas/{id_nota}")
    return res.status_code == 204

# --- Disciplinas ---
def listar_disciplinas():
    res = requests.get(f"{API_BASE}/disciplinas")
    return res.json() if res.status_code == 200 else []
