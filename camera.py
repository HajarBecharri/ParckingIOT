import cv2
import pytesseract
from datetime import datetime
import mysql.connector
from flask import jsonify,Flask
from flask_cors import CORS
import mysql.connector
from datetime import datetime,timedelta
import serial
import time
import re
import connection

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
CORS(app)
mydb=mydb = connection.get_database()

app.config["DEBUG"]=True

def check(code_matricule):
    
    myCursor = mydb.cursor()
    try:
        # Check if the car exists
        car_exists_query = "SELECT * FROM cars WHERE code_matricule = %s"
        car_exists_values = (code_matricule,)
        myCursor.execute(car_exists_query, car_exists_values)
        car_exists = myCursor.fetchone()

        if not car_exists:
            return "Car does not exist"

        # Check if the parking is full
        req_space_check = "SELECT COUNT(*) FROM cars WHERE etat = 'interieur'"
        myCursor.execute(req_space_check)
        total_cars_in_parking = myCursor.fetchone()[0]

        if total_cars_in_parking >= 30:
            return "Parking is full. No available space."

        # Determine which method to call based on the car's etat
        etat_index = 4  # Assuming 'etat' is the second column
        if car_exists[etat_index] == 'exterieur':
            # Call check_entre method
            return check_entre(code_matricule)
        elif car_exists[etat_index] == 'interieur':
            # Call check_sortie method
            return check_sortie(code_matricule)
        else:
            return "Invalid car state"

    except Exception as e:
        return str(e)


def check_entre(code_matricule):
    myCursor = mydb.cursor()
    try:
        # Check if the parking has available space (less than 30 cars in total)
        req_space_check = "SELECT COUNT(*) FROM cars WHERE etat = 'interieur'"
        myCursor.execute(req_space_check)
        total_cars_in_parking = myCursor.fetchone()[0]

        if total_cars_in_parking >= 30:
            return ("Parking is full. No available space.")

        # Check if there is a valid abonnement for the car
        abonnement_query = "SELECT * FROM abonnement WHERE code_matricule = %s AND date_expiration > NOW()"
        abonnement_values = (code_matricule,)
        myCursor.execute(abonnement_query, abonnement_values)
        valid_abonnement = myCursor.fetchone()

        if not valid_abonnement:
            return jsonify("Abonnement expired or not found")
        #sr.write(1)
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

        return ("Enregistrement added successfully")

    except Exception as e:
        return (str(e))
def check_sortie(code_matricule):
    myCursor = mydb.cursor()
    try:
        # Check if there is an active enregistrement for the car
        active_enregistrement_query = "SELECT * FROM enregistrement WHERE code_matricule = %s AND datetime_sortie IS NULL"
        active_enregistrement_values = (code_matricule,)
        myCursor.execute(active_enregistrement_query, active_enregistrement_values)
        active_enregistrement = myCursor.fetchone()

        if not active_enregistrement:
            return ("No active enregistrement found for the car")
        
        #sr.write(1)
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

        return ("Sortie enregistrement processed successfully")

    except Exception as e:
        return (e)

def text_detection(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to perform OCR on the frame
    text = pytesseract.image_to_string(gray)

    return text

def video_stream():
    try:
     sr = serial.Serial("COM5", 9600) 
     print("Serial connection established.")
     print("Command sent to Arduino.")
    except serial.SerialException as e:
     print(f"Error opening serial port: {e}")
     exit()
    vs = cv2.VideoCapture(0)

    while True:
        ret, frame = vs.read()

        # Detect text in the frame
        detected_text = text_detection(frame)
        # If text is detected, print it in the console
        if(detected_text):
             detected_text_wittout_spce = detected_text.strip()
             print("Result",detected_text_wittout_spce)
             result = check(detected_text_wittout_spce)
             if result == "Enregistrement added successfully" or result == "Sortie enregistrement processed successfully":
                 print("Result",result)
                 sr.write(str(1).encode())
                 time.sleep(2000)
             else:
                  print("Result",result)
                  sr.write(str(0).encode())
             
          
        # Display the frame in the console
        cv2.imshow('Video Feed', frame)

        # Break the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture and destroy all OpenCV windows
    vs.release()
    cv2.destroyAllWindows()
def is_valid_format(text):

    pattern = re.compile(r'^[a-zA-Z]+\s[a-zA-Z]+\d{2}\s\d{2}\s\d{2}$')
    return bool(pattern.match(text))


    
if __name__ == "__main__":
    video_stream()
   