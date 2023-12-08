from modules import gt_solar as gt_solar, souenergy as souenergy
from flask import Flask, request
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/gtsolar", methods=["POST"])
def search_gtsolar():
    return gt_solar.visit_gtsolar(request.json)

@app.route("/souenergy", methods=["POST"])
def search_souenergy():
    return souenergy.visit_souenergy(request.json)

@app.route("/", methods=["GET"])
def hello_heroku():
    return "Hello Heroku!"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=os.getenv('PORT', 8080))
