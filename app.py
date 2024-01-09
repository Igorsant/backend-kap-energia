from modules import gt_solar, souenergy
from modules import luvik
from flask import Flask, request
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/gtsolar", methods=["POST"])
def search_gtsolar():
    valor = gt_solar.visit_gtsolar(request.json)
    print("Valor do painel:", valor)
    return valor

@app.route("/souenergy", methods=["POST"])
def search_souenergy():
    valor = souenergy.visit_souenergy(request.json)
    print("Valor do painel:", valor)
    return valor

@app.route("/", methods=["GET"])
def hello_heroku():
    return "Hello Heroku!"

@app.route("/luvik", methods=["POST"])
def create_luvik():
    return luvik.start_luvik(request.json)

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=os.getenv('PORT', 8080))
