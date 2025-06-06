import streamlit as st
import pandas as pd
import requests
import asyncio
import aiohttp

API_URL = "http://localhost:8000/api/webscrapping"

st.set_page_config(page_title="Scraper DF Imóveis", layout="wide")
st.title("Scraping de Imóveis com Django + Streamlit")

if "df" not in st.session_state:
    st.session_state.df = None

# Formulário de filtros
with st.form("filtros_form"):
    st.subheader("Filtros de Busca")

    tipo_operacao = st.selectbox("Tipo de operação", ["", "ALUGUEL", "IMOVEL NOVO", "TEMPORADA", "VENDA"])
    tipo_imovel = st.selectbox("Tipo de imóvel", [
        "", "Apartamento", "Casa", "Kitnet/Studio", "Cobertura", "Loja",
        "Prédio", "Terreno", "Hotel/Flat"
    ])
    localizacao = st.text_input("Localização")
    cidade = st.text_input("Cidade")
    bairro = st.text_input("Bairro")
    quartos = st.selectbox("Número de quartos", ["", "1", "2", "3", "4", "5 ou mais"])
    preco_medio = st.text_input("Preço médio")
    palavra_chave = st.text_input("Palavra-chave")

    submit = st.form_submit_button("Executar scraping")

# Função assíncrona para chamar a API
async def executar_scraping_api(filtros):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/executar-scraping", json=filtros) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                st.error(f"Erro ao executar scraping: {resp.status}")
                return []

if submit:
    with st.spinner("Executando scraping..."):
        filtros = {
            "tipo_operacao": tipo_operacao,
            "tipo_imovel": tipo_imovel,
            "localizacao": localizacao,
            "cidade": cidade,
            "bairro": bairro,
            "quartos": quartos,
            "preco_medio": preco_medio,
            "palavra_chave": palavra_chave
        }
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        dados = loop.run_until_complete(executar_scraping_api(filtros))
        if dados:
            st.session_state.df = pd.DataFrame(dados)
            st.success("Scraping finalizado com sucesso!")

if st.session_state.df is not None:
    st.subheader("Resultado do Scraping")
    st.dataframe(st.session_state.df)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Salvar no banco de dados"):
            with st.spinner("Salvando no banco..."):
                try:
                    response = requests.post(
                        f"{API_URL}/salvar-dados",
                        json=st.session_state.df.to_dict(orient="records")
                    )
                    if response.status_code == 200:
                        st.success(response.json()["mensagem"])
                    else:
                        st.error("Erro ao salvar no banco de dados.")
                except Exception as e:
                    st.error(f"Erro: {e}")

    with col2:
        if st.button("Exportar para Excel"):
            with st.spinner("Exportando..."):
                try:
                    response = requests.post(
                        f"{API_URL}/exportar-excel",
                        json=st.session_state.df.to_dict(orient="records")
                    )
                    if response.status_code == 200:
                        caminho = response.json()["arquivo"]
                        st.success(f"Excel gerado em: {caminho}")
                    else:
                        st.error("Erro ao exportar Excel.")
                except Exception as e:
                    st.error(f"Erro: {e}")
