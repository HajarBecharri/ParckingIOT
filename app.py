from flask import jsonify,Flask,render_template,request,Response
from flask_cors import CORS,cross_origin
import time
import json
import mysql.connector
import myCar as car
import user as user
import enregistrement as eng
import jwt
from datetime import datetime,timedelta
import os
import cv2
import pytesseract
import serial

try:
    sr = serial.Serial("COM5", 9600) 
    print("Serial connection established.")
    sr.write('1'.encode())
    print("Command sent to Arduino.")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
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


@app.route('/savecar' , methods = ['POST'])
def saveCar():
    args = request.json
    print(args)
    code_matricule = args.get('code_matricule')
    nom_client = args.get('nom_client') 
    cni_client = args.get('cni_client') 
    date_enregistrement = args.get('date_enregistrement')
    etat = args.get('etat')
    mycar = car.Car(code_matricule, nom_client, cni_client, date_enregistrement, etat)
    mydb = get_database()
    myCursor = mydb.cursor()
    req = "insert into cars (code_matricule, nom_client, cni_client, date_enregistrement) values (%s, %s, %s, %s)"
    val = (mycar.code_matricule, mycar.nom_client, mycar.cni_client, mycar.date_enregistrement)
    myCursor.execute(req, val)
    mydb.commit()
    mydb.close()
    return {'status': 'save :'}

