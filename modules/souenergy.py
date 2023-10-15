from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome()
navegador.implicitly_wait(5)

navegador.get("https://souenergy.com.br")

elementos = [
    {
        'name': 'Click para login',
        'xpath': '//*[@id="loginIconContainer"]/div[1]/span',
        'script': 'click'
    },
    {
        'name': 'email',
        'xpath': '//*[@id="email"]',
        'script': 'type',
        'value': 'gestaogkap@gmail.com'
    },
    {
        'name': 'pass',
        'xpath': '//*[@id="pass"]',
        'script': 'type',
        'value': 'Engarq_123$'
    },
    {
        'name': 'enter button',
        'xpath': '//*[@id="send2"]',
        'script': 'click'
    },
]

for element in elementos:
    el = navegador.find_element(By.XPATH, element[By.XPATH])
    if element['script'] == 'click':
        el.click()
    if element['script'] == 'type':
        time.sleep(1)
        el.send_keys(element['value'])