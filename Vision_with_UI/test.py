import cv2
import face_recognition
import mysql.connector

def register_user(name):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="face_recognition_db"
    )

    cursor = connection.cursor()

    cap = cv2.VideoCapture(0)

    print(f"Registering {name}... Press 's' to capture")

    while True:
        success, img = cap.read()
        cv2.imshow("Register User", img)

        key = cv2.waitKey(1)

        if key == ord('s'):
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb)

            if encodings:
                encoding = encodings[0]
                encoding_string = str(encoding.tolist())

                cursor.execute(
                    "INSERT INTO users (name, face_encoding) VALUES (%s, %s)",
                    (name, encoding_string)
                )
                connection.commit()

                print(f"{name} registered successfully!")
            else:
                print("No face detected")

            break

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()