import navegador


def visit_souenergy():
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

    navegador.execute_script("https://souenergy.com.br", elementos)
