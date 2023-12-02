from flask import Flask, render_template, Response, jsonify
from flask_cors import CORS, cross_origin
import json
import methods

#app = Flask(__name__)
app=Flask(__name__,static_folder='static',template_folder='template')
CORS(app)

# Routes
@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")
@app.route('/login', methods=['POST'])
def login():
    return methods.login()


@app.route('/add_car', methods=['POST'])
def add_car():
    return methods.add_car()


@app.route('/get_enregistrements', methods=['GET'])
def get_enregistrements():
    return methods.get_enregistrements()


@app.route('/save_abonnement', methods=['POST'])
def save_abonnement():
    return methods.save_abonnement()

@app.route('/get_cars', methods=['GET'])
def get_cars():
    return methods.getCars()


@app.route('/get_cars_in_parking', methods=['GET'])
def get_cars_in_parking():
    return methods.get_cars_in_parking()


if __name__ == '__main__':
    app.run(debug=True)
