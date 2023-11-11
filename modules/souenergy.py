from modules import navegador
from selenium.webdriver.common.by import By
import time
import os

def visit_souenergy(kwp):
    elementos = [
        {
            "name": "Click para login",
            "xpath": '//*[@id="loginIconContainer"]/div[1]/span',
            "script": "click",
        },
        {
            "name": "email",
            "xpath": '//*[@id="email"]',
            "script": "type",
            "value": os.getenv('SOU_ENERGY_EMAIL'),
        },
        {
            "name": "pass",
            "xpath": '//*[@id="pass"]',
            "script": "type",
            "value": os.getenv('SOU_ENERGY_PASS'),
        },
        {"name": "enter button", "xpath": '//*[@id="send2"]', "script": "click"},
    ]

    nav = navegador.execute_script("https://souenergy.com.br", elementos)
    # time.sleep(3)
    # nav.get("https://souenergy.com.br/inversores-e-microinversores/solplanet.html")
    # boards = nav.find_elements(By.CLASS_NAME, "product-item-link")

    # for board in boards:
    #     text = board.text
    #     number = float(text.rstrip()[-8:-3].replace(",", ".").strip())
    #     if kwp <= number:
    #         board.click()
    #         print("found")
    #         break
    #     print(number)
    #     print("tamanho boards", len(boards))
    
    # parent_panel = nav.find_element(By.XPATH, '//*[@id="product-options-wrapper"]/div/fieldset/div[2]/div/div')
    # list_panel = parent_panel.find_elements(By.CLASS_NAME, "choice")
    # for panel in list_panel:
    #     radio_button = panel.find_element(By.TAG_NAME, 'input')
    #     radio_button.location_once_scrolled_into_view
    #     radio_button.click()
    #     kwp_status = nav.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[2]/span')
    #     print("Status do kwp:", kwp_status.text)

