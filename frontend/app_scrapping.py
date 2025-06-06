import streamlit as st
import pandas as pd
import requests
import asyncio
import aiohttp

API_URL = "http://localhost:8000/api/webscrapping"  # ajuste se necessário

st.set_page_config(page_title="Scraper DF Imóveis", layout="wide")
st.title("Scraping de Imóveis com Django + Streamlit")

# Estado da sessão
if "df" not in st.session_state:
    st.session_state.df = None

# Executar scraping (chama API assincronamente)
async def executar_scraping_api():
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/executar-scraping") as resp:
            if resp.status == 200:
                data = await resp.json()
                return data
            else:
                st.error(f"Erro ao executar scraping: {resp.status}")
                return []

# Botão para executar scraping
if st.button("Executar scraping"):
    with st.spinner("Executando scraping..."):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        dados = loop.run_until_complete(executar_scraping_api())
        if dados:
            st.session_state.df = pd.DataFrame(dados)
            st.success("Scraping finalizado com sucesso!")

# Exibir resultados
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