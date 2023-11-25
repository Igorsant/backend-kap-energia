from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

def set_chrome_options() -> Options:
    """
    Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")

    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}

    return chrome_options

def execute_script(site, elementos):
    navegador = webdriver.Chrome()
    navegador.implicitly_wait(5)
    navegador.get(site)

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
