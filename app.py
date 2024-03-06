from modules import gt_solar, souenergy
from modules import luvik
from flask import Flask, request, jsonify, abort
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def authenticate():
    if request.headers.get('Authorization') != os.getenv('AUTH_TOKEN'):
        abort(401)

@app.route("/gtsolar", methods=["POST"])
def search_gtsolar():
    authenticate()
    valor = gt_solar.visit_gtsolar(request.json)
    print("Valor do painel:", valor)
    return valor

@app.route("/souenergy", methods=["POST"])
def search_souenergy():
    authenticate()
    valor = souenergy.visit_souenergy(request.json)
    return valor

@app.route("/", methods=["GET"])
def hello_heroku():
    authenticate()
    return "Hello Heroku!"

@app.route("/luvik", methods=["POST"])
def create_luvik():
    authenticate()
    return luvik.start_luvik(request.json)

@app.route("/auth", methods=["GET"])
def auth():
    authenticate()
    return jsonify({'message': 'Success!'})

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=os.getenv('PORT', 8080))
