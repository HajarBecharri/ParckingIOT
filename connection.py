
from flask import jsonify,Flask,render_template,request,Response
import mysql.connector
from flask_cors import CORS,cross_origin
import os
app = Flask(__name__)

CORS(app)
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_NAME = os.getenv("DB_NAME")
def get_database():
    return mysql.connector.connect(
    host=DB_HOST or "127.0.0.1",
    user=DB_USER or "root",
    password=DB_PASSWORD or "",
    database=DB_NAME or "projectparcking")
app.config["DEBUG"]=True



