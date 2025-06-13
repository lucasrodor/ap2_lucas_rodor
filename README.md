
# 📚 Sistema Escolar & Scraper de Imóveis (Django + Django Ninja)

Este projeto Django contém **dois aplicativos integrados** com APIs RESTful desenvolvidas com **Django Ninja**:

- 🏫 `administracao`: um sistema escolar para cadastro e gerenciamento de alunos, endereços, carros, disciplinas e notas.
- 🏘️ `webscrapping`: realiza scraping assíncrono de imóveis à venda, salvando em banco de dados MySQL independente.

Desenvolvido por **Lucas Rodor**  
- [LinkedIn](https://www.linkedin.com/in/lucasrodor)  
- [GitHub](https://github.com/lucasrodor)

**Julia Felix Giannadrea**
-[Linkedin](https://www.linkedin.com/in/juliafgiannandrea/)
-[Github](https://github.com/juliafgiannandrea)

**Luigi Ajello**
-[Linkedin](https://www.linkedin.com/in/luigi-pedroso-ajello-346934278/)
-[Github](https://github.com/luigiajello)

---

## 🧠 Funcionalidades principais

### 🏫 Sistema Escolar
- CRUD completo para alunos
- Cadastro de endereços por CEP
- Cadastro de carros associados a alunos
- Cadastro de disciplinas
- Cadastro e visualização de notas por aluno e disciplina

### 🏘️ Scraper de Imóveis
- Executa scraping com filtros personalizáveis
- Armazena imóveis não duplicados no banco
- Lista imóveis coletados
- Retorna resultados recentes via arquivo temporário

---

## 🚀 Tecnologias utilizadas

- Python 3.11+
- Django
- Django Ninja
- MySQL (dois bancos distintos)
- Pandas
- Selenium
- Asyncio / asgiref
- python-dotenv
- [uv (Universal Virtualenv)](https://github.com/astral-sh/uv)

---

## 📁 Estrutura do projeto

```
├── manage.py
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── routers.py           # (opcional) para múltiplos bancos
├── administracao/
│   ├── models.py
│   ├── views.py
│   ├── apis.py
│   └── schemas.py
├── webscrapping/
│   ├── models.py
│   ├── views.py
│   ├── apis.py
│   ├── schemas.py
│   └── scraping/
│       ├── navegador.py
│       ├── filtros.py
│       ├── extrator.py
│       └── tratamento.py
├── requirements.txt
└── .env
```

---

## ⚙️ Como rodar localmente com `uv`

> Recomendado abrir o projeto com o Visual Studio Code (com a extensão do Python instalada).  
> O VS Code detecta automaticamente o ambiente virtual e ativa no terminal integrado.

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie o ambiente virtual com `uv`

```bash
uv venv
```

### 3. Instale as dependências

```bash
uv pip install -r requirements.txt
```

---

## 🛠️ Configuração dos Bancos de Dados

### Você precisará criar **dois bancos de dados separados** no MySQL:

#### 🔹 Banco 1: `db_escola`

```sql
CREATE DATABASE db_escola;
USE db_escola;

CREATE TABLE tb_enderecos (
    cep VARCHAR(10) PRIMARY KEY,
    endereco VARCHAR(255),
    cidade VARCHAR(100),
    estado VARCHAR(2)
);

CREATE TABLE tb_carros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fabricante VARCHAR(100),
    modelo VARCHAR(100),
    especificacao VARCHAR(255)
);

CREATE TABLE tb_alunos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_aluno VARCHAR(255),
    email VARCHAR(100),
    cep VARCHAR(10),
    carro_id INT,
    FOREIGN KEY (cep) REFERENCES tb_enderecos(cep),
    FOREIGN KEY (carro_id) REFERENCES tb_carros(id)
);

CREATE TABLE tb_disciplinas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome_disciplina VARCHAR(255),
    carga INT,
    semestre INT
);

CREATE TABLE tb_notas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    aluno_id INT,
    disciplina_id INT,
    nota DECIMAL(5,2),
    FOREIGN KEY (aluno_id) REFERENCES tb_alunos(id),
    FOREIGN KEY (disciplina_id) REFERENCES tb_disciplinas(id)
);
```

#### 🔹 Banco 2: `db_imoveis`

```sql
CREATE DATABASE db_imoveis;
USE db_imoveis;

CREATE TABLE imoveis (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255),
    preco DECIMAL(15,2),
    endereco VARCHAR(255),
    detalhes TEXT,
    descricao TEXT,
    link VARCHAR(500) UNIQUE,
    tamanho VARCHAR(20),
    quartos VARCHAR(20),
    vagas VARCHAR(20),
    suites VARCHAR(20),
    plantas VARCHAR(20),
    data_extracao DATETIME
);
```

---

## 🧩 Configuração do `.env`

```
DB1_NAME=db_escola
DB1_USER=root
DB1_PASSWORD=sua_senha
DB1_HOST=localhost

DB2_NAME=db_imoveis
DB2_USER=root
DB2_PASSWORD=sua_senha
DB2_HOST=localhost
```

---

## 🔧 Ajustes no `settings.py` (múltiplos bancos)

```python
import os
from dotenv import load_dotenv
load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB1_NAME'),
        'USER': os.getenv('DB1_USER'),
        'PASSWORD': os.getenv('DB1_PASSWORD'),
        'HOST': os.getenv('DB1_HOST'),
        'PORT': '3306',
    },
    'imoveis': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB2_NAME'),
        'USER': os.getenv('DB2_USER'),
        'PASSWORD': os.getenv('DB2_PASSWORD'),
        'HOST': os.getenv('DB2_HOST'),
        'PORT': '3306',
    }
}
```

---

## ▶️ Rodando o projeto

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 📬 Endpoints principais

### 🏫 API Escolar (`/api/escolar/`)

| Método |      Rota      |     Função    |
|--------|----------------|---------------|
|  GET   | `/alunos`      | Listar alunos |
|  POST  | `/criar-aluno` |  Criar aluno  |
| ...    | _e outros endpoints de notas, endereços, carros_ |

### 🏘️ API Scraper (`/api/imoveis/`)

| POST | `/executar-scraping` | Iniciar scraping |
| GET  | `/resultados-atuais` | Ver últimos resultados |
| GET  | `/imoveis`           | Listar imóveis |
| POST | `/salvar-dados`      | Salvar imóveis |

---

## ❓ Perguntas Frequentes

### 1. O que é `uv`?

`uv` é uma alternativa ultrarrápida ao `pip + virtualenv`, ideal para ambientes modernos. Instale com:

```bash
cargo install uv
```

Ou via binário: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)

---

### 2. Preciso instalar algo pro scraping?

Sim. Você precisa do **Google Chrome** e do **[ChromeDriver](https://sites.google.com/chromium.org/driver/)** compatível, e o `selenium` já vem no `requirements.txt`.

---

## 📄 Licença

Projeto desenvolvido para fins educacionais e demonstrativos.
