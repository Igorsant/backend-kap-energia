from modules import navegador
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

def visit_gtsolar(formValues):
    elementos = [
        {
            "name": "email",
            "xpath": '//*[@id="email"]',
            "script": "type",
            "value": os.getenv('GT_SOLAR_EMAIL'),
        },
        {
            "name": "pass",
            "xpath": '//*[@id="password"]',
            "script": "type",
            "value": os.getenv('GT_SOLAR_PASS'),
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
            "name": "watt",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[2]/div[1]/input',
            "script": "type",
            "value": formValues["watt"],
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
            "value": formValues["classification"],
        },
        {
            "name": "Onde sera instalado",
            "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/form/div/div/select',
            "script": "select",
            "value": formValues["roof"]
        },
    ]
    nav = navegador.execute_script("https://app.goldentecsolar.com.br/login", elementos)

    fab_modules_value = {
        "canadian": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[1]/div[1]/div/div[3]/ul/li[1]/span',
        "rise": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[1]/div[1]/div/div[3]/ul/li[2]/span',
        "shinefar": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[1]/div[1]/div/div[3]/ul/li[3]/span'
    }

    fab_inversores_value = {
        "canadian": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[2]/div[1]/div/div[3]/ul/li[1]/span',
        "deye": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[2]/div[1]/div/div[3]/ul/li[2]/span',
        "general": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[2]/div[1]/div/div[3]/ul/li[3]/span'
    }
    for module in fab_modules_value.values():
        module_select = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[1]/div[1]/div/div[2]')
        module_select.click()
        module_value = nav.find_element(By.XPATH, module)
        module_value.click()
        for inversor in fab_inversores_value.values():
            inversor_select = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[2]/div[1]/div/div[2]')
            inversor_select.click()
            inversor_value = nav.find_element(By.XPATH, inversor)
            inversor_value.click()

            # actions = ActionChains(driver=nav)
            dimensionar_button = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/button')
            nav.execute_script("arguments[0].scrollIntoView();", dimensionar_button)
            dimensionar_button.click()
            time.sleep(2)
            componentes_tab = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[1]/button[2]')
            componentes_tab.click()

            price = nav.find_element(By.XPATH, '//*[@id="orcfooter"]/div[1]/div[1]/div/p[2]')
            print("Price is:", price.text)

            dimensionar_tab = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[1]/button[1]')
            dimensionar_tab.click()
            # at the end
            xicon_inversores = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[4]/form/div/div[2]/div[1]/div/div[2]/div[1]/span/i')
            xicon_inversores.click()
            time.sleep(1)
        xicon_modules = nav.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[4]/form/div/div[1]/div[1]/div/div[2]/div[1]/span/i')
        xicon_modules.click()
                # {
                #     "name": "Avancar",
                #     "xpath": '//*[@id="orcfooter"]/div[1]/div[2]/button',
                #     "script": "click"
                # },
                # {
                #     "name": "Cartao select",
                #     "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div/form/div[2]/div/select',
                #     "script": "select",
                #     "value": formValues["cartao"]
                # },
                # {
                #     "name": "Numero de parcelas",
                #     "xpath": '//*[@id="app"]/div[2]/div/main/div/div/div/div/div/div[2]/div[1]/div[2]/div/div/div[1]/div/form/div[3]/div/select',
                #     "script": "select",
                #     "value": "21"
                # }

    
    time.sleep(1)
    return nav.find_element(By.XPATH, '//*[@id="orcfooter"]/div[1]/div[1]/div/p').text
