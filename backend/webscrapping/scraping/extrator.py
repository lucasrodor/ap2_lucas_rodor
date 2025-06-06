
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import re


def extrair_dados(driver):
    wait = WebDriverWait(driver, 10)
    lista_imoveis = []
    pagina = 1

    while True:
        print(f"📄 Coletando página {pagina}...")

        try:
            wait.until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="resultadoDaBuscaDeImoveis"]')))
            cards = driver.find_elements(
                By.XPATH, '//*[@id="resultadoDaBuscaDeImoveis"]//a[contains(@href, "/imovel/")]')
        except Exception as e:
            print(f"❌ Erro ao localizar cards: {e}")
            break

        if not cards:
            print("⚠️ Nenhum card encontrado. Encerrando...")
            break

        for card in cards:
            imovel = {}
            try:
                imovel['titulo'] = card.find_element(
                    By.CLASS_NAME, 'new-title').text
            except:
                imovel['titulo'] = "N/A"
            try:
                imovel['preco'] = card.find_element(
                    By.CLASS_NAME, 'new-price').text
            except:
                imovel['preco'] = "N/A"
            try:
                imovel['endereco'] = card.find_element(
                    By.CLASS_NAME, 'new-subtitle').text
            except:
                imovel['endereco'] = "N/A"
            try:
                imovel['detalhes'] = card.find_element(
                    By.CLASS_NAME, 'new-details-ul').text
            except:
                imovel['detalhes'] = "N/A"
            try:
                imovel['descricao'] = card.find_element(
                    By.CLASS_NAME, 'new-simple').text
            except:
                imovel['descricao'] = "N/A"
            try:
                imovel['link'] = card.get_attribute("href")
            except:
                imovel['link'] = "N/A"

            lista_imoveis.append(imovel)

        try:
            paginacao = driver.find_elements(
                By.CSS_SELECTOR, '.pagination .btn.next')
            if not paginacao:
                print("🔚 Botão 'Próximo' não encontrado. Encerrando...")
                break

            botao_proximo = paginacao[0]
            if "disabled" in botao_proximo.get_attribute("class"):
                print("✅ Última página. Encerrando...")
                break

            print("Indo para a próxima página...")
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", botao_proximo)
            sleep(1)
            driver.execute_script("arguments[0].click();", botao_proximo)

            sleep(3)
            pagina += 1

        except Exception as e:
            print(f"❌ Erro ao clicar no botão de próxima página: {e}")
            break

    print(
        f"✅ Extração finalizada. Total de imóveis coletados: {len(lista_imoveis)}")
    return pd.DataFrame(lista_imoveis)
