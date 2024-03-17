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
    kwp_offset = 0.09
    time.sleep(3)
    actions = ActionChains(nav)
    compre_por_marca = nav.find_element(By.XPATH, '//span[text()="Compre por marca"]')

    actions.move_to_element(compre_por_marca).perform()
    nav.find_element(By.XPATH, '//span[text()="Solplanet"]').click()

    get_best_board(nav, formValues, kwp_offset)

    try:
        nav.execute_script('document.querySelector(".block-bundle-summary").style.display="none"')
    except:
        print("couldn't remove footer")

    date = compare_date_inversor(_get_best_panel(nav, formValues["kwp"], kwp_offset), nav)
    
    try:
        [scroll_click_nenhum(nav, input) for input in ['PROTEÇÃO CC', 'CABO SOLAR PRETO', 'CABO SOLAR VERMELHO']]
    except:
        print("couldn't choose nenhum")

    if "mini-trilho" in formValues["roof"]:
        minitrilho = nav.find_element(By.XPATH, '//span[text()="MINITRILHO EM PRFV 25cm PARA TELHADO METÁLICO - 45m/s - SOU ENERGY (GARANTIA - 25 ANOS)"]')
        minitrilho.click()
        print("mini-trilho escolhido")
    if "fibrocimento" in formValues["roof"]:
        fibrocimento = nav.find_element(By.XPATH, '//span[text()="PRISIONEIRO PARA MADEIRA COM PERFIL EM PRFV 2,40m P/ TELHADOS C/ TELHAS CERÂMICAS|METÁLICAS|FIBROCIMENTO - 45m/s - SOU ENERGY (GARANTIA - 12 ANOS)"]')
        fibrocimento.click()
        print("fibrocimento escolhido")
    if "Laje" in formValues["roof"]:
        scroll_click_nenhum(nav, 'KIT DE FIXAÇÃO P/ 4  PAINÉIS')
        laje = nav.find_element(By.XPATH, '//span[text()="KIT DE LAJE/SOLO P/ 4 MÓDULOS EM RETRATO"]')
        laje.click()
        print("laje escolhido")

    try:
        nav.execute_script('document.querySelector(".block-bundle-summary").style.display="block"')
    except:
        print("couldn't put footer back")
    preco = nav.find_element(By.XPATH, '//*[@id="bundleSummary"]/div/div/div/div/div[3]/p/span')

    summary = nav.find_element(By.XPATH, '//*[@id="bundle-summary"]/ul')
    summary_infos = summary.find_elements(By.TAG_NAME, 'li')

    response_dict = {}
    for info in summary_infos:
        values = info.text.split('\n')
        print(values[0], '--->', values[1])
        response_dict[values[0]] = values[1]

    print(preco.text)
    float_price = preco.text.split("R$")[1].replace(".", "").replace(",", ".")
    formatted_price = "{:.2f}".format(float(float_price)/12)
    response_dict['Preço:'] = f'12x de R${formatted_price.replace(".", ",")}'
    if date:
        response_dict['Previsão de entrega:'] = date

    return response_dict

def scroll_click(nav, xpath):
    element = nav.find_element(By.XPATH, xpath)
    nav.execute_script("arguments[0].scrollIntoView();", element)
    element.click()

def scroll_click_nenhum(nav, name):
    print(name)
    scroll_click(nav, f'//span[text()="{name}"]/../../div/div/div/input')

def get_best_board(nav, formValues, kwp_offset):
    def sort_boards(b):
        price_float = float(b.find_element(By.CLASS_NAME, 'price').text.replace("R$", "").replace(".", "").replace(",", "."))
        return price_float
    for i in range(4):
        boards = nav.find_elements(By.XPATH, '//*[@id="maincontent"]/div[3]/div[1]/div[3]/ol/li')
        boards.sort(key=lambda b: sort_boards(b))
        
        for board in boards:
            print(board.find_element(By.CLASS_NAME, 'price').text)
        for board in boards:
            product_link = board.find_element(By.CLASS_NAME, 'product-item-link')
            text = product_link.text
            number = float(text.split(' ')[-1].replace('kWp', '').replace(",", "."))
            if formValues["kwp"] <= number+kwp_offset:
                nav.execute_script("arguments[0].scrollIntoView();", board)
                nav.execute_script("arguments[0].click();", product_link)
                return
        print("Didn find a board in this page")
        link = nav.find_elements(By.XPATH, '//*[@id="maincontent"]/div[3]/div[1]/div[4]/div[2]/ul/li[@class="item"]/a')[i]
        link.click()

