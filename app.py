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
    
    

    

app.run()
#we can add car without model
#def addCar():
   
#   value=('mercedes',123456,'marquex')
#   cursor = cnx.cursor()
#   cursor.execute("insert into cars(model,hp,marque) values(%s,%s,%s)",value)
#   cnx.commit()
#   cursor.close()
#   return "done"
