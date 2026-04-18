import cv2
import face_recognition
import mysql.connector

def register_user(name, img):
    connection = mysql.connector.connect (
        host="localhost",
        user="root",
        password="",
        database="face_recognition_db"
    )
    
    cursor = connection.cursor()
    
    
    print(f"Registering user: {name}....")
    
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb)
    
    if encodings:
        encoding = encodings[0]
        encoding_string = str(encoding.tolist())
    
        cursor.execute(
            "INSERT INTO users (name, Encoding) VALUES (%s, %s)",
            (name, encoding_string)
        )
        connection.commit()
    
        print(f"User {name} registered successfully!")
    else:
        print("No face detected. Please try again.")
