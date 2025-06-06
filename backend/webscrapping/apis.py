from ninja import Router
from typing import List
from webscrapping.schemas import ImovelIn, ImovelOut, FiltroScraping
from webscrapping import views

router = Router()

@router.post("/salvar-dados")
async def salvar_dados(request, dados: List[ImovelIn]):
    return await views.salvar_dados(request, dados)

@router.post("/exportar-excel")
async def exportar_excel(request, dados: List[ImovelIn]):
    return await views.exportar_excel(request, dados)

@router.get("/imoveis", response=List[ImovelOut])
async def listar_imoveis(request):
    return await views.listar_imoveis(request)

@router.post("/executar-scraping")
async def executar_scraping(request, filtros: FiltroScraping):
    return await views.executar_scraping(request, filtros)