def _get_best_panel(nav, kwp, kwp_offset):
    parent_panel = nav.find_element(By.XPATH, '//span[text()="PAINEL FOTOVOLTAICO"]/../../div')
    nav.execute_script("arguments[0].scrollIntoView();", parent_panel)
    list_panel = parent_panel.find_elements(By.CLASS_NAME, "choice")
    panels = []
    for panel in list_panel:
        radio_button = panel.find_element(By.TAG_NAME, 'input')
        nav.execute_script("arguments[0].scrollIntoView();", radio_button)
        radio_button.click()
        date = None
        try:
            date = panel.find_element(By.CLASS_NAME, 'dataPrevendaItem')
        except NoSuchElementException:
            pass

        if date:
            time_numbers = date.text.split("/")
            panel_date = datetime(int(time_numbers[2]), int(time_numbers[1]), int(time_numbers[0]))
            now = datetime.now()
            delta_time = timedelta(days=30)
            if panel_date > now+delta_time:
                continue

        if not(number_modules(parent_panel, kwp, kwp_offset, nav)):
            continue
        
        nav.execute_script('document.querySelector(".block-bundle-summary").style.display="block"')
        panels.append({
            "radio": radio_button,
            "kwp": nav.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[2]/span').text,
            "preco": nav.find_element(By.XPATH, '//*[@id="bundleSummary"]/div/div/div/div/div[3]/p/span').text,
            "date": date.text if date else None
        })
        nav.execute_script('document.querySelector(".block-bundle-summary").style.display="none"')
    panels.sort(key=lambda p:p["preco"])
    for p in panels:
        print("Preco:", p["preco"])
        print("radio", p["radio"])

    panels[0]["radio"].click()
    print(panels[0]["preco"])
    number_modules(parent_panel, kwp, kwp_offset, nav)
    return panels[0]["date"]

def number_modules(parent_panel, kwp, kwp_offset, nav):
    plus_button = parent_panel.find_element(By.CLASS_NAME, 'fa-plus-circle')
    current_qtd = parent_panel.find_element(By.CLASS_NAME, 'irs-single').text
    aux_qtd = ""
    current_kwp = nav.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[2]/span')
    print(current_qtd)
    
    while(aux_qtd != current_qtd):
        current_kwp = nav.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[2]/span')
        curr_kwp_value = get_kwp_value(current_kwp.text)
        if curr_kwp_value+kwp_offset > kwp:
            break
        plus_button.click()
        aux_qtd = current_qtd
        current_qtd = parent_panel.find_element(By.CLASS_NAME, 'irs-single').text
        
    kwp_value = get_kwp_value(current_kwp.text)
    if kwp_value+kwp_offset < kwp:
        return False

    minus_button = parent_panel.find_element(By.CLASS_NAME, 'fa-minus-circle')

    while(kwp_value+kwp_offset > kwp):
        print('going down')
        minus_button.click()
        current_kwp = nav.find_element(By.XPATH, '//*[@id="maincontent"]/div[2]/div/div[2]/span')
        current_kwp_value = get_kwp_value(current_kwp.text)
        kwp_value = current_kwp_value

    plus_button.click()
    return True
        
def get_kwp_value(kwp):
    if "\n" in kwp:
        return float(kwp.replace(",", ".").split("\n")[0])
    return float(kwp.replace(",", "."))

def compare_date_inversor(date_panel, nav):
    date_array = date_panel.split("/")
    date = datetime(int(date_array[2]), int(date_array[1]), int(date_array[0]))
    div_inversor = nav.find_element(By.XPATH, '//span[text()="INVERSOR"]/../../div')
    try:
        date_inversor_text = div_inversor.find_element(By.CLASS_NAME, 'dataPrevendaItem').text
        date_inversor_array = date_inversor_text.split("/")
        date_inversor = datetime(int(date_inversor_array[2]), int(date_inversor_array[1]), int(date_inversor_array[0]))
        if date_inversor > date:
            return date_inversor_text
        return date_panel
    except NoSuchElementException:
        return date_panel
