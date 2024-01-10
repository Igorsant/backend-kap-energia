from modules import navegador
from selenium.webdriver.common.by import By
import time
import os
from selenium.webdriver.support.select import Select

def visit_gtsolar(formValues):
    elementos = [
        {
            "xpath": '//*[@id="email"]',
            "script": "type",
            "value": os.getenv('GT_SOLAR_EMAIL'),
        },
        {
            "xpath": '//*[@id="password"]',
            "script": "type",
            "value": os.getenv('GT_SOLAR_PASS'),
        },
        {
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div[1]/div[2]/div[1]/div/form/div[4]/button',
            "script": "click",
        },
        {
            "xpath": '//*[@id="app"]/div[2]/nav/div/div[3]/div/ul/li[3]/a',
            "script": "click",
        },
        {
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/input',
            "script": "type",
            "value": float(formValues["watt"])*100,
        },
        {
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[2]/select',
            "script": "select",
            "value": "tradicional",
        },
        {
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[3]/select',
            "script": "select",
            "value": formValues["classification"],
        },
        {
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/form/div/div/select',
            "script": "select",
            "value": formValues["roof"]
        }
    ]
    nav = navegador.execute_script("https://app.goldentecsolar.com.br/login", elementos)

    dimensionar_button = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/button')
    nav.execute_script("arguments[0].scrollIntoView();", dimensionar_button)
    
    dimensionar_button.click()
    time.sleep(2)
    componentes_tab = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[1]/button[2]')
    componentes_tab.click()

    servicos = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[1]/button[3]')
    servicos.click()

    time.sleep(1)
    cartao_select = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div/form/div[2]/div/select')
    cartao_select.click()
    Select(cartao_select).select_by_value(formValues["cartao"])

    time.sleep(1)
    parcelas = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div/form/div[3]/div/select')
    Select(parcelas).select_by_value("21")

    time.sleep(1)
    price = nav.find_element(By.CLASS_NAME, 'my-auto')
    
    print("Price is:", price.text)

    time.sleep(1)
    return nav.find_element(By.XPATH, '//*[@id="orcfooter"]/div[1]/div[1]/div/p').text
