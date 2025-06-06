import asyncio
import pandas as pd
from django.utils.timezone import now
from webscrapping.models import Imoveis
from webscrapping.schemas import ImovelIn, FiltroScraping
from asgiref.sync import sync_to_async
from pathlib import Path
from webscrapping.scraping.navegador import iniciar_navegador
from webscrapping.scraping.extrator import extrair_dados
from webscrapping.scraping.tratamento import tratar_dataframe
from webscrapping.scraping.filtros import aplicar_filtros

@sync_to_async
def salvar_no_banco_async(dados):
    novos = 0
    for item in dados:
        if not Imoveis.objects.filter(link=item.link).exists():
            Imoveis.objects.create(**item.dict(), data_extracao=now())
            novos += 1
    return novos

@sync_to_async
def exportar_excel_async(dados):
    df = pd.DataFrame([item.dict() for item in dados])
    path = Path("data")
    path.mkdir(exist_ok=True)
    filename = path / f"imoveis_{now().strftime('%Y-%m-%d_%H-%M')}.xlsx"
    df.to_excel(filename, index=False)
    return str(filename)

@sync_to_async
def listar_todos_async():
    return list(Imoveis.objects.all().values())

async def salvar_dados(request, dados: list[ImovelIn]):
    novos = await salvar_no_banco_async(dados)
    return {"mensagem": f"{novos} registros salvos com sucesso."}

async def exportar_excel(request, dados: list[ImovelIn]):
    path = await exportar_excel_async(dados)
    return {"mensagem": "Arquivo Excel exportado com sucesso.", "arquivo": path}

async def listar_imoveis(request):
    dados = await listar_todos_async()
    return dados

async def executar_scraping(request, filtros: FiltroScraping):
    loop = asyncio.get_event_loop()

    def tarefa():
        driver = iniciar_navegador(headless=True)
        try:
            aplicar_filtros(
                driver,
                tipo_operacao=filtros.tipo_operacao,
                tipo_imovel=filtros.tipo_imovel,
                localizacao=filtros.localizacao,
                cidade=filtros.cidade,
                bairro=filtros.bairro,
                quartos=filtros.quartos,
                preco_medio=filtros.preco_medio,
                palavra_chave=filtros.palavra_chave,
            )
            df = extrair_dados(driver)
            return tratar_dataframe(df).to_dict(orient="records")
        finally:
            driver.quit()

    resultado = await loop.run_in_executor(None, tarefa)
    return resultado