from modules import navegador
from selenium.webdriver.common.by import By


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
            "value": "gestaogkap@gmail.com",
        },
        {
            "name": "pass",
            "xpath": '//*[@id="pass"]',
            "script": "type",
            "value": "Engarq_123$",
        },
        {"name": "enter button", "xpath": '//*[@id="send2"]', "script": "click"},
    ]

    nav = navegador.execute_script("https://souenergy.com.br", elementos)

    nav.get("https://souenergy.com.br/inversores-e-microinversores/solplanet.html")

    boards = nav.find_elements(By.CLASS_NAME, "product-item-link")

    for board in boards:
        number = float(board.text.rstrip()[-8:-3].replace(",", ".").strip())
        if kwp <= number:
            board.click()
            print("found")
            break
        print(number)
    
    
