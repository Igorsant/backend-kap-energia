import modules.gt_solar as gt_solar
from flask import Flask, request
from flask_cors import CORS
from selenium.webdriver.common.by import By

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def best_price():
    watts = request.json["watts"]

    total = gt_solar.visit_gtsolar(watts)
    print(watts)
    return f'{total}'
