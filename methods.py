from flask import jsonify, request
import mysql.connector
from datetime import datetime, timedelta
import json
import jwt
import connection
import models

mydb = connection.get_database()

def login():
    mylist = []
    args = request.json
    email = args.get('email')
    password_user = args.get('password')
    req = "SELECT * FROM user WHERE email=%s AND password=%s"
    val = (email, password_user)
    myCursor = mydb.cursor()
    myCursor.execute(req, val)
    myresult = myCursor.fetchall()
    if myresult:
        exp_epoch = datetime.now() + timedelta(minutes=15)
        exp_epoch_time = int(exp_epoch.timestamp())
        myuser = models.User(email, password_user)
        payload = {"exp": exp_epoch_time}
        token = jwt.encode(payload, "sagar", algorithm="HS256")
        return {'email': email, 'password': password_user, 'token': token}
    else:
        return {}


def add_car():
    current_date = datetime.now()
    # Format the date as a string in 'YYYY-MM-DD' format
    args = request.json
    print(args)
    code_matricule = args.get('code_matricule')
    nom_client = args.get('nom_client') 
    cni_client = args.get('cni_client') 
    date_enregistrement = current_date.strftime('%Y-%m-%d')
    etat = args.get('etat')
    mycar = models.Car(code_matricule, nom_client, cni_client, date_enregistrement, etat)
    myCursor = mydb.cursor()
    req = "insert into cars (code_matricule, nom_client, cni_client, date_enregistrement) values (%s, %s, %s, %s)"
    val = (mycar.code_matricule, mycar.nom_client, mycar.cni_client, mycar.date_enregistrement)
    myCursor.execute(req, val)
    mydb.commit()
    
    return {'status': 'save :'}


def get_enregistrements():
    try:
        mylist = []
        req = "SELECT * FROM enregistrement"

        myCursor = mydb.cursor()
        myCursor.execute(req)
        myresult = myCursor.fetchall()

        for x in myresult:
            enregistrement_instance = models.Enregistrement(x[0], x[1], str(x[2]), str(x[3]))
            mylist.append(enregistrement_instance.__dict__)

        return json.dumps(mylist)

    except Exception as e:
        return jsonify({"error": str(e)})


def save_abonnement():
    try:
        args = request.json
        code_matricule = args.get('code_matricule')
        date_expiration = args.get('date_expiration')
        myCursor = mydb.cursor()
        req = "INSERT INTO abonnement (code_matricule, date_expiration) VALUES (%s, %s)"
        val = (code_matricule, date_expiration)
        myCursor.execute(req, val)
        mydb.commit()
        return {'status': 'success', 'message': 'Abonnement added successfully'}
    except Exception as e:
        return jsonify({"error": str(e)})


def save_enregistrement():
    try:
        data = request.get_json()
        code_matricule = data.get('code_matricule')

        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        req = "INSERT INTO enregistrement (code_matricule, datetime_entree, datetime_sortie) VALUES (%s, %s, %s)"
        values = (code_matricule, current_datetime, None)

        myCursor = mydb.cursor()
        myCursor.execute(req, values)
        mydb.commit()

        return jsonify({"message": "Enregistrement added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


def get_cars_in_parking():
    try:
        mylist = []
        myCursor = mydb.cursor()

        req = "SELECT * FROM cars WHERE etat != 'exterieur'"
        myCursor.execute(req)
        myresult = myCursor.fetchall()

        cars_in_parking = []

        for x in myresult:
            car_instance = models.Car(x[0], x[1], x[2], str(x[3]), x[4])
            cars_in_parking.append(car_instance.__dict__)

        return json.dumps(cars_in_parking)

    except Exception as e:
        return jsonify({"error": str(e)})

def getCars():
    mylist = []
    req = "select * from cars"
    myCursor = mydb.cursor()
    myCursor.execute(req)
    myresult = myCursor.fetchall()
    for x in myresult:
        car_instance = models.Car(x[0], x[1], x[2], str(x[3]),x[4])
        mylist.append(car_instance.__dict__)
    
    return json.dumps(mylist)