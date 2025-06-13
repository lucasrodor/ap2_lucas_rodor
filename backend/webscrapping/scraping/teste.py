from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
# Tente sem headless primeiro
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
driver.get("https://www.google.com")

print("✅ Navegador abriu com sucesso")
input("Pressione Enter para fechar...")
driver.quit()