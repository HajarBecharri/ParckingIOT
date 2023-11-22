from flask import jsonify,Flask,render_template,request
from flask_cors import CORS,cross_origin
from flask_mysqldb import MySQL
import json
import mysql.connector
import myCar as car
import user as user
import enregistrement as eng
import jwt
from datetime import datetime,timedelta

app = Flask(__name__)

CORS(app)
mydb=mysql.connector.connect(user='root',password='',host='localhost',database='projectparcking')

app.config["DEBUG"]=True



@app.route('/savecar' , methods = ['POST'])
def saveCar():


    args = request.json
    print(args)
    code_matricule = args.get('code_matricule')
    nom_client = args.get('nom_client')
    cni_client = args.get('cni_client')
    date_enregistrement = args.get('date_enregistrement')

    myCursor = mydb.cursor()

    mycar = car.Car(code_matricule , nom_client ,cni_client , date_enregistrement)
    req = "insert into cars (code_matricule , nom_client ,cni_client ,date_enregistrement) values (%s , %s , %s,%s)"
    val = (mycar.code_matricule , mycar.nom_client , mycar.cni_client,mycar.date_enregistrement)
    myCursor.execute(req , val)
    mydb.commit()
    return {'status':'save :'}
@app.route('/saveabonnement', methods=['POST'])
def save_abonnement():
    args = request.json
    code_matricule = args.get('code_matricule')
    date_expiration = args.get('date_expiration')

    myCursor = mydb.cursor()

    req = "INSERT INTO abonnement (code_matricule, date_expiration) VALUES (%s, %s)"
    val = (code_matricule, date_expiration)

    try:
        myCursor.execute(req, val)
        mydb.commit()
        return {'status': 'success', 'message': 'Abonnement ajouté avec succès'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@app.route('/enregistrement' , methods = ['GET'])
def getenregistremnts():
    mylist = []
    req = "select * from enregistrement"
    

    myCursor = mydb.cursor()
    myCursor.execute(req)
    myresult = myCursor.fetchall()
    for x in myresult:
        enregistrement_instance = eng.Enregistrement(x[0], x[1], str(x[2]), str(x[3]))
        mylist.append(enregistrement_instance.__dict__)
    
    return json.dumps(mylist)
@app.route('/cars' , methods = ['GET'])
def getCars():
    mylist = []
    req = "select * from cars"
    

    myCursor = mydb.cursor()
    myCursor.execute(req)
    myresult = myCursor.fetchall()
    for x in myresult:
        car_instance = car.Car(x[0], x[1], x[2], str(x[3]),x[4])
        mylist.append(car_instance.__dict__)
    
    return json.dumps(mylist)

@app.route('/carsInParking', methods=['GET'])
def getCarsInParking():
    mylist = []
    try:
        myCursor = mydb.cursor()

        # Fetch cars with etat not equal to 'exterieur'
        req = "SELECT * FROM cars WHERE etat != 'exterieur'"
        myCursor.execute(req)
        myresult = myCursor.fetchall()

        cars_in_parking = []

        for x in myresult:
         car_instance = car.Car(x[0], x[1], x[2], str(x[3]),x[4])
         cars_in_parking.append(car_instance.__dict__)
    
        return json.dumps(cars_in_parking)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/saveEnregistrement', methods=['POST'])
def saveEnregistrement():
    try:
        data = request.get_json()
        code_matricule = data.get('code_matricule')

        # Get the current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert the new enregistrement into the database
        req = "INSERT INTO enregistrement (code_matricule, datetime_entree, datetime_sortie) VALUES (%s, %s, %s)"
        values = (code_matricule, current_datetime, None)  # Assuming datetime_sortie can be NULL

        myCursor = mydb.cursor()
        myCursor.execute(req, values)
        mydb.commit()

        return jsonify({"message": "Enregistrement added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/login' , methods = ['POST'])
def login():
    mylist = []
    args = request.json
    email=args.get('email')
    password_user=args.get('password')
    req = "select * from user where email=%s AND password=%s"
    val=(email,password_user)
    myCursor = mydb.cursor()
    myCursor.execute(req,val)
    myresult = myCursor.fetchall()
    if(myresult):
        exp_epoch=datetime.now()+timedelta(minutes=15)
        exp_epoch_time=int(exp_epoch.timestamp())
        myuser:myuser.user(email,password_user)
        payload={
        
            "exp":exp_epoch_time
        }
        token=jwt.encode(payload,"sagar",algorithm="HS256")
        return {'email':email,'password':password_user,'token':token}
    else:
       
        return {}
    
@app.route('/check_entre', methods=['POST'])
def check_entre():
    myCursor = mydb.cursor()
    try:
        data = request.get_json()
        code_matricule = data.get('code_matricule')
         # Check if the parking has available space (less than 30 cars in total)
        req_space_check = "SELECT COUNT(*) FROM cars WHERE etat = 'interieur'"
        myCursor = mydb.cursor()
        myCursor.execute(req_space_check)
        total_cars_in_parking = myCursor.fetchone()[0]

        if total_cars_in_parking >= 30:
            return jsonify({"error": "Parking is full. No available space."})


        # Check if the car exists
        car_exists_query = "SELECT * FROM cars WHERE code_matricule = %s"
        car_exists_values = (code_matricule,)
        myCursor.execute(car_exists_query, car_exists_values)
        car_exists = myCursor.fetchone()

        if not car_exists:
            return jsonify({"error": "Car does not exist"})

        # Check if there is a valid abonnement for the car
        abonnement_query = "SELECT * FROM abonnement WHERE code_matricule = %s AND date_expiration > NOW()"
        abonnement_values = (code_matricule,)
        myCursor.execute(abonnement_query, abonnement_values)
        valid_abonnement = myCursor.fetchone()

        if not valid_abonnement:
            return jsonify({"error": "Abonnement expired or not found"})

        # Insert enregistrement
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_enregistrement_query = "INSERT INTO enregistrement (code_matricule, datetime_entree, datetime_sortie) VALUES (%s, %s, NULL)"
        insert_enregistrement_values = (code_matricule, current_datetime)
        myCursor.execute(insert_enregistrement_query, insert_enregistrement_values)
        mydb.commit()

        # Update car's etat to 'interieur'
        update_etat_query = "UPDATE cars SET etat = 'interieur' WHERE code_matricule = %s"
        update_etat_values = (code_matricule,)
        myCursor.execute(update_etat_query, update_etat_values)
        mydb.commit()

        return jsonify({"message": "Enregistrement added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/check_sortie', methods=['POST'])
def check_sortie():
    myCursor = mydb.cursor()
    try:
        data = request.get_json()
        code_matricule = data.get('code_matricule')

        # Check if the car exists
        car_exists_query = "SELECT * FROM cars WHERE code_matricule = %s"
        car_exists_values = (code_matricule,)
        myCursor.execute(car_exists_query, car_exists_values)
        car_exists = myCursor.fetchone()

        if not car_exists:
            return jsonify({"error": "Car does not exist"})

        # Check if there is an active enregistrement for the car
        active_enregistrement_query = "SELECT * FROM enregistrement WHERE code_matricule = %s AND datetime_sortie IS NULL"
        active_enregistrement_values = (code_matricule,)
        myCursor.execute(active_enregistrement_query, active_enregistrement_values)
        active_enregistrement = myCursor.fetchone()

        if not active_enregistrement:
            return jsonify({"error": "No active enregistrement found for the car"})

        # Update date_sortie in enregistrement table
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_sortie_query = "UPDATE enregistrement SET datetime_sortie = %s WHERE code_matricule = %s AND datetime_sortie IS NULL"
        update_sortie_values = (current_datetime, code_matricule)
        myCursor.execute(update_sortie_query, update_sortie_values)
        mydb.commit()

        # Update car's etat to 'exterieur'
        update_etat_query = "UPDATE cars SET etat = 'exterieur' WHERE code_matricule = %s"
        update_etat_values = (code_matricule,)
        myCursor.execute(update_etat_query, update_etat_values)
        mydb.commit()

        return jsonify({"message": "Sortie enregistrement processed successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})



app.run()
#we can add car without model
#def addCar():
   
#   value=('mercedes',123456,'marquex')
#   cursor = cnx.cursor()
#   cursor.execute("insert into cars(model,hp,marque) values(%s,%s,%s)",value)
#   cnx.commit()
#   cursor.close()
#   return "done"
