from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


def execute_script(site, elementos):
    navegador = webdriver.Chrome()
    navegador.implicitly_wait(5)
    navegador.get(site)
    wait = WebDriverWait(navegador, timeout=2)

    for element in elementos:
        el = navegador.find_element(By.XPATH, element[By.XPATH])
        if element.get("shouldWait"):
            time.sleep(3)
        if element["script"] == "click":
            el.click()
        if element["script"] == "type":
            el.send_keys(element["value"])
        if element["script"] == "select":
            select = Select(el)
            select.select_by_value(element["value"])

    return navegador
