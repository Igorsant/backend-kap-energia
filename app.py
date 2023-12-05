from modules import gt_solar as gt_solar, souenergy as souenergy
from flask import Flask, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["POST"])
def best_price():
    # souenergy.visit_souenergy(request.json)
    gt_solar.visit_gtsolar(request.json)
    return ""

@app.route("/", methods=["GET"])
def hello_heroku():
    return "Hello Heroku!"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=os.getenv('PORT', 8080))
