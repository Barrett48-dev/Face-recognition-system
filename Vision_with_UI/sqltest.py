import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="face_recognition_db"
    )

    if connection.is_connected():
        print("Connected to MySQL successfully!")

except mysql.connector.Error as e:
    print("Error:", e)