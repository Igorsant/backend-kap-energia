from modules import navegador
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def visit_souenergy(formValues):
    elementos = [
        {
            "xpath": '//*[@id="loginIconContainer"]/div[1]',
            "script": "click",
            "shouldWait": True
        },
        {
            "xpath": '//*[@id="email"]',
            "script": "type",
            "value": os.getenv('SOU_ENERGY_EMAIL'),
        },
        {
            "xpath": '//*[@id="pass"]',
            "script": "type",
            "value": os.getenv('SOU_ENERGY_PASS'),
        },
        {
            "xpath": '//*[@id="send2"]',
            "script": "click"
        },
        {
            "xpath": '/html/body/div[1]/div/a',
            "script": "click"
        }
    ]

    nav = navegador.execute_script("https://souenergy.com.br", elementos)
    
    time.sleep(3)
    actions = ActionChains(nav)
    compre_por_marca = nav.find_element(By.XPATH, '//*[@id="ui-id-3"]')
    actions.move_to_element(compre_por_marca).perform()
    nav.find_element(By.XPATH, '//*[@id="ui-id-15"]').click()

    boards = nav.find_elements(By.XPATH, '//*[@id="maincontent"]/div[3]/div[1]/div[3]/ol/li')
    for board in boards:
        product_link = board.find_element(By.CLASS_NAME, 'product-item-link')
        text = product_link.text
        number = float(text.split(' ')[-1].replace('kWp', '').replace(",", "."))
        if formValues["kwp"] <= number:
            nav.execute_script("arguments[0].scrollIntoView();", board)
            nav.execute_script("arguments[0].click();", product_link)
            break

    nav.execute_script('document.querySelector(".block-bundle-summary").style.display="none"')

    best_panel = _get_best_panel(nav, formValues["kwp"])["radio"]
    nav.execute_script("arguments[0].scrollIntoView();", best_panel)
    best_panel.click()
    print("Best panel was:", best_panel.text)
    
    # protecao cc
    scroll_click_element(nav, '//*[@id="product-options-wrapper"]/div/fieldset/div[3]/div[1]/div/div[1]/label/div/span')

    # cabo ca
    scroll_click_element(nav, '//*[@id="product-options-wrapper"]/div/fieldset/div[7]/div[1]/div/div[1]/label/div')
    
    # aterramento
    scroll_click_element(nav, '//*[@id="product-options-wrapper"]/div/fieldset/div[8]/div[1]/div/div[1]/label/div')

    #kit
    scroll_click_element(nav, '//*[@id="product-options-wrapper"]/div/fieldset/div[9]/div[1]/div/div[1]/label/div')

    if "mini-trilho" in formValues["roof"]:
        minitrilho = nav.find_element(By.XPATH, '//span[text()="MINITRILHO EM PRFV 25cm PARA TELHADO METÁLICO - 45m/s - SOU ENERGY (GARANTIA - 25 ANOS)"]')
        minitrilho.click()
        print("mini-trilho escolhido")
    if "fibrocimento" in formValues["roof"]:
        fibrocimento = nav.find_element(By.XPATH, '//span[text()="PRISIONEIRO PARA MADEIRA COM PERFIL EM PRFV 2,40m P/ TELHADOS C/ TELHAS CERÂMICAS|METÁLICAS|FIBROCIMENTO - 45m/s - SOU ENERGY (GARANTIA - 12 ANOS)"]')
        fibrocimento.click()
        print("fibrocimento escolhido")
    if "Laje" in formValues["roof"]:
        scroll_click_element(nav, '//*[@id="product-options-wrapper"]/div/fieldset/div[10]/div[1]/div/div[1]/label/div/span')
        laje = nav.find_element(By.XPATH, '//span[text()="KIT DE LAJE/SOLO P/ 4 MÓDULOS EM RETRATO"]')
        laje.click()
        print("laje escolhido")

    nav.execute_script('document.querySelector(".block-bundle-summary").style.display="block"')
    preco = nav.find_element(By.XPATH, '//*[@id="bundleSummary"]/div/div/div/div/div[3]/p/span')

    summary = nav.find_element(By.XPATH, '//*[@id="bundle-summary"]/ul')
    summary_infos = summary.find_elements(By.TAG_NAME, 'li')

    response_dict = {}
    for info in summary_infos:
        values = info.text.split('\n')
        print(values[0], '--->', values[1])
        response_dict[values[0]] = values[1]
    response_dict['preco:'] = preco.text

    # time.sleep(10)
    return response_dict

def scroll_click_element(nav, xpath):
    element = nav.find_element(By.XPATH, xpath)
    nav.execute_script("arguments[0].scrollIntoView();", element)
    element.click()

def _get_best_panel(nav, kwp):
    parent_panel = nav.find_element(By.XPATH, '//*[@id="product-options-wrapper"]/div/fieldset/div[2]/div/div')
    nav.execute_script("arguments[0].scrollIntoView();", parent_panel)
    list_panel = parent_panel.find_elements(By.CLASS_NAME, "choice")
    panels = []
    for panel in list_panel:
        radio_button = panel.find_element(By.TAG_NAME, 'input')
        nav.execute_script("arguments[0].scrollIntoView();", radio_button)
        radio_button.click()
        try:
            panels.append({
                "radio": radio_button,
                "kwp": nav.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[2]/span').text,
                "preco": nav.find_element(By.XPATH, '//*[@id="bundleSummary"]/div/div/div/div/div[3]/p/span').text,
                "date": panel.find_element(By.CLASS_NAME, 'dataPrevendaItem').text
            })
        except NoSuchElementException:
            panels.append({
                "radio": radio_button,
                "kwp": nav.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[2]/span').text,
                "preco": nav.find_element(By.XPATH, '//*[@id="bundleSummary"]/div/div/div/div/div[3]/p/span').text,
                
                "date": None
            })
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
