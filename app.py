from flask import jsonify,Flask,render_template,request
from flask_cors import CORS,cross_origin
from flask_mysqldb import MySQL
import json
import mysql.connector
import myCar as car
import user as user
import jwt
from datetime import datetime,timedelta

app = Flask(__name__)

CORS(app)
mydb=mysql.connector.connect(user='root',password='',host='localhost',database='projectflask')

app.config["DEBUG"]=True



@app.route('/savecar' , methods = ['POST'])
def saveCar():

    args = request.json
    print(args)
    id_car = args.get('id')
    model = args.get('model')
    hp = args.get('hp')
    marque = args.get('marque')

    myCursor = mydb.cursor()

    mycar = car.Car(id_car , model ,hp , marque)
    req = "insert into cars (model , hp , marque ) values (%s , %s , %s)"
    val = (mycar.model , mycar.hp , mycar.marque)
    myCursor.execute(req , val)
    mydb.commit()
    return {'status':'save :'}
@app.route('/cars' , methods = ['GET'])
def getCars():
    mylist = []
    req = "select * from cars"
    

    myCursor = mydb.cursor()
    myCursor.execute(req)
    myresult = myCursor.fetchall()
    for x in myresult:
        mylist.append(car.Car(x[0] ,x[1], x[2] , x[3]).__dict__)
        

    return json.dumps(mylist)
@app.route('/login' , methods = ['POST'])
def login():
    mylist = []
    args = request.json
    id_user=args.get('id')
    email=args.get('email')
    password_user=args.get('password')
    req = "select * from users where email=%s AND password=%s"
    val=(email,password_user)
    myCursor = mydb.cursor()
    myCursor.execute(req,val)
    myresult = myCursor.fetchall()
    if(myresult):
        exp_epoch=datetime.now()+timedelta(minutes=15)
        exp_epoch_time=int(exp_epoch.timestamp())
        myuser:myuser.user(id_user,email,password_user)
        payload={
            "payload":id_user,
            "exp":exp_epoch_time
        }
        token=jwt.encode(payload,"sagar",algorithm="HS256")
        return {'id':id_user,'email':email,'password':password_user,'token':token}
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
