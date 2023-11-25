from modules import gt_solar as gt_solar, souenergy as souenergy
from flask import Flask, request
from flask_cors import CORS
import os

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
    # gt_solar.visit_gtsolar(kwp_number)
    return ""

@app.route("/", methods=["GET"])
def hello_heroku():
    return "Hello Heroku!"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=os.getenv('PORT', 8080))
