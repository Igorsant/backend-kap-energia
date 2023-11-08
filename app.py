from modules import gt_solar as gt_solar, souenergy as souenergy
from flask import Flask, request
from flask_cors import CORS
from selenium.webdriver.common.by import By

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def best_price():
    kwp = request.json["kwp"]

    # total = gt_solar.visit_gtsolar(watts)
    # print(watts)
    # return f'{total}'
    kwp_number = float(kwp.replace(",", "."))
    souenergy.visit_souenergy(kwp_number)
    return ""