@app.route('/saveabonnement', methods=['POST'])
def save_abonnement():
    mydb=get_database()
    args = request.json
    code_matricule = args.get('code_matricule')
    date_expiration = args.get('date_expiration')
    myCursor = mydb.cursor()
    req = "INSERT INTO abonnement (code_matricule, date_expiration) VALUES (%s, %s)"
    val = (code_matricule, date_expiration)
    try:
        myCursor.execute(req, val)
        mydb.commit()
        mydb.close()
        return {'status': 'success', 'message': 'Abonnement ajouté avec succès'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@app.route('/enregistrement' , methods = ['GET'])
def getenregistremnts():
    mydb=get_database()
    mylist = []
    req = "select * from enregistrement"
    

    myCursor = mydb.cursor()
    myCursor.execute(req)
    myresult = myCursor.fetchall()
    for x in myresult:
        enregistrement_instance = eng.Enregistrement(x[0], x[1], str(x[2]), str(x[3]))
        mylist.append(enregistrement_instance.__dict__)
    mydb.close()
    return json.dumps(mylist)

@app.route('/cars' , methods = ['GET'])
def getCars():
    mydb=get_database()
    mylist = []
    req = "select * from cars"
    myCursor = mydb.cursor()
    myCursor.execute(req)
    myresult = myCursor.fetchall()
    for x in myresult:
        car_instance = car.Car(x[0], x[1], x[2], str(x[3]),x[4])
        mylist.append(car_instance.__dict__)
    mydb.close()
    return json.dumps(mylist)

@app.route('/carsInParking', methods=['GET'])
def getCarsInParking():
    mydb=get_database()
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
        mydb.close()
        return json.dumps(cars_in_parking)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/saveEnregistrement', methods=['POST'])
def saveEnregistrement():
    mydb=get_database()
    try:
        data = request.get_json()
        code_matricule = data.get('code_matricule')
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        req = "INSERT INTO enregistrement (code_matricule, datetime_entree, datetime_sortie) VALUES (%s, %s, %s)"
        values = (code_matricule, current_datetime, None)
        myCursor = mydb.cursor()
        myCursor.execute(req, values)
        mydb.commit()
        mydb.close()
        return jsonify({"message": "Enregistrement added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})
@app.route('/login' , methods = ['POST'])
def login():
    mydb=get_database()
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
        mydb.close()
        return {'email':email,'password':password_user,'token':token}
    else:
       
        return {}
    

def check_entre(code):
    mydb=get_database()
    myCursor = mydb.cursor()
    try:
        
        code_matricule = code
        req_space_check = "SELECT COUNT(*) FROM cars WHERE etat = 'interieur'"
        myCursor = mydb.cursor()
        myCursor.execute(req_space_check)
        total_cars_in_parking = myCursor.fetchone()[0]
        if total_cars_in_parking >= 30:
            return jsonify({"error": "Parking is full. No available space."})
        car_exists_query = "SELECT * FROM cars WHERE code_matricule = %s"
        car_exists_values = (code_matricule,)
        myCursor.execute(car_exists_query, car_exists_values)
        car_exists = myCursor.fetchone()

        if not car_exists:
            return jsonify({"error": "Car does not exist"})
        abonnement_query = "SELECT * FROM abonnement WHERE code_matricule = %s AND date_expiration > NOW()"
        abonnement_values = (code_matricule,)
        myCursor.execute(abonnement_query, abonnement_values)
        valid_abonnement = myCursor.fetchone()
        


        if not valid_abonnement:
            return jsonify({"error": "Abonnement expired or not found"})
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_enregistrement_query = "INSERT INTO enregistrement (code_matricule, datetime_entree, datetime_sortie) VALUES (%s, %s, NULL)"
        insert_enregistrement_values = (code_matricule, current_datetime)
        myCursor.execute(insert_enregistrement_query, insert_enregistrement_values)
        mydb.commit()
        update_etat_query = "UPDATE cars SET etat = 'interieur' WHERE code_matricule = %s"
        update_etat_values = (code_matricule,)
        myCursor.execute(update_etat_query, update_etat_values)
        mydb.commit()
        mydb.close()
        return jsonify({"message": "Enregistrement added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)})


def check_sortie():
    mydb=get_database()
    myCursor = mydb.cursor()
    try:
        data = request.get_json()
        code_matricule = data.get('code_matricule')
        car_exists_query = "SELECT * FROM cars WHERE code_matricule = %s"
        car_exists_values = (code_matricule,)
        myCursor.execute(car_exists_query, car_exists_values)
        car_exists = myCursor.fetchone()

        if not car_exists:
            return jsonify({"error": "Car does not exist"})
        active_enregistrement_query = "SELECT * FROM enregistrement WHERE code_matricule = %s AND datetime_sortie IS NULL"
        active_enregistrement_values = (code_matricule,)
        myCursor.execute(active_enregistrement_query, active_enregistrement_values)
        active_enregistrement = myCursor.fetchone()

        if not active_enregistrement:
            return jsonify({"error": "No active enregistrement found for the car"})
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_sortie_query = "UPDATE enregistrement SET datetime_sortie = %s WHERE code_matricule = %s AND datetime_sortie IS NULL"
        update_sortie_values = (current_datetime, code_matricule)
        myCursor.execute(update_sortie_query, update_sortie_values)
        mydb.commit()
        update_etat_query = "UPDATE cars SET etat = 'exterieur' WHERE code_matricule = %s"
        update_etat_values = (code_matricule,)
        myCursor.execute(update_etat_query, update_etat_values)
        mydb.commit()
        mydb.close()
        return jsonify({"message": "Sortie enregistrement processed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})



def text_detection(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to perform OCR on the frame
    text = pytesseract.image_to_string(gray)

    return text

def video_stream():
    vs = cv2.VideoCapture(0)

    while True:
        ret, frame = vs.read()

        # Detect text in the frame
        detected_text = text_detection(frame)

        # If text is detected, print it in the console
        if detected_text:
            print("Detected Text:", detected_text)
            result = check_entre(detected_text)
            print(result.get_data(as_text=True))
            sr.write(b'1')  # Send the byte representation of the integer 1
            time.sleep(2)   # Wait for the Arduino to process the data
            sr.close()
            # Wait for 15 seconds before capturing the next frame
            time.sleep(15)

        # Display the frame in the console
        cv2.imshow('Video Feed', frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture and destroy all OpenCV windows
    vs.release()
    cv2.destroyAllWindows()

@app.route("/ws")
def video_feed():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace;boundary=frame')
@app.route("/CB")
def close_barrier():
    send_integer_to_arduino(1) 
    time.sleep(2)   # Wait for the Arduino to process the data
    sr.close()
    
    return jsonify({"status": "Barrier closed"})

def send_integer_to_arduino(value):
    # Convert the integer to a string and encode it as ASCII
    data = str(value).encode('ascii')

    # Send the string to Arduino
    sr.write(data)

# app.run()

