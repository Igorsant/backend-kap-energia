from modules import navegador
from selenium.webdriver.common.by import By
import time

def visit_gtsolar(watts):
    elementos = [
        {
            "name": "email",
            "xpath": '//*[@id="email"]',
            "script": "type",
            "value": "gestaogkap@gmail.com",
        },
        {
            "name": "pass",
            "xpath": '//*[@id="password"]',
            "script": "type",
            "value": "engarq123",
        },
        {
            "name": "enter button",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div[1]/div[2]/div[1]/div/form/div[4]/button',
            "script": "click",
        },
        {
            "name": "orcamento",
            "xpath": '//*[@id="app"]/div[2]/nav/div/div[3]/div/ul/li[3]/a',
            "script": "click",
        },
        {
            "name": "kwp",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/input',
            "script": "type",
            "value": watts,
        },
        {
            "name": "topologia",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/select',
            "script": "select",
            "value": "tradicional",
        },
        {
            "name": "Classificacao da rede",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[3]/select',
            "script": "select",
            "value": "monofasico",
        },
        {
            "name": "Fab. Modulos",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[1]/div[1]/div/div[2]',
            "script": "click"
        },
        {
            "name": "Fab. Modulos select value",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[1]/div[1]/div/div[3]/ul/li[3]',
            "script": "click"
        },
        {
            "name": "Fab. Inversores",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[2]/div[1]/div/div[2]',
            "script": "click"
        },
        {
            "name": "Fab. Inversores select value",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[2]/div[1]/div/div[3]/ul/li[2]',
            "script": "click"
        },
        {
            "name": "Onde sera instalado",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/form/div/div/select',
            "script": "select",
            "value": "PRATYC - Telha cerâmica",
            "shouldWait": True
        },
        {
            "name": "Dimensionar",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/button',
            "script": "click",
            "shouldWait": True
        },
        {
            "name": "Avancar",
            "xpath": '//*[@id="orcfooter"]/div[1]/div[2]/button',
            "script": "click",
            "shouldWait": True
        },
        {
            "name": "Avancar",
            "xpath": '//*[@id="orcfooter"]/div[1]/div[2]/button',
            "script": "click"
        },
        {
            "name": "Cartao select",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div/form/div[2]/div/select',
            "script": "select",
            "value": "SIM"
        },
        {
            "name": "Numero de parcelas",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div/form/div[3]/div/select',
            "script": "select",
            "value": "21"
        }
    ]

    nav = navegador.execute_script("https://app.goldentecsolar.com.br/login", elementos)
    time.sleep(1)
    return nav.find_element(By.XPATH, '//*[@id="orcfooter"]/div[1]/div[1]/div/p').text
