from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def execute_script(site = '', elementos = []):
    # chrome_options = set_chrome_options()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    navegador = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(navegador, timeout=10)
    
    if not site == '':
        navegador.get(site)
        wait.until(EC.presence_of_element_located((By.XPATH, elementos[0][By.XPATH])))
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
