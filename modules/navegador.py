from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def execute_script(site = '', elementos = []):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    navegador = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(navegador, timeout=10)
    
    print("navegador criado")
    if not site == '':
        navegador.get(site)
        wait.until(EC.presence_of_element_located((By.XPATH, elementos[0][By.XPATH])))
        print("site visitado")
    for element in elementos:
        el = wait.until(EC.element_to_be_clickable((By.XPATH, element[By.XPATH])))
        if element["script"] == "click":
            el.click()
        if element["script"] == "type":
            el.send_keys(element["value"])
        if element["script"] == "select":
            select = Select(el)
            select.select_by_value(element["value"])
    
    return navegador
