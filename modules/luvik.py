import os
from modules import navegador
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_luvik(formValues):
    elements = [
        {
            "name": "email",
            "xpath": '//*[@id="loginForm"]/div/div[2]/div[1]/input',
            "script": "type",
            "value": os.getenv('LUVIK_EMAIL'),
        },
        {
            "name": "password",
            "xpath": '//*[@id="show_hide_password"]/input',
            "script": "type",
            "value": os.getenv('LUVIK_PASS'),
        },
        {
            "name": "button login",
            "xpath": '//*[@id="loginForm"]/div/div[3]/button',
            "script": "click"
        }
    ]
    nav = navegador.execute_script('https://app.luvik.com.br/login', elements)
    
    time.sleep(3)
    wait = WebDriverWait(nav, timeout=10)

    actions = ActionChains(nav)
    sidebar = nav.find_element(By.XPATH, '/html/body/div[1]/div[1]/div')
    print('moving to sidebar...', sidebar)
    actions.move_to_element(sidebar).perform()

    novo_negocio = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="linkModalNovoNegocio"]')))
    novo_negocio.click()
    
    return 'worked!'
    # name = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="nomeNG"]')))
    # name.send_keys(formValues["name"])

    # phone = nav.find_element(By.XPATH, '//*[@id="telefoneNG"]')
    # phone.send_keys(formValues["phone"])

    # state = nav.find_element(By.XPATH, '//*[@id="ufMenu"]')
    # state_select = Select(state)
    # state_select.select_by_value(formValues["state"])

    # city = nav.find_element(By.XPATH, '//*[@id="cidadeMenu"]')
    # city_select = Select(city)
    # city_select.select_by_value(formValues["city"])

    # next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnContinuarDadosContaPvMenu"]')))
    # next_button.click()

    # time.sleep(10)