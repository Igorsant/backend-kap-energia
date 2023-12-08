from modules import navegador
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException

def visit_souenergy(formValues):
    elementos = [
        {
            "name": "Click para login",
            "xpath": '//*[@id="loginIconContainer"]/div[1]/span',
            "script": "click",
            "shouldWait": True
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
    time.sleep(3)
    nav.get("https://souenergy.com.br/inversores-e-microinversores/solplanet.html")
    boards = nav.find_elements(By.CLASS_NAME, "product-item-link")

    for board in boards:
        text = board.text
        number = float(text.rstrip()[-8:-3].replace(",", ".").strip())
        if formValues["watt"] <= number:
            board.click()
            break
    
    cabo_ca = nav.find_element(By.XPATH, '//*[@id="bundle-option-14656"]')
    nav.execute_script("arguments[0].scrollIntoView();", cabo_ca)
    cabo_ca.click()

    aterramento = nav.find_element(By.XPATH, '//*[@id="bundle-option-14657"]')
    nav.execute_script("arguments[0].scrollIntoView();", aterramento)
    aterramento.click()

    kit = nav.find_element(By.XPATH, '//*[@id="bundle-option-14655"]')
    nav.execute_script("arguments[0].scrollIntoView();", kit)
    kit.click()

    if "mini-trilho" in formValues["roof"]:
        minitrilho = nav.find_element(By.XPATH, '//*[@id="bundle-option-14654-93624"]')
        minitrilho.click()
    if "fibrocimento" in formValues["roof"]:
        fibrocimento = nav.find_element(By.XPATH, '//*[@id="bundle-option-14654-92404"]')
        fibrocimento.click()
    if "laje" in formValues["roof"]:
        laje = nav.find_element(By.XPATH, '//*[@id="bundle-option-14663-70584"]')
        laje.click()
    preco = nav.find_element(By.XPATH, '//*[@id="product-price-2551"]/span')
    return preco.text
    # parent_panel = nav.find_element(By.XPATH, '//*[@id="product-options-wrapper"]/div/fieldset/div[2]/div/div')
    # list_panel = parent_panel.find_elements(By.CLASS_NAME, "choice")
    # panels = []
    # for panel in list_panel:
    #     radio_button = panel.find_element(By.TAG_NAME, 'input')
    #     radio_button.location_once_scrolled_into_view
    #     radio_button.click()
    #     try:
    #         panels.append({
    #             "radio": radio_button,
    #             "kwp": nav.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[2]/span').text,
    #             "preco": nav.find_element(By.XPATH, '//*[@id="product-price-2551"]/span').text,
    #             "date": panel.find_element(By.CLASS_NAME, 'dataPrevendaItem').text
    #         })
    #     except NoSuchElementException:
    #         panels.append({
    #             "radio": radio_button,
    #             "kwp": nav.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[2]/span').text,
    #             "preco": nav.find_element(By.XPATH, '//*[@id="product-price-2551"]/span').text,
    #             "date": None
    #         })
    # best_panel = _get_best_panel(panels, kwp)["radio"]
    # best_panel.click()
    # print("Best panel was:", best_panel)

def _get_best_panel(panels, kwp):
    panels.sort(key=lambda p:p["preco"])
    for panel in panels:
        kwp_panel = get_kwp_value(panel["kwp"])
        print("kwp_panel:", kwp_panel)
        if kwp_panel < kwp:
            continue
        if panel["date"] == None:
            return panel
        time_numbers = panel["date"].split("/")
        print(time_numbers)
        panel_date = datetime(int(time_numbers[2]), int(time_numbers[1]), int(time_numbers[0]))
        now = datetime.now()
        delta_time = timedelta(days=20)
        if panel_date < now+delta_time:
            print(panel["preco"], panel_date)
            return panel
        
def get_kwp_value(kwp):
    if "\n" in kwp:
        return float(kwp.replace(",", ".").split("\n")[0])
    return float(kwp.replace(",", "."))
